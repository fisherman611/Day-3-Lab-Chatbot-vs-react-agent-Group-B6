import os
import sys
from pathlib import Path
import logging

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from src.agent.agent import ReActAgent
from src.core.openai_provider import OpenAIProvider
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run the ReAct Agent Travel Advisor")
    parser.add_argument("--registry", type=int, choices=[1, 2], default=1, help="Registry version to use (1 or 2)")
    parser.add_argument("--max-steps", type=int, default=8, help="Maximum steps for the agent")
    parser.add_argument("--prompt-path", type=str, default="src/prompts/system_prompt_v1.txt", help="Path to the system prompt file")
    parser.add_argument("--testcases", type=str, default="testcases/travel_agent_questions.json", help="Path to the test cases JSON file")
    parser.add_argument("--question", type=str, help="Run the agent for a single question instead of the test cases file")
    parser.add_argument("--log-file", type=str, default="log_agent.txt", help="Path to the log file")
    
    args = parser.parse_args()

    # Tạo thư mục chứa log nếu chưa tồn tại
    Path(args.log_file).parent.mkdir(parents=True, exist_ok=True)

    # Cấu hình logging để ghi vào file log_agent.txt và console
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[
            logging.FileHandler(args.log_file, encoding='utf-8', mode='w'),
            logging.StreamHandler()
        ]
    )
    
    # Chọn registry dựa trên tham số --registry
    if args.registry == 2:
        from src.tools.registry_2 import TOOLS
        logging.info("Using Tool Registry V2 (Enhanced)")
    else:
        from src.tools.registry import TOOLS
        logging.info("Using Tool Registry V1 (Basic)")
    
    # Load environment
    load_dotenv()
    api_key = os.getenv("NVIDIA_API_KEY")
    base_url = os.getenv("NVIDIA_BASE_URL")
    
    # Khởi tạo LLM
    llm = OpenAIProvider(api_key=api_key, base_url=base_url)
    
    # Khởi tạo Agent với max_steps và prompt path từ arguments
    agent = ReActAgent(llm=llm, tools=TOOLS, max_steps=args.max_steps, system_prompt_path=args.prompt_path)
    
    logging.info("="*70)
    logging.info("TESTING REACT AGENT - TRAVEL ADVISOR")
    logging.info("="*70)

    if args.question:
        test_cases = [args.question]
    else:
        # Test cases from file
        try:
            with open(args.testcases, "r", encoding="utf-8") as f:
                data = json.load(f)
            test_cases = [sample["question"] for sample in data]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading test cases from {args.testcases}: {e}")
            sys.exit(1)
    
    for i, question in enumerate(test_cases, 1):
        logging.info(f"\n[TEST {i}] User: {question}")
        logging.info("-"*70)
        
        answer = agent.run(question)
        
        logging.info(f"Agent: {answer}")
        logging.info("="*70)

if __name__ == "__main__":
    main()
