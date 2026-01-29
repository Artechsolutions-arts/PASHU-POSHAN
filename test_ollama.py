"""
Test script to verify Ollama integration with Gemma2:2b model
"""
from langchain_ollama import ChatOllama

print("Testing Ollama with Gemma2:2b model...")
print("-" * 50)

try:
    # Initialize the model
    llm = ChatOllama(
        model="gemma2:2b",
        temperature=0.1,
        base_url="http://localhost:11434"
    )
    
    # Test query
    test_prompt = "What is 2+2? Answer in one short sentence."
    print(f"Query: {test_prompt}")
    print("Waiting for response...")
    
    response = llm.invoke(test_prompt)
    print(f"\nResponse: {response.content}")
    print("-" * 50)
    print("[SUCCESS] Ollama is working correctly with Gemma2:2b")
    
except Exception as e:
    print(f"\n[ERROR]: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure Ollama is running")
    print("2. Verify gemma2:2b model is installed: ollama list")
    print("3. If not installed, run: ollama pull gemma2:2b")
