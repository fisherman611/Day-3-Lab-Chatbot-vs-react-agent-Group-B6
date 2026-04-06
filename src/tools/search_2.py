import os
from tavily import TavilyClient

def search_tavily(query: str) -> str:
    """
    Tìm kiếm thông tin trực tiếp từ internet sử dụng Tavily API.
    
    Args:
        query: Câu hỏi cần tìm kiếm
    
    Returns:
        Thông tin tìm được dạng văn bản
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Lỗi: Không tìm thấy TAVILY_API_KEY trong file .env"

    try:
        tavily = TavilyClient(api_key=api_key)
        # Thực hiện tìm kiếm nâng cao (context) để có kết quả tốt hơn
        response = tavily.search(query=query, search_depth="advanced")
        
        # Format kết quả
        results = response.get('results', [])
        if not results:
            return f"Không tìm thấy thông tin trực tuyến cho: {query}"
            
        formatted_results = []
        for i, res in enumerate(results[:3], 1): # Lấy top 3 kết quả
            title = res.get('title', 'No Title')
            content = res.get('content', 'No Content')
            source = res.get('url', 'No URL')
            formatted_results.append(f"{i}. [{title}] {content}\nNguồn: {source}")
            
        return "Kết quả tìm kiếm từ internet:\n\n" + "\n\n".join(formatted_results)
        
    except Exception as e:
        return f"Lỗi khi tìm kiếm với Tavily: {str(e)}"
