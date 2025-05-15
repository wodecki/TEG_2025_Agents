import json
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool 

# Initialize the model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)


@tool # Decorate the function to make it a LangChain Tool
def get_current_weather(location: str, unit: str = "fahrenheit") -> str:
    """
    Get the current weather in a given location.

    Args:
        location: The city and state, e.g. San Francisco, CA.
        unit: The unit of temperature, can be 'celsius' or 'fahrenheit'. Defaults to 'fahrenheit'.
    """
    weather_info = {
        "location": location,
        "temperature": "72",  # Placeholder actual value
        "unit": unit,
        "forecast": ["sunny", "windy"],  # Placeholder actual forecast
    }
    return json.dumps(weather_info)

# Create a list of your tools
tools = [get_current_weather]

# Bind the tools to the model
model_with_tools = model.bind_tools(tools)

# Invoke the model without any tools
response = model.invoke("what is the weather in sf?")
print(response)

# Invoke the model with tools
response = model_with_tools.invoke("what is the weather in sf?")

# IMPORTANT: the model returns a function call only, not the answer!
print(response)
print(response.additional_kwargs['tool_calls'][0]['function'])

# Extraction details
import json
tool_call_data = response.additional_kwargs['tool_calls'][0]

# Extract the name of a function and its parameters
function_name = tool_call_data['function']['name']
function_args = json.loads(tool_call_data['function']['arguments'])

# Function call
if function_name == "get_current_weather":
    result = get_current_weather(function_args)
    print(f"The current weather: {result}")
    
# Let's add a few more tools to the list
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    print("I multiply two numbers together")
    return a * b

model_with_tools = model.bind_tools([multiply])

from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage

tool_call = model_with_tools.invoke([HumanMessage(content=f"How much is two multiplied by 3?", name="Andrzej")])

print(tool_call)

# Calling the LLM to use a function is not that easy...

from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    print("I multiply two numbers together")
    return a * b

model_with_tools = model.bind_tools([multiply])

# We will the specific prompt from the hub
prompt = hub.pull("hwchase17/openai-tools-agent")
tools = [get_current_weather, multiply]
agent = create_tool_calling_agent(model, tools, prompt)

# We also need to create a separate “executor” for the agent: its task will be to run the functions indicated by the model.
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Finally, we can call the agent with a question
agent_executor.invoke(
    {
        "input": "What is the temperature in the city where PKN Orlen was founded, raised to the second power??",
    }
)