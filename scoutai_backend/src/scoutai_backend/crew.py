from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, TavilySearchTool

@CrewBase
class ScoutaiBackend():
    """ScoutaiBackend crew"""

    agents: list[BaseAgent]
    tasks: list[Task]
    # tool = SerperDevTool(
    #     country = "INDIA"
    # )

    tool = TavilySearchTool()  

    minimax = LLM(model="ollama/minimax-m3:cloud")
    gemma = LLM(model="ollama/gemma4:31b-cloud")
    


    @agent
    def research_analyst(self):
        """Agent to research competitors in the startup space"""
        return Agent(
            config = self.agents_config["research_analyst"],
            llm=self.minimax,
            tools=[self.tool],
            verbose = False
        )
    
    @agent
    def market_analyst(self):
        """Agent to analyze market trends and competitor strategies"""
        return Agent(
            config = self.agents_config["market_analyst"],
            llm=self.gemma,
            tools=[self.tool],
            verbose = False
        )
    
    @agent
    def report_writer(self):
        """Agent to compile research findings into a comprehensive report"""
        return Agent(
            config = self.agents_config["report_writer"],
            llm=self.oss,
            tools=[],
            verbose = False
        )
    
    @task
    def search_competitors(self):
        return Task(config = self.tasks_config["search_competitors"],   verbose = False)
    
    @task
    def analyze_competitive_landscape(self):
        return Task(config = self.tasks_config["analyze_competitive_landscape"],    verbose = False)
    
    @task
    def write_intel_report(self):
        return Task(config = self.tasks_config["write_intel_report"],   verbose = False)
    
    @crew
    def crew(self) -> Crew:
        """Define the crew with its agents and tasks"""
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.sequential,
            verbose = False,
            tracing=True
        )