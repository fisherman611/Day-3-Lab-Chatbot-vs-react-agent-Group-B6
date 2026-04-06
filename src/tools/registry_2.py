from src.tools.calculator import calculator
from src.tools.search_2 import search_tavily
from src.tools.weather import get_weather

# Registry update: Updated descriptions with clear Input/Output formats
TOOLS = [
    {
        "name": "calculate",
        "description": """Thực hiện các phép tính toán học.
            Input: Biểu thức toán học dạng chuỗi (ví dụ: '2+2', '10*5').
            Output: Kết quả tính toán dưới dạng số.""",
        "function": calculator
    },
    {
        "name": "search_live",
        "description": """Tìm kiếm thông tin thực tế từ internet.
            Input: Câu hỏi hoặc từ khóa tìm kiếm (string).
            Output: Nội dung thông tin tổng hợp từ các kết quả tìm kiếm trực tuyến.""",
        "function": search_tavily
    },
    {
        "name": "get_weather",
        "description": """Lấy thông tin thời tiết của thành phố.
            Input: Tên thành phố (string).
            Output: Thông tin về nhiệt độ, trạng thái thời tiết và các thông số liên quan.""",
        "function": get_weather
    }
]

def get_tool_by_name(name: str):
    """
    Hàm hỗ trợ lấy tool bằng tên gọi.
    """
    for tool in TOOLS:
        if tool["name"] == name:
            return tool["function"]
    return None
