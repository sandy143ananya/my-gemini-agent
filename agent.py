import google.adk as adk
from google.adk.tools import google_search

# Switching the model string to gemini-2.0-flash redirects your request to a stable queue
root_agent = adk.Agent(
    name="SmartTravelAgent",
    instruction="You are a travel assistant. Use Google Search to look up live, current information like weather, flights, or hotel availability.",
    model="gemini-2.0-flash",
    tools=[google_search]
)
