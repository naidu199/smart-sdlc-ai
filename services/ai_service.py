import requests
import json
import os
from typing import Dict, Any, Optional

class AIService:
    """Service class for interacting with IBM Granite AI model"""
    
    def __init__(self):
        self.url = "https://eu-gb.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29"
        self.access_token = os.getenv("IBM_ACCESS_TOKEN")
        self.project_id = os.getenv("IBM_PROJECT_ID", "08334910-e7ec-4e32-990d-be70ab4159ad")
        self.model_id = "ibm/granite-3-8b-instruct"
        
    def is_configured(self) -> bool:
        """Check if the AI service is properly configured"""
        return bool(self.access_token and self.project_id and self.access_token != "YOUR_ACCESS_TOKEN")
    
    def generate_sdlc_breakdown(self, project_data: Dict[str, Any]) -> str:
        """Generate SDLC breakdown using IBM Granite model"""
        
        if not self.is_configured():
            raise Exception("AI service not configured. Please set IBM_ACCESS_TOKEN and IBM_PROJECT_ID environment variables.")
        
        # Construct the AI prompt
        prompt = self._construct_sdlc_prompt(project_data)
        
        body = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are Granite, an AI language model developed by IBM in 2024. You are an expert software project manager and SDLC consultant with deep knowledge of software development methodologies, project planning, and time estimation. You provide detailed, structured, and practical SDLC breakdowns."
                },
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }
            ],
            "project_id": self.project_id,
            "model_id": self.model_id,
            "frequency_penalty": 0,
            "max_tokens": 2000,
            "presence_penalty": 0,
            "temperature": 0.3,  # Lower temperature for more consistent results
            "top_p": 0.9
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.post(self.url, headers=headers, json=body, timeout=30)
            
            if response.status_code != 200:
                raise Exception(f"API request failed with status {response.status_code}: {response.text}")
            
            data = response.json()
            
            # Extract the AI response
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content']
            else:
                raise Exception("Invalid response format from AI service")
                
        except requests.exceptions.Timeout:
            raise Exception("AI service request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error when contacting AI service: {str(e)}")
        except Exception as e:
            raise Exception(f"Error generating SDLC breakdown: {str(e)}")
    
    def _construct_sdlc_prompt(self, project_data: Dict[str, Any]) -> str:
        """Construct a detailed prompt for SDLC breakdown generation"""
        
        prompt = f"""
As an expert software project manager, analyze the following project and create a detailed Software Development Lifecycle (SDLC) breakdown:

PROJECT DETAILS:
- Project Name: {project_data['name']}
- Description: {project_data['description']}
- Total Duration: {project_data['duration_weeks']} weeks
- Team Size: {project_data['team_size']}
- Project Type: {project_data['project_type']}
- Methodology: {project_data['methodology']}

REQUIREMENTS:
1. Break down the project into appropriate SDLC phases based on the methodology
2. Allocate time (in weeks and percentages) for each phase
3. Ensure the total time equals exactly {project_data['duration_weeks']} weeks
4. Consider the project complexity, team size, and project type
5. Provide realistic time distributions based on industry best practices

RESPONSE FORMAT (JSON):
{{
    "project_summary": {{
        "name": "{project_data['name']}",
        "total_duration_weeks": {project_data['duration_weeks']},
        "methodology": "{project_data['methodology']}",
        "complexity_assessment": "High/Medium/Low based on description"
    }},
    "phases": [
        {{
            "name": "Phase Name",
            "duration_weeks": number,
            "percentage": percentage_of_total,
            "description": "Detailed description of what happens in this phase",
            "deliverables": ["List", "of", "key", "deliverables"],
            "activities": ["Main", "activities", "and", "tasks"],
            "team_focus": "Primary team focus area"
        }}
    ],
    "recommendations": [
        "Key recommendation 1",
        "Key recommendation 2"
    ]
}}

GUIDELINES:
- For Agile: Include Sprint Planning, Development Sprints, Testing, Deployment phases
- For Waterfall: Include Requirements, Design, Implementation, Testing, Deployment, Maintenance
- For Hybrid: Combine elements appropriately
- Consider project type complexity (Web apps need more frontend work, APIs need more backend focus)
- Adjust phase durations based on team size (larger teams may need more coordination time)
- Include buffer time for complex projects
- Make recommendations specific to the project context

Please provide ONLY the JSON response, no additional text or formatting.
"""
        return prompt
