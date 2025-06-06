import json
import csv
import io
from typing import Dict, Any, List
from datetime import datetime

class ExportUtils:
    """Utility class for exporting SDLC breakdown data in various formats"""
    
    def to_json(self, sdlc_data: Dict[str, Any]) -> str:
        """Export SDLC data to JSON format"""
        export_data = {
            'generated_at': datetime.now().isoformat(),
            'sdlc_breakdown': sdlc_data
        }
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    def to_csv(self, sdlc_data: Dict[str, Any]) -> str:
        """Export SDLC phases to CSV format"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Phase Name',
            'Duration (Weeks)',
            'Percentage',
            'Description',
            'Key Deliverables',
            'Main Activities',
            'Team Focus'
        ])
        
        # Write phase data
        phases = sdlc_data.get('phases', [])
        for phase in phases:
            deliverables_str = '; '.join(phase.get('deliverables', []))
            activities_str = '; '.join(phase.get('activities', []))
            
            writer.writerow([
                phase.get('name', ''),
                phase.get('duration_weeks', 0),
                f"{phase.get('percentage', 0):.1f}%",
                phase.get('description', ''),
                deliverables_str,
                activities_str,
                phase.get('team_focus', '')
            ])
        
        return output.getvalue()
    
    def to_markdown(self, sdlc_data: Dict[str, Any]) -> str:
        """Export SDLC breakdown to Markdown format"""
        
        project_summary = sdlc_data.get('project_summary', {})
        phases = sdlc_data.get('phases', [])
        
        md_content = []
        
        # Title and summary
        md_content.append(f"# SDLC Breakdown: {project_summary.get('name', 'Software Project')}")
        md_content.append("")
        md_content.append(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_content.append(f"**Total Duration:** {project_summary.get('total_duration_weeks', 0)} weeks")
        md_content.append(f"**Methodology:** {project_summary.get('methodology', 'N/A')}")
        md_content.append(f"**Complexity Assessment:** {project_summary.get('complexity_assessment', 'N/A')}")
        md_content.append("")
        
        # Phase overview table
        md_content.append("## Phase Overview")
        md_content.append("")
        md_content.append("| Phase | Duration | Percentage |")
        md_content.append("|-------|----------|------------|")
        
        for phase in phases:
            md_content.append(f"| {phase.get('name', '')} | {phase.get('duration_weeks', 0)} weeks | {phase.get('percentage', 0):.1f}% |")
        
        md_content.append("")
        
        # Detailed phase breakdown
        md_content.append("## Detailed Phase Breakdown")
        md_content.append("")
        
        for i, phase in enumerate(phases, 1):
            md_content.append(f"### Phase {i}: {phase.get('name', '')}")
            md_content.append("")
            md_content.append(f"**Duration:** {phase.get('duration_weeks', 0)} weeks ({phase.get('percentage', 0):.1f}%)")
            md_content.append("")
            md_content.append(f"**Description:** {phase.get('description', '')}")
            md_content.append("")
            
            if phase.get('deliverables'):
                md_content.append("**Key Deliverables:**")
                for deliverable in phase['deliverables']:
                    md_content.append(f"- {deliverable}")
                md_content.append("")
            
            if phase.get('activities'):
                md_content.append("**Main Activities:**")
                for activity in phase['activities']:
                    md_content.append(f"- {activity}")
                md_content.append("")
            
            if phase.get('team_focus'):
                md_content.append(f"**Team Focus:** {phase['team_focus']}")
                md_content.append("")
        
        # Recommendations
        recommendations = sdlc_data.get('recommendations', [])
        if recommendations:
            md_content.append("## Recommendations")
            md_content.append("")
            for rec in recommendations:
                md_content.append(f"- {rec}")
            md_content.append("")
        
        return '\n'.join(md_content)
    
    def generate_summary(self, sdlc_data: Dict[str, Any]) -> str:
        """Generate a text summary of the SDLC breakdown"""
        
        project_summary = sdlc_data.get('project_summary', {})
        phases = sdlc_data.get('phases', [])
        
        summary_lines = []
        summary_lines.append(f"Project: {project_summary.get('name', 'Software Project')}")
        summary_lines.append(f"Total Duration: {project_summary.get('total_duration_weeks', 0)} weeks")
        summary_lines.append(f"Number of Phases: {len(phases)}")
        summary_lines.append("")
        summary_lines.append("Phase Breakdown:")
        
        for phase in phases:
            summary_lines.append(f"• {phase.get('name', '')}: {phase.get('duration_weeks', 0)} weeks ({phase.get('percentage', 0):.1f}%)")
        
        return '\n'.join(summary_lines)
    
    def to_gantt_data(self, sdlc_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convert SDLC data to format suitable for Gantt chart visualization"""
        
        phases = sdlc_data.get('phases', [])
        gantt_data = []
        
        current_start = 0
        for phase in phases:
            duration = phase.get('duration_weeks', 0)
            gantt_data.append({
                'Task': phase.get('name', ''),
                'Start': current_start,
                'Finish': current_start + duration,
                'Duration': duration,
                'Description': phase.get('description', ''),
                'Team': phase.get('team_focus', '')
            })
            current_start += duration
        
        return gantt_data
