import os

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools
# Load environment variables

from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

arxiv = load_tools(["arxiv"])[0]
tools = [arxiv]

prompt = """You are a helpful assistant performing internet search for scientific papers."""

graph = create_react_agent(
    llm,
    tools=tools,
    prompt=prompt,
)

query = "Find papers about quantum computing"

sessionId = "session_1"
config = {'configurable': {'thread_id': sessionId}}

response = graph.invoke({'messages': [('user', query)]}, config)

print(response)