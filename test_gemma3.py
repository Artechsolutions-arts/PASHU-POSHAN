from langchain_ollama import ChatOllama

print("Testing Ollama with gemma3:1b model...")
try:
    llm = ChatOllama(model="gemma3:1b", temperature=0.1, base_url="http://localhost:11434")
    response = llm.invoke("What is 2+2?")
    print(f"Response: {response.content}")
except Exception as e:
    print(f"Error: {e}")
