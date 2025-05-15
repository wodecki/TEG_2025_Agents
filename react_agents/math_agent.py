import os

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    print("Multiplying", a, b)
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Add a and b.
    Args:
        a: first int
        b: second int
    """
    print("Adding", a, b)
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """Subtract a and b.
    Args:
        a: first int
        b: second int
    """
    print("Subtracting", a, b)
    return a - b

@tool
def divide(a: int, b: int) -> int:
    """Divide a and b.
    Args:
        a: first int
        b: second int
    """
    print("Dividing", a, b)
    return a / b

@tool
def power(a: int, b: int) -> int:
    """Power a and b.
    Args:
        a: first int
        b: second int
    """
    print("Powering", a, b)
    return a ** b

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

tools = [multiply, add, subtract, divide, power]

prompt = """You are a helpful assistant performing basic arithmetic."""

graph = create_react_agent(
    llm,
    tools=tools,
    prompt=prompt,
)

query = "What's 2**3?"

sessionId = "session_1"
config = {'configurable': {'thread_id': sessionId}}

response = graph.invoke({'messages': [('user', query)]}, config)

print(response)