import os

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
# Load environment variables

from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
tools = [wikipedia]

prompt = """You are a helpful assistant performing Wikipedia search."""

graph = create_react_agent(
    llm,
    tools=tools,
    prompt=prompt,
)

query = "Tell me about Adam Mickiewicz"

sessionId = "session_1"
config = {'configurable': {'thread_id': sessionId}}

response = graph.invoke({'messages': [('user', query)]}, config)

print(response)