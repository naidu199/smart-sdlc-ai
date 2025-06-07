from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
import os
from typing import Dict, Any, Optional

class AIService:
    """Service class for interacting with IBM Granite AI model using ibm-watsonx-ai library"""

    def __init__(self):
        self.url = "https://eu-gb.ml.cloud.ibm.com"
        self.api_key = os.getenv("IBM_API_KEY", "gVlNnx0CgD8YMT813nCKEgYlkux2Grh7sN2K2dI0XKQK")
        self.project_id = os.getenv("IBM_PROJECT_ID", "08334910-e7ec-4e32-990d-be70ab4159ad")
        self.model_id = "ibm/granite-3-8b-instruct"

        # Initialize API client
        credentials = {
            "apikey": self.api_key,
            "url": self.url
        }
        self.client = APIClient(credentials)
        self.client.set.default_project(self.project_id)

        # Initialize model
        self.parameters = {
            GenParams.DECODING_METHOD: "greedy",  # Matches frequency_penalty=0 and presence_penalty=0
            GenParams.MAX_NEW_TOKENS: 2000,
            GenParams.TEMPERATURE: 0.3,  # Matches original temperature
            GenParams.TOP_P: 0.9,       # Matches original top_p
            GenParams.STOP_SEQUENCES: []
        }
        self.model = ModelInference(
            model_id=self.model_id,
            api_client=self.client,
            project_id=self.project_id,
            params=self.parameters
        )

    def is_configured(self) -> bool:
        """Check if the AI service is properly configured"""
        return bool(self.api_key and self.project_id and self.api_key != "YOUR_API_KEY")

    def generate_sdlc_breakdown(self, project_data: Dict[str, Any]) -> str:
        """Generate SDLC breakdown using IBM Granite model"""

        if not self.is_configured():
            raise Exception("AI service not configured. Please set IBM_API_KEY and IBM_PROJECT_ID environment variables.")

        # Construct the AI prompt
        system_prompt = (
            "You are Granite, an AI language model developed by IBM in 2024. "
            "You are an expert software project manager and SDLC consultant with deep knowledge of software development methodologies, project planning, and time estimation. "
            "You provide detailed, structured, and practical SDLC breakdowns."
        )
        user_prompt = self._construct_sdlc_prompt(project_data)

        try:
            # Generate response
            response = self.model.generate_text(
                prompt=f"{system_prompt}\n\n{user_prompt}"
            )
            # print(f"Generated response: {response}")
            return response
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

# Example usage
if __name__ == "__main__":
    project_data = {
        "name": "Task Management App",
        "description": "A web-based task management application with user authentication and task tracking",
        "duration_weeks": 10,
        "team_size": 5,
        "project_type": "Web Application",
        "methodology": "Agile"
    }

    ai_service = AIService()
    try:
        print("\n📦 SDLC Breakdown:")
        result = ai_service.generate_sdlc_breakdown(project_data)
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}")
