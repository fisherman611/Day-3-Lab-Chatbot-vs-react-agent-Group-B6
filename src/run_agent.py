import os
from dotenv import load_dotenv
from src.agent.agent import ReActAgent
from src.tools.registry import TOOLS
from src.chatbot import get_llm_provider

def main():
    # Load environment
    load_dotenv()
    
    # Khởi tạo LLM
    llm = get_llm_provider()
    
    # Khởi tạo Agent với max_steps cao hơn cho câu hỏi phức tạp
    agent = ReActAgent(llm=llm, tools=TOOLS, max_steps=8)
    
    # Test cases
    test_cases = [
        "Tính 15 * 23",
        "Thời tiết Hà Nội hôm nay thế nào?",
        "Tính 100 + 50 rồi nhân với 2",
        "Thủ đô của Việt Nam là gì?",
        "Tính (10 + 5) * 3 - 20",
        
        # Test cases mới - Tư vấn du lịch
        "Tôi có 5 triệu đồng, muốn đi du lịch 3 ngày. Nên đi Hà Nội hay Đà Nẵng? Chi phí mỗi ngày khoảng bao nhiêu?",
        "So sánh thời tiết và chi phí giữa Hà Nội và Sài Gòn",
    ]
    
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
