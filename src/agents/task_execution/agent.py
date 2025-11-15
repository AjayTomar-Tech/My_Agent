from adk.agents import LlmAgent
from adk.llms import GcpVertexAiLlm, CacheConfig, RetryConfig
from adk.planners import ReactPlanner
from adk.planners.thinking import ThinkingConfig
from adk.state import State
from adk.tools import tool
from src.tools import data_gatherer_tools, task_execution_tools
import os


@tool
def bug_analysis_tool(issue_description: str) -> str:
    """Analyzes a bug and creates a bug proposal."""
    bug_analyzer = LlmAgent(
        llm=GcpVertexAiLlm(
            model="gemini-1.5-flash-001",
            project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            location=os.environ.get("GOOGLE_CLOUD_LOCATION"),
            retry_config=RetryConfig(retry_limit=3),
            cache_config=CacheConfig(enable_cache=True),
        ),
        planner=ReactPlanner(
            tools=[
                data_gatherer_tools.get_error_details,
                data_gatherer_tools.get_speed_issues,
                data_gatherer_tools.get_accessibility_issues,
                data_gatherer_tools.get_discoverability_issues,
            ]
        ),
        instruction="""Analyze the user's issue and create a bug proposal with a title, description, impact, metric, and type.""",
    )
    return bug_analyzer.invoke(issue_description)


def create_task_execution_agent(site_id: str):
    """Creates the task execution agent."""
    return LlmAgent(
        name="TaskExecutionAgent",
        description="Analyzes bugs and creates bug reports.",
        llm=GcpVertexAiLlm(
            model="gemini-1.5-flash-001",
            project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            location=os.environ.get("GOOGLE_CLOUD_LOCATION"),
            retry_config=RetryConfig(retry_limit=3),
            cache_config=CacheConfig(enable_cache=True),
        ),
        planner=ReactPlanner(
            tools=[
                bug_analysis_tool,
                task_execution_tools.bug_url_tool,
            ],
            allow_parallel_calls=True,
        ),
        thinking_config=ThinkingConfig(
            enable_thinking=True,
            thought_llm_config_override={"temperature": 0.2},
        ),
        state=State({"site_id": site_id}),
    )
