from adk.tools import tool

@tool
def get_error_details(issue_type: str) -> str:
    """Gets error details for a given issue type."""
    return f"Error details for issue type: {issue_type}"

@tool
def get_speed_issues(issue_type: str) -> str:
    """Gets speed issues for a given issue type."""
    return f"Speed issues for issue type: {issue_type}"

@tool
def get_accessibility_issues(issue_type: str) -> str:
    """Gets accessibility issues for a given issue type."""
    return f"Accessibility issues for issue type: {issue_type}"

@tool
def get_discoverability_issues(issue_type: str) -> str:
    """Gets discoverability issues for a given issue type."""
    return f"Discoverability issues for issue type: {issue_type}"
