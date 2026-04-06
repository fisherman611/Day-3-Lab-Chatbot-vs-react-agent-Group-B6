from src.tools.calculator import calculator
from src.tools.search_2 import search_tavily
from src.tools.weather_2 import get_weather_live

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
        "description": """Lấy thông tin thời tiết thực tế của thành phố từ internet.
            Input: Tên thành phố (string).
            Output: Nhiệt độ, trạng thái thời tiết, độ ẩm và tốc độ gió hiện tại.""",
        "function": get_weather_live
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
