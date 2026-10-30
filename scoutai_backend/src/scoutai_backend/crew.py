import os
import logging
from dotenv import load_dotenv
import litellm
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, TavilySearchTool

load_dotenv()  # Load environment variables from .env file

# Clean terminal logging configuration:
# Suppress telemetry and third-party info/debug logs so terminal stays clean
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["LITELLM_LOG"] = "ERROR"
litellm.suppress_debug_info = True
litellm.set_verbose = False

# Only print WARNING (if any exists) or ERRORS in the terminal
logging.basicConfig(level=logging.WARNING)
logging.getLogger("crewai").setLevel(logging.WARNING)
logging.getLogger("litellm").setLevel(logging.WARNING)
logging.getLogger("LiteLLM").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

@CrewBase
class ScoutaiBackend():
    """ScoutaiBackend crew"""

    agents: list[BaseAgent]
    tasks: list[Task]
    tool = SerperDevTool()
 

    model = LLM(
        model = "ollama/gemma4:31b",
        base_url = "https://ollama.com/v1",
        api_key = os.getenv("OLLAMA_API_KEY")
    )

    @agent
    def research_analyst(self):
        """Agent to research competitors in the startup space"""
        return Agent(
            config = self.agents_config["research_analyst"],
            llm=self.model,
            tools=[self.tool],
            verbose = False
        )
    
    @agent
    def market_analyst(self):
        """Agent to analyze market trends and competitor strategies"""
        return Agent(
            config = self.agents_config["market_analyst"],
            llm=self.model,
            tools=[self.tool],
            verbose = False
        )
    
    @agent
    def report_writer(self):
        """Agent to compile research findings into a comprehensive report"""
        return Agent(
            config = self.agents_config["report_writer"],
            llm=self.model,
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
        )