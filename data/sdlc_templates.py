from typing import Dict, List, Any

class SDLCTemplates:
    """Templates and reference data for SDLC phases and methodologies"""
    
    @staticmethod
    def get_agile_template() -> Dict[str, Any]:
        """Get standard Agile SDLC template"""
        return {
            'methodology': 'Agile',
            'phases': [
                {
                    'name': 'Project Initiation & Planning',
                    'typical_percentage': 10,
                    'description': 'Initial project setup, team formation, and high-level planning',
                    'deliverables': ['Project charter', 'Team setup', 'Initial backlog'],
                    'activities': ['Stakeholder alignment', 'Team formation', 'Tool setup']
                },
                {
                    'name': 'Requirements & User Stories',
                    'typical_percentage': 15,
                    'description': 'Detailed requirements gathering and user story creation',
                    'deliverables': ['User stories', 'Acceptance criteria', 'Product backlog'],
                    'activities': ['User story writing', 'Story mapping', 'Backlog grooming']
                },
                {
                    'name': 'Sprint Planning & Design',
                    'typical_percentage': 10,
                    'description': 'Sprint planning, architecture design, and UI/UX design',
                    'deliverables': ['Sprint plans', 'Architecture design', 'UI mockups'],
                    'activities': ['Sprint planning', 'Architecture design', 'Design reviews']
                },
                {
                    'name': 'Development Sprints',
                    'typical_percentage': 50,
                    'description': 'Iterative development with regular sprints and reviews',
                    'deliverables': ['Working software increments', 'Sprint reviews', 'Updated backlog'],
                    'activities': ['Coding', 'Daily standups', 'Sprint reviews', 'Retrospectives']
                },
                {
                    'name': 'Testing & Integration',
                    'typical_percentage': 10,
                    'description': 'Continuous testing, integration, and quality assurance',
                    'deliverables': ['Test reports', 'Bug fixes', 'Integration tests'],
                    'activities': ['Automated testing', 'Manual testing', 'Bug fixing']
                },
                {
                    'name': 'Deployment & Release',
                    'typical_percentage': 5,
                    'description': 'Production deployment and go-live activities',
                    'deliverables': ['Production release', 'Deployment documentation', 'User training'],
                    'activities': ['Production deployment', 'User training', 'Go-live support']
                }
            ]
        }
    
    @staticmethod
    def get_waterfall_template() -> Dict[str, Any]:
        """Get standard Waterfall SDLC template"""
        return {
            'methodology': 'Waterfall',
            'phases': [
                {
                    'name': 'Requirements Analysis',
                    'typical_percentage': 15,
                    'description': 'Comprehensive requirements gathering and analysis',
                    'deliverables': ['Requirements specification', 'Feasibility study', 'Project plan'],
                    'activities': ['Requirements gathering', 'Stakeholder interviews', 'Documentation']
                },
                {
                    'name': 'System Design',
                    'typical_percentage': 20,
                    'description': 'Detailed system and architectural design',
                    'deliverables': ['System design document', 'Database design', 'UI/UX design'],
                    'activities': ['Architecture design', 'Database design', 'Interface design']
                },
                {
                    'name': 'Implementation',
                    'typical_percentage': 35,
                    'description': 'Code development and module implementation',
                    'deliverables': ['Source code', 'Code documentation', 'Unit tests'],
                    'activities': ['Coding', 'Code reviews', 'Unit testing']
                },
                {
                    'name': 'Testing',
                    'typical_percentage': 20,
                    'description': 'Comprehensive system testing and quality assurance',
                    'deliverables': ['Test plans', 'Test results', 'Bug reports'],
                    'activities': ['System testing', 'Integration testing', 'User acceptance testing']
                },
                {
                    'name': 'Deployment',
                    'typical_percentage': 5,
                    'description': 'System deployment and production release',
                    'deliverables': ['Production system', 'Deployment guide', 'User documentation'],
                    'activities': ['Production deployment', 'System configuration', 'User training']
                },
                {
                    'name': 'Maintenance',
                    'typical_percentage': 5,
                    'description': 'Ongoing maintenance and support planning',
                    'deliverables': ['Maintenance plan', 'Support documentation', 'Handover'],
                    'activities': ['Support planning', 'Documentation handover', 'Team transition']
                }
            ]
        }
    
    @staticmethod
    def get_devops_template() -> Dict[str, Any]:
        """Get DevOps-focused SDLC template"""
        return {
            'methodology': 'DevOps',
            'phases': [
                {
                    'name': 'Planning & Infrastructure Setup',
                    'typical_percentage': 15,
                    'description': 'Project planning with emphasis on CI/CD pipeline setup',
                    'deliverables': ['Project plan', 'CI/CD pipeline', 'Infrastructure as code'],
                    'activities': ['Pipeline setup', 'Infrastructure planning', 'Tool configuration']
                },
                {
                    'name': 'Development & Continuous Integration',
                    'typical_percentage': 40,
                    'description': 'Development with continuous integration and automated testing',
                    'deliverables': ['Working features', 'Automated tests', 'Code quality reports'],
                    'activities': ['Feature development', 'Automated testing', 'Code integration']
                },
                {
                    'name': 'Testing & Quality Assurance',
                    'typical_percentage': 20,
                    'description': 'Comprehensive testing with automation focus',
                    'deliverables': ['Test automation suite', 'Quality reports', 'Performance tests'],
                    'activities': ['Test automation', 'Performance testing', 'Security testing']
                },
                {
                    'name': 'Continuous Deployment',
                    'typical_percentage': 15,
                    'description': 'Automated deployment and release management',
                    'deliverables': ['Deployment scripts', 'Release pipeline', 'Monitoring setup'],
                    'activities': ['Deployment automation', 'Release management', 'Monitoring setup']
                },
                {
                    'name': 'Monitoring & Operations',
                    'typical_percentage': 10,
                    'description': 'Production monitoring and operational support',
                    'deliverables': ['Monitoring dashboards', 'Alerting system', 'Operations runbook'],
                    'activities': ['Monitoring setup', 'Alerting configuration', 'Operations planning']
                }
            ]
        }
    
    @staticmethod
    def get_template_by_methodology(methodology: str) -> Dict[str, Any]:
        """Get template based on methodology name"""
        templates = {
            'Agile': SDLCTemplates.get_agile_template(),
            'Waterfall': SDLCTemplates.get_waterfall_template(),
            'DevOps-focused': SDLCTemplates.get_devops_template()
        }
        
        return templates.get(methodology, SDLCTemplates.get_agile_template())
    
    @staticmethod
    def get_project_type_adjustments() -> Dict[str, Dict[str, float]]:
        """Get adjustment factors for different project types"""
        return {
            'Web Application': {
                'Requirements & User Stories': 1.2,
                'Development Sprints': 1.1,
                'Testing & Integration': 1.0,
                'Deployment & Release': 0.8
            },
            'Mobile Application': {
                'Requirements & User Stories': 1.3,
                'Development Sprints': 1.2,
                'Testing & Integration': 1.4,
                'Deployment & Release': 1.2
            },
            'API/Backend Service': {
                'Requirements & User Stories': 1.1,
                'Development Sprints': 1.0,
                'Testing & Integration': 1.3,
                'Deployment & Release': 0.9
            },
            'Enterprise Software': {
                'Requirements & User Stories': 1.5,
                'System Design': 1.3,
                'Development Sprints': 1.1,
                'Testing & Integration': 1.2,
                'Deployment & Release': 1.1
            }
        }
    
    @staticmethod
    def get_team_size_factors() -> Dict[str, float]:
        """Get adjustment factors based on team size"""
        return {
            'Small (1-3)': 0.9,  # Smaller teams are more efficient but may take longer
            'Medium (4-8)': 1.0,  # Baseline
            'Large (9-15)': 1.2,  # More coordination overhead
            'Enterprise (15+)': 1.4  # Significant coordination and communication overhead
        }
