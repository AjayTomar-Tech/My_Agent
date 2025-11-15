from adk.tools import tool
from enum import Enum

class Metric(str, Enum):
    PERFORMANCE = "performance"
    ACCESSIBILITY = "accessibility"
    SEO = "seo"
    OTHER = "other"

class BugType(str, Enum):
    BUG = "bug"
    FEATURE_REQUEST = "feature_request"
    OTHER = "other"

@tool
def bug_url_tool(
    site_id: str,
    bug_title: str,
    bug_description: str,
    metric: Metric,
    type: BugType,
) -> str:
    """Creates a pre-filled bug URL."""
    return f"http://bug-tracker.com/submit?site_id={site_id}&title={bug_title}&description={bug_description}&metric={metric}&type={type}"
