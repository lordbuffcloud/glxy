from crewai import Agent, Crew
from tools.deepinfra_tool import DeepInfraTool
from tools.perplexity_tool import PerplexityTool  # New tool for research
from tools.document_tool import DocumentTool  # New tool for document analysis
from tools.code_tool import CodeTool  # New tool for code execution

# Existing Agents
class VisionaryAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Visionary',
            goal='Handle high-level conceptual tasks and strategy.',
            backstory='You represent the visionary and futuristic thinking of Elon Musk.'
        )
        self._deepinfra_tool = DeepInfraTool()

    def handle_task(self, task_description):
        if "future" in task_description.lower():
            return "I see a future where... (Elon-style speech)"
        return self._deepinfra_tool.generate_text(task_description)


class EngineerAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Engineer',
            goal='Solve technical and engineering problems.',
            backstory='You represent the problem-solving skills and engineering mindset of Elon Musk.'
        )
        self._deepinfra_tool = DeepInfraTool()

    def handle_task(self, task_description):
        if "engineering" in task_description.lower():
            return "Let’s build something amazing! (Elon-style speech)"
        return self._deepinfra_tool.generate_text(task_description)


class EntrepreneurAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Entrepreneur',
            goal='Manage tasks related to business and strategy.',
            backstory='You represent the entrepreneurial spirit of Elon Musk.'
        )
        self._deepinfra_tool = DeepInfraTool()

    def handle_task(self, task_description):
        if "business" in task_description.lower():
            return "Let’s innovate and disrupt industries! (Elon-style speech)"
        return self._deepinfra_tool.generate_text(task_description)

# New Agents
class ResearchAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Researcher',
            goal='Perform deep research using online sources and APIs.',
            backstory='You represent the curiosity and fact-finding nature of a researcher.'
        )
        self._perplexity_tool = PerplexityTool()  # Use the Perplexity API for research

    def handle_task(self, task_description):
        return self._perplexity_tool.perform_research(task_description)


class CodeAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Code Developer',
            goal='Handle code generation and execution tasks.',
            backstory='You represent the coding and automation expertise of a developer.'
        )
        self._code_tool = CodeTool()

    def handle_task(self, task_description):
        return self._code_tool.execute_code(task_description)


class DocumentAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Document Processor',
            goal='Analyze documents using NLP and RAG techniques.',
            backstory='You represent the ability to analyze and retrieve information from documents.'
        )
        self._document_tool = DocumentTool()

    def handle_task(self, task_description):
        return self._document_tool.process_document_for_rag(task_description)

# Modified Crew class to handle task delegation
class Crew:
    def __init__(self, agents):
        self.agents = agents

    def handle_task(self, task_description):
        # Iterate through agents and let them handle tasks they specialize in
        for agent in self.agents:
            response = agent.handle_task(task_description)
            if response:  # If the agent has a valid response, return it
                return response
        return "No agent was able to handle the task."

# Set up the CrewAI system with multiple agents
def setup_crew():
    visionary_agent = VisionaryAgent()
    engineer_agent = EngineerAgent()
    entrepreneur_agent = EntrepreneurAgent()
    research_agent = ResearchAgent()  # New research agent
    code_agent = CodeAgent()  # New code agent
    document_agent = DocumentAgent()  # New document analysis agent

    # Crew setup with multiple agents
    crew = Crew(agents=[
        visionary_agent,
        engineer_agent,
        entrepreneur_agent,
        research_agent,
        code_agent,
        document_agent
    ])
    return crew
