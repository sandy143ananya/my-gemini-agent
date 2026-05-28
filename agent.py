import google.adk as adk
from google.adk.tools import google_search

# Defining 'root_agent' satisfies the precise entry point the CLI module expects
root_agent = adk.Agent(
    name="SmartTravelAgent",
    instruction="You are a travel assistant. Use Google Search to look up live, current information like weather, flights, or hotel availability.",
    model="gemini-2.5-flash",
    tools=[google_search]
)
