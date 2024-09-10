from crewai import Agent, Crew
from tools.deepinfra_tool import DeepInfraTool
from tools.perplexity_tool import PerplexityTool  # New tool for research
from tools.document_tool import DocumentTool  # New tool for document analysis
from tools.code_tool import CodeTool  # New tool for code execution
import asyncio
from typing import List, Dict, Any
# Task class with to_dict method
class Task:
    def __init__(self, task_name, task_description):
        self.task_name = task_name
        self.task_description = task_description

    def to_dict(self):
        return {
            'task_name': self.task_name,
            'task_description': self.task_description
        }


# Set up Crew with agents
def setup_crew():
    agents = [
        VisionaryAgent(),  # For reasoning using DeepInfra
        ResearchAgent(),   # For research using Perplexity
        CodeAgent(),       # For code execution
        DocumentAgent(),   # For document analysis
        EntrepreneurAgent() # For business-related tasks
    ]
    return Crew(agents)
# Visionary Agent uses Reflection-Llama for reasoning tasks
class VisionaryAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Visionary',
            goal='Handle high-level conceptual tasks and strategy.',
            backstory='You represent forward-thinking and problem-solving in creative ways.'
        )
        self._deepinfra_tool = DeepInfraTool()

    def handle_task(self, task_description):
        # Always perform reasoning for any task
        return self._deepinfra_tool.generate_text(task_description)


class ResearchAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Researcher',
            goal='Perform deep research using online sources and APIs.',
            backstory='You represent curiosity and fact-finding.'
        )
        self._perplexity_tool = PerplexityTool()

    def handle_task(self, task_description):
        # Always perform research for any task
        return self._perplexity_tool.perform_research(task_description)

# Code Agent handles code generation and execution
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

# Document Agent processes and analyzes documents
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

# Entrepreneur Agent for business-related tasks
class EntrepreneurAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Entrepreneur',
            goal='Handle tasks related to business strategy and entrepreneurship.',
            backstory='You represent entrepreneurial spirit and strategic decision-making.'
        )

    def handle_task(self, task_description):
        # Example of a task that an entrepreneur might handle
        if "business" in task_description.lower() or "strategy" in task_description.lower():
            return "Here’s a detailed business strategy for your project."
        return "No business-related task detected."

# The Crew class delegates tasks to the appropriate agent


class Crew:
    def __init__(self, agents: List[Agent]):
        self.agents = agents
        self.task_queue = asyncio.Queue()

    async def kickoff(self, task: Dict[str, Any]) -> Any:
        await self.task_queue.put(task)
        return await self.process_tasks()

    async def process_tasks(self) -> Any:
        while not self.task_queue.empty():
            task = await self.task_queue.get()
            for agent in self.agents:
                if agent.can_handle(task):
                    return await agent.handle_task(task)
        return None

    async def run(self):
        while True:
            await self.process_tasks()
            await asyncio.sleep(1)


class Agent:
    def __init__(self, role, goal, backstory):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self._original_role = role

    def interpolate_inputs(self, inputs):
        if not isinstance(inputs, dict):
            raise TypeError("Inputs must be a dictionary")
        self.role = self._original_role.format(**inputs)

