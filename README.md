SmartNavigatorAI
SmartNavigatorAI is an AI-powered web application built with Streamlit that helps users plan Software Development Lifecycle (SDLC) phases for their projects. By leveraging IBM Watsonx AI's Granite model, it generates detailed SDLC breakdowns based on project details, including phase durations, deliverables, and activities. The app supports Agile, Waterfall, Hybrid, and DevOps-focused methodologies, with visualizations and export options (JSON, CSV, Markdown). Project data is stored in memory during the session, making it lightweight and database-free.
Features

AI-Driven SDLC Planning: Generate customized SDLC breakdowns using IBM Watsonx AI.
Interactive UI: Input project details via a Streamlit form and view results with Plotly charts.
In-Memory State Management: Store project data during the session without a database.
Project History: View and search past projects submitted in the current session.
Analytics Dashboard: Visualize project types, methodologies, and durations.
Export Options: Download SDLC breakdowns as JSON, CSV, or Markdown.
Methodology Support: Agile, Waterfall, Hybrid, and DevOps-focused workflows.

Prerequisites

Python: Version 3.11 or 3.12 (as specified in pyproject.toml).
PDM: Package and dependency manager for Python (install via pip install pdm).
IBM Watsonx AI Credentials:
An IBM Cloud account with access to Watsonx AI.
API key and project ID for the ibm/granite-3-8b-instruct model.


Git: For cloning the repository.
A modern web browser (e.g., Chrome, Firefox) to view the Streamlit app.

Installation
1. Clone the Repository
Clone the SmartNavigatorAI repository to your local machine using Git:
git clone https://github.com/your-username/SmartNavigatorAI.git
cd SmartNavigatorAI

Replace https://github.com/your-username/SmartNavigatorAI.git with the actual repository URL.
2. Set Up Python Environment
Ensure Python 3.11 or 3.12 is installed. You can check your Python version with:
python --version

Install PDM if not already installed:
pip install pdm

3. Install Dependencies
Use PDM to install the project dependencies specified in pyproject.toml:
pdm install

This sets up a virtual environment and installs required packages, including:

streamlit>=1.45.1
ibm-watsonx-ai>=1.3.24
pandas>=0.24.2,<2.3.0
plotly>=6.1.2
requests>=2.32.3

4. Configure IBM Watsonx AI Credentials
The app requires an IBM Watsonx AI API key and project ID to access the Granite model. Set these as environment variables:
On Windows (PowerShell):
$env:IBM_API_KEY = "your_actual_api_key"
$env:IBM_PROJECT_ID = "your_actual_project_id"

Alternatively, Use a .env File:
Create a .env file in the project root:
IBM_API_KEY=your_actual_api_key
IBM_PROJECT_ID=your_actual_project_id

The app automatically loads these variables using python-dotenv.
To obtain credentials:

Sign in to IBM Cloud.
Navigate to Watsonx AI and create a project.
Generate an API key and note the project ID.

Running the Project

Activate the Virtual Environment:PDM creates a virtual environment automatically. Activate it:
.\.venv\Scripts\activate


Run the Streamlit App:Start the Streamlit server:
pdm run streamlit run app.py


Access the App:Open your browser and navigate to http://localhost:8501. The SmartNavigatorAI interface should load, displaying the "New Project" page.


Usage

Create a New Project:

On the "New Project" page, fill out the form:
Project Name: e.g., Online Bookstore
Project Description: Provide details like features, tech stack, and complexity.
Total Project Duration: Select a duration (e.g., 12 weeks).
Team Size: Choose from Small, Medium, Large, or Enterprise.
Project Type: Select Web Application, Mobile Application, etc.
Preferred Methodology: Choose Agile, Waterfall, Hybrid, or DevOps-focused.


Click "Generate SDLC Breakdown" to create an AI-powered SDLC plan.


View Results:

The breakdown appears on the right, with phase cards, a pie chart, a timeline, and detailed phase information.
Export the breakdown as JSON, CSV, or Markdown, or copy a summary.


Project History:

Navigate to "Project History" in the sidebar to view all projects created in the session.
Search projects by name or description and view their SDLC breakdowns.


Analytics:

Go to "Analytics" to see metrics and charts for project types, methodologies, and durations based on in-memory data.



Note: Project data is stored in memory (st.session_state) and is cleared when the app is closed or the session ends.
Example Test Case
To test the app:

Run the app as described above.
Create a project:
Project Name: Online Bookstore
Project Description: A web-based bookstore with user registration, book catalog, and payment integration. Uses Python, Django, and React. Medium complexity.
Duration: 12 weeks
Team Size: Medium (4-8)
Project Type: Web Application
Methodology: Agile


Submit the form and verify the SDLC breakdown.
Check "Project History" to see the project listed.
View "Analytics" to confirm metrics and charts.

Troubleshooting

AI Service Not Configured:
Ensure IBM_API_KEY and IBM_PROJECT_ID are set correctly.
Verify access to the ibm/granite-3-8b-instruct model in IBM Watsonx AI.


Dependency Issues:
Run pdm install to ensure all packages are installed.
Check Python version (python --version) is 3.11 or 3.12.


Streamlit Not Loading:
Confirm the server is running (http://localhost:8501).
Check for errors in the terminal and resolve missing dependencies.


Invalid JSON Response:
If the AI generates non-JSON output, check services/ai_service.py and utils/sdlc_parser.py for parsing issues.



Project Structure
SmartNavigatorAI/
├── app.py                  # Main Streamlit application
├── pyproject.toml          # PDM configuration and dependencies
├── .env                    # Environment variables (optional)
├── services/
│   └── ai_service.py       # IBM Watsonx AI integration
├── utils/
│   ├── sdlc_parser.py      # Parses AI-generated SDLC responses
│   └── export_utils.py     # Handles export to JSON, CSV, Markdown
├── data/
│   └── sdlc_templates.py   # SDLC templates (if used)
└── README.md               # This file

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions or support, contact [your-email@example.com] or open an issue on the repository.
