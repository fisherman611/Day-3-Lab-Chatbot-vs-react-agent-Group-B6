import os
import sys
from pathlib import Path
import logging
import json
import argparse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from src.core.openai_provider import OpenAIProvider


def main():
    parser = argparse.ArgumentParser(description="Run the Chatbot Baseline Travel Advisor")
    parser.add_argument("--testcases", type=str, default="testcases/travel_agent_questions.json", help="Path to the test cases JSON file")
    parser.add_argument("--question", type=str, help="Run the chatbot for a single question instead of the test cases file")
    parser.add_argument("--log-file", type=str, default="log_chatbot.txt", help="Path to the log file")
    
    args = parser.parse_args()

    # Tạo thư mục chứa log nếu chưa tồn tại
    Path(args.log_file).parent.mkdir(parents=True, exist_ok=True)

    # Cấu hình logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[
            logging.FileHandler(args.log_file, encoding="utf-8", mode="w"),
            logging.StreamHandler(),
        ],
    )

    # Load environment
    load_dotenv()
    api_key = os.getenv("NVIDIA_API_KEY")
    base_url = os.getenv("NVIDIA_BASE_URL")

    # Khởi tạo LLM cho chatbot baseline
    llm = OpenAIProvider(api_key=api_key, base_url=base_url)

    # System prompt mặc định như lúc đầu
    system_prompt = (
        "Bạn là trợ lý du lịch, trả lời ngắn gọn, thực tế, ưu tiên dữ liệu rõ ràng và không tự bịa khi thiếu thông tin."
    )

    # Xác định danh sách câu hỏi
    if args.question:
        test_cases = [args.question]
    else:
        try:
            with open(args.testcases, "r", encoding="utf-8") as f:
                data = json.load(f)
            test_cases = [sample["question"] for sample in data]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading test cases from {args.testcases}: {e}")
            sys.exit(1)

    logging.info("=" * 70)
    logging.info("TESTING CHATBOT BASELINE - TRAVEL ADVISOR")
    logging.info("=" * 70)

    for i, question in enumerate(test_cases, 1):
        logging.info(f"\n[TEST {i}] User: {question}")
        logging.info("-" * 70)

        response = llm.generate(question, system_prompt=system_prompt)
        answer = response.get("content", "")

        logging.info(f"Chatbot: {answer}")
        logging.info(f"Provider: {response.get('provider', 'unknown')}")
        logging.info(f"Latency (ms): {response.get('latency_ms', 0)}")
        logging.info(f"Tokens: {response.get('usage', {}).get('total_tokens', 0)}")
        logging.info("=" * 70)


if __name__ == "__main__":
    main()