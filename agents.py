import google.generativeai as genai
from abc import ABC, abstractmethod

class IdeaForgeAgent(ABC):
    """
    Abstract Base Class for all IdeaForge Agents.
    Enforces a standard interface for execution.
    """
    def __init__(self, api_key, model_name="gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self.name = "Generic Agent"
        
        if not api_key:
            raise ValueError("API Key is required to initialize an agent.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def _get_common_instruction(self):
        """Global system prompt injection for consistency."""
        return "CRITICAL: You are an expert engineering consultant. Use CHAIN OF THOUGHT reasoning."

    @abstractmethod
    def construct_prompt(self, context_history):
        """Each subclass must define how it constructs its prompt."""
        pass

    def execute(self, context_history):
        """The main method to run the agent."""
        prompt = self.construct_prompt(context_history)
        full_instruction = f"{self._get_common_instruction()}\n\n{prompt}"
        
        try:
            response = self.model.generate_content(full_instruction)
            return response.text
        except Exception as e:
            return f"Error executing {self.name}: {str(e)}"

# ==========================================
# CONCRETE AGENT IMPLEMENTATIONS
# ==========================================

class AnalystAgent(IdeaForgeAgent):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "Analyst"

    def construct_prompt(self, context_history):
        return f"""
        {context_history}
        
        ROLE: Senior Systems Analyst.
        TASK: Analyze the user's project idea.
        OUTPUT REQUIREMENTS:
        1. Identify the 'Core Domain' (e.g., Robotics, IoT).
        2. List specific 'Hardware Requirements' (Sensors, Actuators).
        3. List specific 'Software Requirements' (Processing, Storage).
        
        Start your response with "## Reasoning" then provide "## Analysis".
        """

class ResourceAgent(IdeaForgeAgent):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "Resource Specialist"

    def construct_prompt(self, context_history):
        return f"""
        {context_history}
        
        ROLE: Hardware Procurement Specialist.
        TASK: Create a Bill of Materials (BOM) based on the Analyst's report.
        OUTPUT REQUIREMENTS:
        1. Suggest specific components (e.g., 'Raspberry Pi 4 8GB' vs 'Arduino Uno').
        2. Verify compatibility (Voltage, I/O pins, Compute).
        3. Output a Markdown Table: [Component, Purpose, Estimated Cost, Reason].
        
        Explain why you chose specific parts in a "## Reasoning" section first.
        """

class ArchitectAgent(IdeaForgeAgent):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "Software Architect"

    def construct_prompt(self, context_history):
        return f"""
        {context_history}
        
        ROLE: Chief Software Architect.
        TASK: Design the software stack.
        OUTPUT REQUIREMENTS:
        1. Define the Tech Stack (Languages, Libraries).
        2. Create a File Directory Structure tree.
        3. Explain Data Flow.
        
        Use "## Reasoning" to explain trade-offs (e.g., MQTT vs HTTP).
        """

class ProjectManagerAgent(IdeaForgeAgent):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "Project Manager"

    def construct_prompt(self, context_history):
        return f"""
        {context_history}
        
        ROLE: Technical Project Manager.
        TASK: Create a development timeline.
        
        CRITICAL OUTPUT FORMAT:
        Output ONLY a valid JSON list of objects. NO MARKDOWN. NO EXPLANATIONS.
        Format:
        [
            {{"Phase": "Phase Name", "Task": "Specific Task", "Start_Week": int, "End_Week": int}},
            ...
        ]
        """