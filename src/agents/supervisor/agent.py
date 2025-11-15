from adk.agents import LlmAgent
from adk.llms import GcpVertexAiLlm, CacheConfig, RetryConfig
from adk.planners import BuiltInPlanner
from adk.state import State
from src.agents.data_gatherer.agent import create_data_gatherer_agent
from src.agents.task_execution.agent import create_task_execution_agent
import os


def create_supervisor_agent(site_id: str):
    """Creates the supervisor agent."""
    return LlmAgent(
        llm=GcpVertexAiLlm(
            model="gemini-1.5-flash-001",
            project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            location=os.environ.get("GOOGLE_CLOUD_LOCATION"),
            retry_config=RetryConfig(retry_limit=3),
            cache_config=CacheConfig(enable_cache=True),
            stream=True,
        ),
        planner=BuiltInPlanner(
            tools=[
                create_data_gatherer_agent(),
                create_task_execution_agent(site_id),
            ]
        ),
        instruction="""You are a supervisor agent. Your job is to delegate tasks to your sub-agents and synthesize their responses.
        You have a data gatherer agent that can get information about a website, and a task execution agent that can analyze bugs and create bug reports.
        When the user asks a question, first use the data gatherer to get the information you need. Then, if the user wants to submit a bug, use the task execution agent to analyze the bug and create a bug report.
        Finally, synthesize the responses from your sub-agents into a single, coherent response to the user.""",
        state=State({"site_id": site_id}),
    )
