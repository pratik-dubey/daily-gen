from dotenv import load_dotenv
load_dotenv(override=True)

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize the Gemini Model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

st.title("🤖 AskBuddy - AI QNA chatbot")
st.markdown("Qna Chatbot with Langchain and Gemini")

# --- SESSION STATE (Memory) ---
# NOTE: Streamlit reruns the whole script on every click/input.
# session_state acts as a permanent 'storage' so your chat history doesn't disappear.
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- THE HISTORY LOOP ---
# Q: Why no double printing? 
# A: This loop runs BEFORE the new 'query' code below. 
# It only displays what was saved in PREVIOUS runs.
for message in st.session_state.messages:
    content = message["content"]
    role = message["role"]
    st.chat_message(role).markdown(content)

# --- USER INPUT ---
query = st.chat_input("Ask anything ?")

if query:
    # 1. Save and display the user's current question
    st.session_state.messages.append({"role": "user", "content": query})
    st.chat_message("user").markdown(query)
    
    # 2. Call the AI Model
    res = llm.invoke(query)
    
    # 3. Display the AI response and save it to history
    # This won't show up in the 'for' loop above until the NEXT time you send a message.
    st.chat_message("ai").markdown(res.content)
    st.session_state.messages.append({"role": "ai", "content": res.content})