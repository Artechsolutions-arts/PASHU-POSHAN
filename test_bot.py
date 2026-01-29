import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPEN_API_KEY")
if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key

print(f"Key found: {openai_key[:10]}...")

try:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    response = llm.invoke("Hello, are you working? Respond with 'Yes, I am working!'").content
    print(f"Response: {response}")
except Exception as e:
    print(f"Error: {e}")
