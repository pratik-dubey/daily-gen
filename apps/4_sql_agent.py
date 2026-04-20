from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit 
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
import streamlit as st

db = SQLDatabase.from_uri("sqlite:///my_tasks.db")

db.run("""
   CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT CHECK (status IN ('pending', 'in_progress', 'completed')) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
    );
""")

model = ChatGroq(model="openai/gpt-oss-20b")
toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()
# memory = InMemorySaver()

# for tool in tools:
#     print(tool.name)
# sql_db_query
# sql_db_schema
# sql_db_list_tables
# sql_db_query_checker

system_prompt = """You are a SQL expert assistant. 
Your database has a 'tasks' table with columns: id, title, description, status, created_at.
The 'status' column only accepts: 'pending', 'in_progress', 'completed'.

Rules:
1. Use the 'sql_db_query' tool to run your commands.
2. Always limit SELECT queries to 10 results.
3. When creating or updating, use actual values, not placeholders.
4. After any modification (INSERT/UPDATE/DELETE), run a SELECT query to verify the change.
5. Display lists of tasks as Markdown tables.
"""
# we are creating the agent inside a decorator and function so that the memory is not being created again and again as in streamlit in every query , whole code runs from top to bottom again 

@st.cache_resource
def get_agent():
    agent = create_agent(
        model=model,
        checkpointer=InMemorySaver(),
        tools=tools,
        system_prompt=system_prompt
    )
    return agent

agent = get_agent()

st.subheader(" Taskbot - Mange your tasks !")

prompt = st.chat_input("Ask me to manage your tasks ...")

if "history" not in st.session_state:
     st.session_state.history = []

for chat in st.session_state.history:
     st.chat_message(chat["role"]).markdown(chat["content"])
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.history.append({"role":"user", "content":prompt})
    with st.chat_message("ai"):
        with st.spinner("Processing..."):
                response = agent.invoke({"messages":[{"role":"user", "content":prompt}]}, {"configurable": {"thread_id": "1"}})
                result = response["messages"][-1].content
                st.session_state.history.append({"role":"ai", "content":result})
                st.markdown(result)


# print("Table created!")