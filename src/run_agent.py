import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from src.agent.agent import ReActAgent
from src.tools.registry import TOOLS
from src.core.openai_provider import OpenAIProvider
import json

def main():
    # Load environment
    load_dotenv()
    api_key = os.getenv("NVIDIA_API_KEY")
    base_url = os.getenv("NVIDIA_BASE_URL")
    
    # Khởi tạo LLM
    llm = OpenAIProvider(api_key=api_key, base_url=base_url)
    
    # Khởi tạo Agent với max_steps cao hơn cho câu hỏi phức tạp
    agent = ReActAgent(llm=llm, tools=TOOLS, max_steps=8)
    
    
    # Test cases
    with open("testcases/travel_agent_questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    test_cases = [sample["question"] for sample in data]
    
    print("="*70)
    print("TESTING REACT AGENT - TRAVEL ADVISOR")
    print("="*70)
    
    for i, question in enumerate(test_cases, 1):
        print(f"\n[TEST {i}] User: {question}")
        print("-"*70)
        
        answer = agent.run(question)
        
        print(f"Agent: {answer}")
        print("="*70)

if __name__ == "__main__":
    main()
