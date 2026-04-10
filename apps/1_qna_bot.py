from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

while True:
    query = input("User: ")

    if query.lower() in ["quit", "exit"]:
        print("GoodBye !")
        break
    res = llm.invoke(query)
    print("AI: ", res.content)