# SmartNavigatorAI

A Streamlit web app that uses IBM Watsonx AI to generate Software Development Lifecycle (SDLC) breakdowns for projects. Supports Agile, Waterfall, Hybrid, and DevOps methodologies with in-memory storage, visualizations, and export options.

## Prerequisites

- Python 3.11 or 3.12  
- PDM (`pip install pdm`)  
- IBM Watsonx AI API key and project ID  
- Git  

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/SmartNavigatorAI.git
cd SmartNavigatorAI
```

### 2. Install Dependencies

```bash
pdm install
```

### 3. Configure IBM Watsonx AI

Set environment variables (PowerShell):

```powershell
$env:IBM_API_KEY = "your_api_key"
$env:IBM_PROJECT_ID = "your_project_id"
```

Or create a `.env` file:

```env
IBM_API_KEY=your_api_key
IBM_PROJECT_ID=your_project_id
```

## Running the App

Activate virtual environment:

```powershell
.\.venv\Scripts\activate
```

Start Streamlit:

```powershell
pdm run streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

## Usage

On the **New Project** page, enter:

- **Project Name** (e.g., Online Bookstore)  
- **Description** (e.g., Web app with user registration and payment)  
- **Duration** (e.g., 12 weeks)  
- **Team Size**, **Project Type**, **Methodology**  

Click **"Generate SDLC Breakdown"** to view phases, charts, and export options.  
Check **"Project History"** for past projects.  
View **"Analytics"** for project trends.
