from dotenv import load_dotenv
load_dotenv()

from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

llm = ChatGroq(model="openai/gpt-oss-20b")
search = GoogleSerperAPIWrapper()
import requests
try:
    response = requests.get("https://google.serper.dev", timeout=5)
    print("Connection Successful:", response.status_code)
except Exception as e:
    print("Connection Failed:", e)
agent = create_agent(
    model=llm,
    tools=[search.run],
    system_prompt="You are a agent and can search for any question on Google",
    checkpointer=MemorySaver()
)

while True:
    query = input("User: ")
    if query.lower() == "quit":
        print("Good Bye !")
        break

    response = agent.invoke({"messages": {"role":"user", "content":query}}, {"configurable":{"thread_id":"1"}})

    print(response["messages"][-1].content)