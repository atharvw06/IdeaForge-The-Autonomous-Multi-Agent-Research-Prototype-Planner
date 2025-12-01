# IdeaForge 🛠️

<img width="1920" height="768" alt="Gemini_Generated_Image_onjoyeonjoyeonjo" src="https://github.com/user-attachments/assets/06fd08cc-40ca-4e20-adb0-2efcc37e3a2c" />


###  The Autonomous Multi-Agent Research & Prototype Planner

**IdeaForge bridges the "Implementation Gap" between a high-level napkin sketch and a concrete execution plan.**

---

## 🛑 The Problem

For engineers, researchers, and students, the biggest hurdle isn't writing code—it's **planning**. 
There is a daunting chasm between having an idea (e.g., *"I want to build an autonomous underwater drone with sensor fusion"*) and knowing exactly:
1.  Which specific hardware to buy (BOM).
2.  How to wire and architect the system.
3.  How long it will realistically take to build.

<img width="999" height="536" alt="Screenshot 2025-12-01 212434_processed_by_imagy" src="https://github.com/user-attachments/assets/07f6d907-d36b-4cb2-a263-9725f62eb5c1" />


Most ideas stall at the "Feasibility Phase" because the domain knowledge required is too scattered.


## 🚀 The Solution
IdeaForge is an **autonomous multi-agent system** that acts as a "Consultancy Firm in a Box." You provide the raw idea, and our system spins up a dedicated team of specialized AI agents to validate feasibility, source parts, and design the architecture.



## 🤖 Meet Your Dedicated Team

IdeaForge employs a **Directed Acyclic Graph (DAG)** of four specialized agents, working sequentially to refine your project:

1.  **🧠 The Analyst (Domain Expert)**
    *   Decomposes the vague prompt into core engineering domains (Robotics, Computer Vision, Embedded Systems).
    *   Identifies technical constraints and bottlenecks before you even start.


2.  **🔌 The Resource Agent (Procurement)**
    *   **Bill of Materials (BOM):** Selects specific, compatible hardware (e.g., *Jetson Nano 4GB* over *Raspberry Pi* for AI workloads).
    *   Checks for voltage compatibility, I/O constraints, and compute requirements.


3.  **🏗️ The Architect (Software CTO)**
    *   Designs the complete software stack (Language, Frameworks, Libraries).
    *   Generates a professional **File Directory Structure** tailored to the hardware.
    *   Maps the data flow from sensors to processing to user interface.


4.  **📅 The Project Manager (Planner)**
    *   Synthesizes all technical requirements into a realistic timeline.
    *   **Output:** An interactive **Gantt Chart** visualization estimating phases for Procurement, Dev, Testing, and Deployment.

---


## ✨ Key Features
*   **Chain-of-Thought Reasoning:** Our agents don't just guess; they explain *why* they made specific choices (e.g., explaining why an LSTM model is better than a vanilla RNN for your specific sensor data).
*   **Context Awareness:** Information flows seamlessly from one agent to the next. The *Architect* knows what hardware the *Resource Agent* picked.
*   **Visual Roadmap:** Automatically generates an interactive project timeline using Plotly.
*   **Structured Deliverables:**
    *   ✅ Markdown BOM Table
    *   ✅ Software Stack Diagram
    *   ✅ Codebase File Tree
    *   ✅ Execution Timeline

---


## 🛠️ Installation & Usage

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/atharvw06/IdeaForge-The-Autonomous-Multi-Agent-Research-Prototype-Planner.git
    cd ideaforge
    ```


2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```


3.  **Run the Application**
    ```bash
    streamlit run app.py
    ```


4.  **Start Planning**
    *   Enter your Google Gemini API Key in the sidebar.
    *   Type your project idea (e.g., *"A smart vertical farming system using IoT and LoRaWAN"*).
    *   Watch the agents collaborate to build your blueprint.

---


## 🧠 Powered By
*   **Google Gemini :** For massive context windows and reasoning capabilities.
*   **Streamlit:** For the interactive frontend.
*   **Plotly:** For dynamic data visualization.


---
<img width="1524" height="803" alt="Screenshot 2025-12-01 230901" src="https://github.com/user-attachments/assets/87422b24-2725-4883-ad73-478b85be418d" />

> *"IdeaForge is meta-innovation: a tool built to help build other tools."*
