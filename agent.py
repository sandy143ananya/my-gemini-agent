import google.adk as adk

# Using the active gemini-2.5-flash model matches the v1beta API rules
root_agent = adk.Agent(
    name="SmartTravelAgent",
    instruction="You are a helpful travel assistant. Help users plan trips with budget options.",
    model="gemini-2.5-flash"
)
