from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Project, SDLCBreakdown, SDLCPhase, get_session
import json

class ProjectRepository:
    """Repository for managing project data in the database"""
    
    def __init__(self, session: Optional[Session] = None):
        self.session = session or get_session()
    
    def save_project(self, project_data: Dict[str, Any]) -> int:
        """Save project information and return project ID"""
        project = Project(
            name=project_data['name'],
            description=project_data['description'],
            duration_weeks=project_data['duration_weeks'],
            team_size=project_data['team_size'],
            project_type=project_data['project_type'],
            methodology=project_data['methodology']
        )
        
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project.id
    
    def save_sdlc_breakdown(self, project_id: int, ai_response: str, parsed_data: Dict[str, Any]) -> int:
        """Save SDLC breakdown data and return breakdown ID"""
        breakdown = SDLCBreakdown(
            project_id=project_id,
            ai_response=ai_response,
            parsed_data=parsed_data,
            total_phases=len(parsed_data.get('phases', [])),
            complexity_assessment=parsed_data.get('project_summary', {}).get('complexity_assessment', 'Medium')
        )
        
        self.session.add(breakdown)
        self.session.commit()
        self.session.refresh(breakdown)
        
        # Save individual phases
        phases = parsed_data.get('phases', [])
        for i, phase_data in enumerate(phases):
            phase = SDLCPhase(
                breakdown_id=breakdown.id,
                phase_order=i + 1,
                name=phase_data.get('name', ''),
                description=phase_data.get('description', ''),
                duration_weeks=phase_data.get('duration_weeks', 0),
                percentage=phase_data.get('percentage', 0.0),
                deliverables=phase_data.get('deliverables', []),
                activities=phase_data.get('activities', []),
                team_focus=phase_data.get('team_focus', '')
            )
            self.session.add(phase)
        
        self.session.commit()
        return breakdown.id
    
    def get_project_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent project history"""
        projects = self.session.query(Project).order_by(Project.created_at.desc()).limit(limit).all()
        
        history = []
        for project in projects:
            # Get latest breakdown for this project
            breakdown = self.session.query(SDLCBreakdown).filter_by(project_id=project.id).order_by(SDLCBreakdown.created_at.desc()).first()
            
            history.append({
                'id': project.id,
                'name': project.name,
                'project_type': project.project_type,
                'methodology': project.methodology,
                'duration_weeks': project.duration_weeks,
                'team_size': project.team_size,
                'created_at': project.created_at,
                'has_breakdown': breakdown is not None,
                'total_phases': breakdown.total_phases if breakdown else 0,
                'complexity': breakdown.complexity_assessment if breakdown else 'Unknown'
            })
        
        return history
    
    def get_project_breakdown(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get SDLC breakdown for a specific project"""
        breakdown = self.session.query(SDLCBreakdown).filter_by(project_id=project_id).order_by(SDLCBreakdown.created_at.desc()).first()
        
        if not breakdown:
            return None
        
        return breakdown.parsed_data
    
    def get_analytics_data(self) -> Dict[str, Any]:
        """Get analytics data for dashboard"""
        total_projects = self.session.query(Project).count()
        total_breakdowns = self.session.query(SDLCBreakdown).count()
        
        # Most popular methodologies
        methodology_stats = self.session.query(
            Project.methodology,
            func.count(Project.id).label('count')
        ).group_by(Project.methodology).all()
        
        # Most popular project types
        type_stats = self.session.query(
            Project.project_type,
            func.count(Project.id).label('count')
        ).group_by(Project.project_type).all()
        
        # Average duration by project type
        duration_stats = self.session.query(
            Project.project_type,
            func.avg(Project.duration_weeks).label('avg_duration')
        ).group_by(Project.project_type).all()
        
        return {
            'total_projects': total_projects,
            'total_breakdowns': total_breakdowns,
            'methodology_distribution': {row[0]: row[1] for row in methodology_stats},
            'project_type_distribution': {row[0]: row[1] for row in type_stats},
            'average_duration_by_type': {row[0]: float(row[1]) if row[1] else 0.0 for row in duration_stats}
        }
    
    def search_projects(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search projects by name or description"""
        projects = self.session.query(Project).filter(
            Project.name.ilike(f'%{query}%') | 
            Project.description.ilike(f'%{query}%')
        ).order_by(Project.created_at.desc()).limit(limit).all()
        
        results = []
        for project in projects:
            breakdown = self.session.query(SDLCBreakdown).filter_by(project_id=project.id).order_by(SDLCBreakdown.created_at.desc()).first()
            
            description_text = project.description
            truncated_description = description_text[:200] + '...' if len(description_text) > 200 else description_text
            
            results.append({
                'id': project.id,
                'name': project.name,
                'description': truncated_description,
                'project_type': project.project_type,
                'methodology': project.methodology,
                'duration_weeks': project.duration_weeks,
                'created_at': project.created_at,
                'has_breakdown': breakdown is not None
            })
        
        return results
    
    def close(self):
        """Close the database session"""
        self.session.close()