import json
import re
from typing import Dict, Any, List, Optional

class SDLCParser:
    """Parser class for processing AI-generated SDLC breakdowns"""
    
    def parse_ai_response(self, ai_response: str, expected_duration: int) -> Dict[str, Any]:
        """Parse the AI response and validate the SDLC breakdown"""
        
        try:
            # Extract JSON from the response
            json_data = self._extract_json_from_response(ai_response)
            
            if not json_data:
                # Fallback: create basic structure from text
                return self._create_fallback_structure(ai_response, expected_duration)
            
            # Validate and clean the parsed data
            validated_data = self._validate_and_clean(json_data, expected_duration)
            
            return validated_data
            
        except Exception as e:
            # If parsing fails, create a basic structure
            return self._create_fallback_structure(ai_response, expected_duration)
    
    def _extract_json_from_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from AI response, handling various formats"""
        
        # Try to find JSON in the response
        json_patterns = [
            r'\{.*\}',  # Basic JSON pattern
            r'```json\s*(\{.*?\})\s*```',  # JSON in code blocks
            r'```\s*(\{.*?\})\s*```',  # JSON in generic code blocks
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, response, re.DOTALL)
            for match in matches:
                try:
                    # Clean the JSON string
                    json_str = match.strip()
                    if not json_str.startswith('{'):
                        continue
                    
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    continue
        
        # Try to parse the entire response as JSON
        try:
            return json.loads(response.strip())
        except json.JSONDecodeError:
            return None
    
    def _validate_and_clean(self, data: Dict[str, Any], expected_duration: int) -> Dict[str, Any]:
        """Validate and clean the parsed SDLC data"""
        
        # Ensure required structure
        if 'phases' not in data:
            data['phases'] = []
        
        phases = data['phases']
        if not phases:
            return self._create_default_phases(expected_duration)
        
        # Validate and adjust phase durations
        total_weeks = sum(phase.get('duration_weeks', 0) for phase in phases)
        
        if total_weeks != expected_duration:
            # Adjust durations proportionally
            if total_weeks > 0:
                adjustment_factor = expected_duration / total_weeks
                for phase in phases:
                    original_duration = phase.get('duration_weeks', 0)
                    phase['duration_weeks'] = max(1, round(original_duration * adjustment_factor))
            else:
                # If no valid durations, distribute equally
                duration_per_phase = max(1, expected_duration // len(phases))
                remaining_weeks = expected_duration - (duration_per_phase * len(phases))
                
                for i, phase in enumerate(phases):
                    phase['duration_weeks'] = duration_per_phase
                    if i < remaining_weeks:
                        phase['duration_weeks'] += 1
        
        # Recalculate percentages
        total_weeks = sum(phase['duration_weeks'] for phase in phases)
        for phase in phases:
            phase['percentage'] = (phase['duration_weeks'] / total_weeks) * 100
        
        # Ensure all phases have required fields
        for phase in phases:
            phase.setdefault('name', 'Unnamed Phase')
            phase.setdefault('description', 'Phase description not available')
            phase.setdefault('deliverables', [])
            phase.setdefault('activities', [])
            phase.setdefault('team_focus', 'General development')
        
        # Add project summary if missing
        if 'project_summary' not in data:
            data['project_summary'] = {
                'name': 'Software Project',
                'total_duration_weeks': expected_duration,
                'methodology': 'Agile',
                'complexity_assessment': 'Medium'
            }
        
        return data
    
    def _create_fallback_structure(self, ai_response: str, expected_duration: int) -> Dict[str, Any]:
        """Create a fallback SDLC structure when parsing fails"""
        
        # Try to extract phase information from text
        phases = self._extract_phases_from_text(ai_response, expected_duration)
        
        if not phases:
            phases = self._create_default_phases(expected_duration)
        
        return {
            'project_summary': {
                'name': 'Software Project',
                'total_duration_weeks': expected_duration,
                'methodology': 'Agile',
                'complexity_assessment': 'Medium'
            },
            'phases': phases,
            'recommendations': [
                'Review and adjust phases based on project specifics',
                'Consider team experience and project complexity',
                'Plan for regular reviews and adjustments'
            ]
        }
    
    def _extract_phases_from_text(self, text: str, expected_duration: int) -> List[Dict[str, Any]]:
        """Extract phase information from plain text response"""
        
        phases = []
        
        # Look for common phase patterns in text
        phase_patterns = [
            r'(\d+)\.\s*([^:\n]+):\s*([^:\n]+)',  # "1. Phase Name: Description"
            r'([A-Z][^:\n]+):\s*(\d+)\s*weeks?',  # "Phase Name: X weeks"
            r'Phase\s*\d*:\s*([^:\n]+)',  # "Phase: Name"
        ]
        
        for pattern in phase_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                for match in matches:
                    if len(match) >= 2:
                        phase_name = match[1] if len(match) > 2 else match[0]
                        phases.append({
                            'name': phase_name.strip(),
                            'description': 'Extracted from AI response',
                            'deliverables': [],
                            'activities': [],
                            'team_focus': 'General development'
                        })
        
        if phases:
            # Distribute duration evenly
            duration_per_phase = max(1, expected_duration // len(phases))
            remaining_weeks = expected_duration - (duration_per_phase * len(phases))
            
            for i, phase in enumerate(phases):
                phase['duration_weeks'] = duration_per_phase
                if i < remaining_weeks:
                    phase['duration_weeks'] += 1
                phase['percentage'] = (phase['duration_weeks'] / expected_duration) * 100
        
        return phases
    
    def _create_default_phases(self, expected_duration: int) -> List[Dict[str, Any]]:
        """Create default SDLC phases when no valid data is available"""
        
        default_phases = [
            {
                'name': 'Requirements Analysis & Planning',
                'description': 'Gather requirements, analyze feasibility, and create project plan',
                'deliverables': ['Requirements document', 'Project plan', 'Technical specifications'],
                'activities': ['Stakeholder interviews', 'Requirements gathering', 'Risk assessment'],
                'team_focus': 'Business analysis and planning'
            },
            {
                'name': 'System Design & Architecture',
                'description': 'Design system architecture, database schema, and technical specifications',
                'deliverables': ['System architecture document', 'Database design', 'UI/UX mockups'],
                'activities': ['System design', 'Architecture planning', 'Technology selection'],
                'team_focus': 'System architects and designers'
            },
            {
                'name': 'Development & Implementation',
                'description': 'Code development, feature implementation, and integration',
                'deliverables': ['Working software modules', 'Code documentation', 'Unit tests'],
                'activities': ['Coding', 'Code reviews', 'Module integration'],
                'team_focus': 'Development team'
            },
            {
                'name': 'Testing & Quality Assurance',
                'description': 'Comprehensive testing including unit, integration, and user acceptance testing',
                'deliverables': ['Test results', 'Bug reports', 'Test documentation'],
                'activities': ['Test execution', 'Bug fixing', 'Performance testing'],
                'team_focus': 'QA and testing team'
            },
            {
                'name': 'Deployment & Launch',
                'description': 'Production deployment, user training, and go-live activities',
                'deliverables': ['Production system', 'User documentation', 'Training materials'],
                'activities': ['Production deployment', 'User training', 'Go-live support'],
                'team_focus': 'DevOps and support team'
            }
        ]
        
        # Distribute duration based on typical percentages
        typical_percentages = [15, 20, 40, 20, 5]  # Typical SDLC distribution
        
        for i, phase in enumerate(default_phases):
            percentage = typical_percentages[i]
            duration = max(1, round(expected_duration * percentage / 100))
            phase['duration_weeks'] = duration
            phase['percentage'] = percentage
        
        # Adjust to match exact duration
        total_allocated = sum(phase['duration_weeks'] for phase in default_phases)
        difference = expected_duration - total_allocated
        
        if difference != 0:
            # Adjust the development phase (usually the largest)
            default_phases[2]['duration_weeks'] += difference
            
            # Recalculate percentages
            total_weeks = sum(phase['duration_weeks'] for phase in default_phases)
            for phase in default_phases:
                phase['percentage'] = (phase['duration_weeks'] / total_weeks) * 100
        
        return default_phases
