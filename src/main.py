from src.agents.supervisor.agent import create_supervisor_agent
from adk.api.server import APIServer
from adk.sessions import Session


def main():
    """Main function to run the AI insights agent."""
    site_id = "12345"  # This will be passed from the frontend
    supervisor = create_supervisor_agent(site_id)
    session = Session()

    print("AI Insights Agent is running. Type 'exit' to quit.")
    while True:
        user_input = input("> ")
        if user_input == "exit":
            break
        for chunk in session.stream(supervisor, user_input):
            print(chunk.text, end="")
        print()


if __name__ == "__main__":
    main()
