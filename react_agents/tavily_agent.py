import os

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
# Load environment variables

from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

tavily = TavilySearchResults(max_results=5)
tools = [tavily]

prompt = """You are a helpful assistant performing internet search."""

graph = create_react_agent(
    llm,
    tools=tools,
    prompt=prompt,
)

query = "Tell me about Warsaw?"

sessionId = "session_1"
config = {'configurable': {'thread_id': sessionId}}

response = graph.invoke({'messages': [('user', query)]}, config)

print(response)