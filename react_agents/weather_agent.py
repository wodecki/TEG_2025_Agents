import os

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENWEATHERMAP_API_KEY"] = os.getenv("OPENWEATHERMAP_API_KEY")

weather = load_tools(["openweathermap-api"])[0]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

tools = [weather]

prompt = """You are a helpful assistant answering questions about the weather."""

graph = create_react_agent(
    llm,
    tools=tools,
    prompt=prompt,
)

query = "What's the weather like in Warsaw?"

sessionId = "session_1"
config = {'configurable': {'thread_id': sessionId}}

response = graph.invoke({'messages': [('user', query)]}, config)

print(response)