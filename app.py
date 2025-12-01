import streamlit as st
import pandas as pd
import plotly.express as px
import json
import re

# Import our OOP modules
from agents import AnalystAgent, ResourceAgent, ArchitectAgent, ProjectManagerAgent

# ==========================================
# 1. SETUP & UTILITIES
# ==========================================
st.set_page_config(page_title="IdeaForge OOP | AI Consultant", page_icon="🛠️", layout="wide")

st.markdown("""
    <style>
    .stButton>button {width: 100%; background-color: #FF4B4B; color: white;}
    </style>
""", unsafe_allow_html=True)

def clean_json_string(json_str):
    """Utility to strip Markdown code fences from LLM output."""
    clean = re.sub(r'```json', '', json_str)
    clean = re.sub(r'```', '', clean)
    return clean.strip()

# ==========================================
# 2. SIDEBAR
# ==========================================
with st.sidebar:
    st.title("IdeaForge 🏗️")
    st.caption("Powered by OOP & Multi-Agent Systems")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Architecture:\n\n`Analyst` -> `Resource` -> `Architect` -> `Manager`")

# ==========================================
# 3. MAIN LOGIC
# ==========================================
st.title("🛠️ IdeaForge: Autonomous Engineering Planner")
user_idea = st.text_area("What do you want to build?", placeholder="e.g. A solar-powered IoT weather station...")

if st.button("🚀 Launch Agent Swarm") and user_idea and api_key:
    
    # Initialize Context
    shared_context = f"USER PROJECT IDEA: {user_idea}"
    
    # Initialize Agents (OOP Instantiation)
    try:
        agent_analyst = AnalystAgent(api_key)
        agent_resource = ResourceAgent(api_key)
        agent_architect = ArchitectAgent(api_key)
        agent_pm = ProjectManagerAgent(api_key)
        
        # Pipeline Execution
        with st.status("Agents are collaborating...", expanded=True) as status:
            
            # Step 1
            st.write("🧠 Analyst is thinking...")
            res_analyst = agent_analyst.execute(shared_context)
            shared_context += f"\n\n--- ANALYST REPORT ---\n{res_analyst}"
            st.markdown(f"**Analyst:** Task Complete.")
            
            # Step 2
            st.write("🔌 Resource Specialist is sourcing...")
            res_resource = agent_resource.execute(shared_context)
            shared_context += f"\n\n--- RESOURCE REPORT ---\n{res_resource}"
            st.markdown(f"**Resource Specialist:** Task Complete.")

            # Step 3
            st.write("🏗️ Architect is designing...")
            res_architect = agent_architect.execute(shared_context)
            shared_context += f"\n\n--- ARCHITECT REPORT ---\n{res_architect}"
            st.markdown(f"**Architect:** Task Complete.")

            # Step 4
            st.write("📅 Project Manager is scheduling...")
            res_pm = agent_pm.execute(shared_context)
            st.markdown(f"**Project Manager:** Task Complete.")
            
            status.update(label="Blueprint Generated Successfully!", state="complete", expanded=False)

        # ==========================================
        # 4. RENDERING RESULTS
        # ==========================================
        st.divider()
        
        # Textual Reports in Tabs
        tab1, tab2, tab3 = st.tabs(["🧠 Analysis", "🔌 Hardware", "🏗️ Software"])
        with tab1: st.markdown(res_analyst)
        with tab2: st.markdown(res_resource)
        with tab3: st.markdown(res_architect)

        # Visualization (Gantt Chart)
        st.subheader("📅 Execution Timeline")
        try:
            clean_json = clean_json_string(res_pm)
            data = json.loads(clean_json)
            df = pd.DataFrame(data)
            
            # Create Gantt
            fig = px.timeline(df, x_start="Start_Week", x_end="End_Week", y="Task", color="Phase")
            fig.layout.xaxis.type = 'linear'
            fig.data[0].x = df.End_Week - df.Start_Week
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Visualization Error: {e}")
            with st.expander("Debug Raw JSON"):
                st.code(res_pm)

    except Exception as e:
        st.error(f"Initialization Error: {e}")

elif not api_key:
    st.warning("Please enter your API Key to proceed.")