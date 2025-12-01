import streamlit as st
import pandas as pd
import plotly.express as px
import json
import re
import time

# Import our OOP Agent modules
# Ensure agents.py is in the same directory!
from agents import AnalystAgent, ResourceAgent, ArchitectAgent, ProjectManagerAgent

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="IdeaForge | Autonomous Engineering Planner",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a Professional Hackathon UI
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
    }
    .stButton>button {
        width: 100%;
        background-color: #0E1117;
        color: white;
        border-radius: 8px;
        height: 50px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF4B4B;
        border: none;
    }
    h1 {
        color: #0E1117;
    }
    .agent-card {
        padding: 15px;
        border-radius: 10px;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def clean_json_string(json_str):
    """
    Sanitizes LLM output to ensure valid JSON parsing.
    Removes markdown code fences (```json ... ```).
    """
    clean = re.sub(r'```json', '', json_str)
    clean = re.sub(r'```', '', clean)
    return clean.strip()

# ==========================================
# 3. SIDEBAR: SETTINGS & INPUTS
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8637/8637099.png", width=80)
    st.title("IdeaForge 🛠️")
    st.markdown("**Autonomous Project Planner**")
    st.markdown("---")
    
    # --- FIXED: MANUAL KEY INPUT ONLY ---
    api_key = st.text_input("Enter Gemini API Key", type="password", help="Get one at aistudio.google.com")
    # ------------------------------------
    
    st.markdown("---")
    st.info("""
    **Architecture:**
    1. 🧠 **Analyst:** Domain Logic
    2. 🔌 **Resource:** Hardware BOM
    3. 🏗️ **Architect:** Software Stack
    4. 📅 **Manager:** Timeline & Gantt
    """)
    st.markdown("---")
    st.caption("v2.1 | Hackathon Build")

# ==========================================
# 4. MAIN INTERFACE
# ==========================================
st.title("From Idea to Execution 🚀")
st.markdown("##### *Describe your engineering concept, and our AI Agent Swarm will build the blueprint.*")

col1, col2 = st.columns([3, 1])
with col1:
    user_idea = st.text_area(
        "Project Description",
        placeholder="e.g., An autonomous drone that uses thermal imaging to detect forest fires and report coordinates via LoRaWAN.",
        height=120,
        label_visibility="collapsed"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True) # Spacer
    start_btn = st.button("🚀 Initialize Agents")

# ==========================================
# 5. AGENT ORCHESTRATION LOGIC
# ==========================================
if start_btn and user_idea and api_key:
    
    # 1. Initialize Context
    shared_context = f"USER PROJECT IDEA: {user_idea}"
    
    # 2. Instantiate Agents (OOP)
    try:
        agent_analyst = AnalystAgent(api_key)
        agent_resource = ResourceAgent(api_key)
        agent_architect = ArchitectAgent(api_key)
        agent_pm = ProjectManagerAgent(api_key)
        
        # 3. Execution Pipeline with Visual Feedback
        with st.status("🤖 **Agent Swarm is Active...**", expanded=True) as status:
            
            # --- PHASE 1: ANALYST ---
            st.write("🧠 **Analyst Agent:** Decomposing requirements...")
            start_time = time.time()
            res_analyst = agent_analyst.execute(shared_context)
            shared_context += f"\n\n--- ANALYST REPORT ---\n{res_analyst}"
            st.markdown(f"*Analyst finished in {round(time.time()-start_time, 2)}s*")
            
            # --- PHASE 2: RESOURCE ---
            st.write("🔌 **Resource Agent:** Sourcing hardware components...")
            res_resource = agent_resource.execute(shared_context)
            shared_context += f"\n\n--- RESOURCE REPORT ---\n{res_resource}"
            st.markdown(f"*Procurement finished.*")

            # --- PHASE 3: ARCHITECT ---
            st.write("🏗️ **Architect Agent:** Designing software stack...")
            res_architect = agent_architect.execute(shared_context)
            shared_context += f"\n\n--- ARCHITECT REPORT ---\n{res_architect}"
            st.markdown(f"*Architecture design finished.*")

            # --- PHASE 4: PROJECT MANAGER ---
            st.write("📅 **Project Manager:** Calculating Gantt timeline...")
            res_pm = agent_pm.execute(shared_context)
            
            status.update(label="✅ Blueprint Generated Successfully!", state="complete", expanded=False)

        # ==========================================
        # 6. RESULTS DISPLAY (TABS)
        # ==========================================
        st.divider()
        st.subheader("📂 Project Deliverables")
        
        tab_analysis, tab_bom, tab_code, tab_timeline = st.tabs([
            "🧠 System Analysis", 
            "🔌 Bill of Materials", 
            "🏗️ Software Arch",
            "📅 Master Schedule"
        ])

        with tab_analysis:
            st.markdown(res_analyst)

        with tab_bom:
            st.markdown(res_resource)
            st.info("💡 Pro Tip: Check voltage compatibility between the selected Controller and Sensors.")

        with tab_code:
            st.markdown(res_architect)

        # ==========================================
        # 7. FIXED GANTT CHART VISUALIZATION
        # ==========================================
        with tab_timeline:
            try:
                # A. Parse JSON
                clean_json = clean_json_string(res_pm)
                data = json.loads(clean_json)
                df = pd.DataFrame(data)
                
                # B. Data Processing for Waterfall Effect
                # Calculate Duration for Plotly linear mode
                df['Duration'] = df['End_Week'] - df['Start_Week']
                
                # Sort by Start Week to ensure "Waterfall" visual flow
                df = df.sort_values(by="Start_Week", ascending=True)
                
                # C. Generate Chart
                fig = px.timeline(
                    df, 
                    x_start="Start_Week", 
                    x_end="End_Week", 
                    y="Task", 
                    color="Phase",
                    hover_data=["Duration", "Phase"],
                    title="<b>End-to-End Execution Roadmap</b>",
                    color_discrete_sequence=px.colors.qualitative.Prism, # Professional color scheme
                    height=600  # Taller for better readability
                )
                
                # D. Custom Layout Updates
                fig.update_layout(
                    xaxis_title="<b>Project Timeline (Weeks)</b>",
                    yaxis_title="",
                    showlegend=True,
                    legend=dict(orientation="h", y=1.1), # Legend on top
                    plot_bgcolor='rgba(0,0,0,0)', # Transparent background
                    xaxis=dict(
                        tickmode='linear',
                        tick0=1,
                        dtick=1,
                        showgrid=True,
                        gridcolor='#eee'
                    )
                )
                
                # E. CRITICAL FIXES FOR VISUALIZATION
                # 1. Reverse Y-axis so Week 1 tasks are at the TOP
                fig.update_yaxes(autorange="reversed")
                
                # 2. Fix X-axis type (Integers vs Dates quirk in Plotly)
                fig.layout.xaxis.type = 'linear'
                
                # 3. Explicitly map data widths to avoid rendering bugs
                for d in fig.data:
                    filt = df['Phase'] == d.name
                    d.x = df[filt]['Duration'].tolist()

                st.plotly_chart(fig, use_container_width=True)
                
                # Data Table for detail view
                with st.expander("View Raw Schedule Data"):
                    st.dataframe(df[['Phase', 'Task', 'Start_Week', 'End_Week']])

            except Exception as e:
                st.error("⚠️ Visualizer Error: The Project Manager Agent produced invalid JSON.")
                st.error(f"Debug Info: {e}")
                with st.expander("Raw Output Debug"):
                    st.code(res_pm)

    except Exception as e:
        st.error(f"❌ System Error: {str(e)}")
        st.warning("Please ensure your API Key is correct and you have internet access.")

elif start_btn and not api_key:
    st.warning("⚠️ Access Denied: Please provide a valid Gemini API Key in the sidebar.")