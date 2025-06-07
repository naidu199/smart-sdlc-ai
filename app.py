import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
from services.ai_service import AIService
from utils.sdlc_parser import SDLCParser
from utils.export_utils import ExportUtils
from data.sdlc_templates import SDLCTemplates

# Set page config as the FIRST Streamlit command
st.set_page_config(
    page_title="SmartSDLC - AI-Powered SDLC Planning",
    page_icon="🚀",
    layout="wide"
)

# Initialize session state
if 'sdlc_result' not in st.session_state:
    st.session_state.sdlc_result = None
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'projects' not in st.session_state:
    st.session_state.projects = []  # Store project data in memory

def main():
    # Header
    st.title("🚀 SmartSDLC")
    st.markdown("**AI-Powered Software Development Lifecycle Planning**")
    st.markdown("Transform your project ideas into structured SDLC phases with intelligent time allocation.")

    # Navigation
    with st.sidebar:
        st.header("🧭 Navigation")
        pages = {
            'home': '🏠 New Project',
            'history': '📋 Project History',
            'analytics': '📊 Analytics'
        }

        for page_key, page_name in pages.items():
            if st.button(page_name, key=f"nav_{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()

        st.divider()

        # API Configuration Check
        ai_service = AIService()
        if ai_service.is_configured():
            st.success("✅ AI Service Connected")
        else:
            st.error("❌ AI Service Not Configured")
            st.info("Please ensure IBM_API_KEY and IBM_PROJECT_ID are set in environment variables.")

    # Page routing
    if st.session_state.current_page == 'home':
        show_new_project_page()
    elif st.session_state.current_page == 'history':
        show_project_history_page()
    elif st.session_state.current_page == 'analytics':
        show_analytics_page()

def show_new_project_page():
    """Display the new project creation page"""

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📝 Project Input")

        # Project input form
        with st.form("project_form"):
            project_name = st.text_input(
                "Project Name",
                placeholder="e.g., E-commerce Mobile App",
                help="Enter a descriptive name for your project"
            )

            project_description = st.text_area(
                "Project Description",
                height=150,
                placeholder="Describe your project in detail including key features, target audience, technology preferences, complexity level, and any specific requirements...",
                help="The more detailed your description, the better the AI can tailor the SDLC phases"
            )

            col_duration, col_team = st.columns(2)
            with col_duration:
                total_duration = st.selectbox(
                    "Total Project Duration (weeks)",
                    options=[4, 6, 8, 10, 12, 16, 20, 24, 28, 32, 36, 48, 52],
                    index=4,  # Default to 12 weeks
                    help="Select the total duration for your project"
                )

            with col_team:
                team_size = st.selectbox(
                    "Team Size",
                    options=["Small (1-3)", "Medium (4-8)", "Large (9-15)", "Enterprise (15+)"],
                    index=1,
                    help="Approximate size of your development team"
                )

            project_type = st.selectbox(
                "Project Type",
                options=[
                    "Web Application",
                    "Mobile Application",
                    "Desktop Software",
                    "API/Backend Service",
                    "Data Analytics Platform",
                    "E-commerce Platform",
                    "Enterprise Software",
                    "Game Development",
                    "IoT Application",
                    "Other"
                ],
                help="Select the type that best describes your project"
            )

            methodology = st.selectbox(
                "Preferred Methodology",
                options=["Agile", "Waterfall", "Hybrid", "DevOps-focused"],
                help="Choose your preferred development methodology"
            )

            submitted = st.form_submit_button(
                "🤖 Generate SDLC Breakdown",
                type="primary",
                use_container_width=True
            )

            if submitted:
                if not project_name.strip() or not project_description.strip():
                    st.error("❌ Please provide both project name and description.")
                else:
                    st.session_state.processing = True
                    st.rerun()

    with col2:
        st.header("📋 SDLC Breakdown")

        if st.session_state.processing:
            with st.spinner("🤖 AI is analyzing your project and generating SDLC breakdown..."):
                try:
                    # Prepare project data
                    project_data = {
                        'name': project_name,
                        'description': project_description,
                        'duration_weeks': total_duration,
                        'team_size': team_size,
                        'project_type': project_type,
                        'methodology': methodology,
                        'created_at': pd.Timestamp.now()  # Store creation timestamp
                    }

                    # Generate SDLC breakdown using AI
                    ai_service = AIService()
                    ai_response = ai_service.generate_sdlc_breakdown(project_data)

                    # Parse the AI response
                    parser = SDLCParser()
                    parsed_result = parser.parse_ai_response(ai_response, total_duration)

                    # Store in session state for display
                    st.session_state.sdlc_result = parsed_result

                    # Store project and breakdown in session state
                    project_data['sdlc_result'] = parsed_result
                    project_data['id'] = len(st.session_state.projects) + 1  # Simple ID for in-memory storage
                    st.session_state.projects.append(project_data)

                    st.session_state.processing = False
                    st.success("✅ SDLC breakdown generated and stored successfully!")
                    st.rerun()

                except Exception as e:
                    st.session_state.processing = False
                    st.error(f"❌ Error generating SDLC breakdown: {str(e)}")
                    st.info("Please check your API configuration and try again.")

        elif st.session_state.sdlc_result:
            display_sdlc_results(st.session_state.sdlc_result)

        else:
            # Show example or instructions
            st.info("👆 Fill out the project details on the left to generate your AI-powered SDLC breakdown.")

            with st.expander("📖 How SmartSDLC Works"):
                st.markdown("""
                **SmartSDLC** uses advanced AI to analyze your project requirements and generate a customized SDLC breakdown:

                1. **Input Analysis**: AI examines your project description, duration, team size, and type
                2. **Phase Generation**: Creates appropriate SDLC phases based on your methodology preference
                3. **Time Allocation**: Intelligently distributes time across phases based on project complexity
                4. **Deliverable Mapping**: Suggests key deliverables and milestones for each phase
                5. **Visualization**: Presents results in easy-to-understand charts and tables
                """)

            with st.expander("💡 Tips for Better Results"):
                st.markdown("""
                - **Be Specific**: Include technology stack, target platforms, and key features
                - **Mention Complexity**: Describe integration requirements, scalability needs
                - **Include Constraints**: Timeline pressures, budget limitations, compliance requirements
                - **Team Context**: Experience level, distributed vs. co-located team
                """)

def show_project_history_page():
    """Display the project history page using in-memory session state"""
    st.header("📋 Project History")

    # Search functionality
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 Search projects", placeholder="Search by name or description...")
    with col2:
        search_button = st.button("Search", use_container_width=True)

    try:
        # Filter projects based on search query
        if search_query and search_button:
            projects = [
                p for p in st.session_state.projects
                if search_query.lower() in p['name'].lower() or search_query.lower() in p['description'].lower()
            ]
        else:
            projects = st.session_state.projects

        if projects:
            st.subheader(f"Found {len(projects)} projects")

            for project in projects:
                with st.expander(f"📁 {project['name']} ({project['project_type']})"):
                    col1, col2, col3 = st.columns([2, 1, 1])

                    with col1:
                        st.markdown(f"**Description:** {project.get('description', 'No description')}")
                        st.markdown(f"**Methodology:** {project['methodology']}")

                    with col2:
                        st.metric("Duration", f"{project['duration_weeks']} weeks")
                        st.metric("Team Size", project['team_size'])

                    with col3:
                        st.markdown(f"**Created:** {project['created_at'].strftime('%Y-%m-%d')}")
                        if project.get('sdlc_result'):
                            st.success("✅ Has SDLC Breakdown")
                            if st.button(f"View Breakdown", key=f"view_{project['id']}"):
                                st.session_state.sdlc_result = project['sdlc_result']
                                st.session_state.current_page = 'home'
                                st.rerun()
                        else:
                            st.warning("⚠️ No Breakdown")
        else:
            st.info("No projects found. Create your first project to get started!")

    except Exception as e:
        st.error(f"Error loading project history: {str(e)}")

def show_analytics_page():
    """Display the analytics page using in-memory session state"""
    st.header("📊 Analytics Dashboard")

    try:
        # Mock analytics data from session state
        total_projects = len(st.session_state.projects)
        total_breakdowns = sum(1 for p in st.session_state.projects if p.get('sdlc_result'))
        project_types = {}
        methodologies = {}
        durations = {}

        for project in st.session_state.projects:
            # Project type distribution
            project_type = project['project_type']
            project_types[project_type] = project_types.get(project_type, 0) + 1

            # Methodology distribution
            methodology = project['methodology']
            methodologies[methodology] = methodologies.get(methodology, 0) + 1

            # Duration by project type
            duration = project['duration_weeks']
            if project_type in durations:
                durations[project_type].append(duration)
            else:
                durations[project_type] = [duration]

        # Calculate average durations
        average_duration_by_type = {
            pt: sum(durations[pt]) / len(durations[pt]) if durations[pt] else 0
            for pt in durations
        }

        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Projects", total_projects)
        with col2:
            st.metric("Total Breakdowns", total_breakdowns)
        with col3:
            completion_rate = (total_breakdowns / total_projects * 100) if total_projects > 0 else 0
            st.metric("Completion Rate", f"{completion_rate:.1f}%")
        with col4:
            st.metric("Active Templates", "4")  # Static for now

        st.divider()

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 Project Types Distribution")
            if project_types:
                type_df = pd.DataFrame(
                    list(project_types.items()),
                    columns=['Project Type', 'Count']
                )
                fig = px.pie(type_df, values='Count', names='Project Type',
                           title="Distribution by Project Type")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No project type data available yet.")

        with col2:
            st.subheader("🔄 Methodology Preferences")
            if methodologies:
                method_df = pd.DataFrame(
                    list(methodologies.items()),
                    columns=['Methodology', 'Count']
                )
                fig = px.bar(method_df, x='Methodology', y='Count',
                           title="Methodology Usage")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No methodology data available yet.")

        # Duration analysis
        st.subheader("⏱️ Average Duration by Project Type")
        if average_duration_by_type:
            duration_df = pd.DataFrame(
                list(average_duration_by_type.items()),
                columns=['Project Type', 'Average Duration (weeks)']
            )
            fig = px.bar(duration_df, x='Project Type', y='Average Duration (weeks)',
                       title="Average Project Duration by Type")
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No duration data available yet.")

    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")

def display_sdlc_results(sdlc_result):
    """Display the SDLC breakdown results with visualizations"""

    phases = sdlc_result.get('phases', [])
    if not phases:
        st.warning("No phases were generated. Please try again with a more detailed project description.")
        return

    # Phase Overview Cards
    st.subheader("📊 Phase Overview")

    # Create metrics for each phase
    cols = st.columns(min(len(phases), 4))
    for i, phase in enumerate(phases):
        with cols[i % 4]:
            st.metric(
                phase['name'],
                f"{phase['duration_weeks']} weeks",
                f"{phase['percentage']:.1f}%"
            )

    # Time Distribution Chart
    st.subheader("⏱️ Time Distribution")

    # Create pie chart
    fig_pie = px.pie(
        values=[phase['percentage'] for phase in phases],
        names=[phase['name'] for phase in phases],
        title="Phase Time Allocation",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

    # Timeline Chart
    st.subheader("📅 Project Timeline")

    # Create Gantt-like timeline
    timeline_data = []
    current_start = 0

    for phase in phases:
        timeline_data.append({
            'Phase': phase['name'],
            'Start': current_start,
            'Duration': phase['duration_weeks'],
            'End': current_start + phase['duration_weeks']
        })
        current_start += phase['duration_weeks']

    fig_timeline = go.Figure()

    colors = px.colors.qualitative.Set3[:len(phases)]
    for i, data in enumerate(timeline_data):
        fig_timeline.add_trace(go.Bar(
            name=data['Phase'],
            x=[data['Duration']],
            y=[data['Phase']],
            orientation='h',
            marker_color=colors[i],
            text=f"Week {data['Start']+1}-{data['End']}",
            textposition='inside'
        ))

    fig_timeline.update_layout(
        title="Project Timeline (Weeks)",
        xaxis_title="Duration (Weeks)",
        yaxis_title="Phases",
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

    # Detailed Phase Information
    st.subheader("📋 Detailed Phase Breakdown")

    for i, phase in enumerate(phases):
        with st.expander(f"Phase {i+1}: {phase['name']} ({phase['duration_weeks']} weeks)"):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**Description:** {phase['description']}")

                if phase.get('deliverables'):
                    st.markdown("**Key Deliverables:**")
                    for deliverable in phase['deliverables']:
                        st.markdown(f"• {deliverable}")

                if phase.get('activities'):
                    st.markdown("**Main Activities:**")
                    for activity in phase['activities']:
                        st.markdown(f"• {activity}")

            with col2:
                st.metric("Duration", f"{phase['duration_weeks']} weeks")
                st.metric("Time Allocation", f"{phase['percentage']:.1f}%")

                if phase.get('team_focus'):
                    st.markdown(f"**Team Focus:** {phase['team_focus']}")

    # Export Options
    st.subheader("📤 Export Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        export_utils = ExportUtils()
        json_data = export_utils.to_json(sdlc_result)
        st.download_button(
            label="📄 Download JSON",
            data=json_data,
            file_name=f"sdlc_breakdown_{sdlc_result.get('project_name', 'project').replace(' ', '_')}.json",
            mime="application/json"
        )

    with col2:
        csv_data = export_utils.to_csv(sdlc_result)
        st.download_button(
            label="📊 Download CSV",
            data=csv_data,
            file_name=f"sdlc_breakdown_{sdlc_result.get('project_name', 'project').replace(' ', '_')}.csv",
            mime="text/csv"
        )

    with col3:
        markdown_data = export_utils.to_markdown(sdlc_result)
        st.download_button(
            label="📝 Download Markdown",
            data=markdown_data,
            file_name=f"sdlc_breakdown_{sdlc_result.get('project_name', 'project').replace(' ', '_')}.md",
            mime="text/markdown"
        )

    # Action buttons
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Generate New Breakdown", use_container_width=True):
            st.session_state.sdlc_result = None
            st.rerun()

    with col2:
        if st.button("📋 Copy Summary", use_container_width=True):
            summary = export_utils.generate_summary(sdlc_result)
            st.code(summary, language=None)

if __name__ == "__main__":
    main()
