from adk.agents import LlmAgent
from adk.llms import GcpVertexAiLlm, CacheConfig, RetryConfig
from adk.planners import ReactPlanner
from adk.planners.thinking import ThinkingConfig
from src.tools import data_gatherer_tools


def create_data_gatherer_agent():
    """Creates the data gatherer agent."""
    return LlmAgent(
        llm=GcpVertexAiLlm(
            model="gemini-1.5-flash-001",
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
        thinking_config=ThinkingConfig(
            enable_thinking=True,
            thought_llm_config_override={"temperature": 0.2},
        ),
    )
