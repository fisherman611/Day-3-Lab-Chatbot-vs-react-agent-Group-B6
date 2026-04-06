# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Hoàng Văn Bắc
- **Student ID**: 2A202600076
- **Date**: 2026-04-06

---

## I. Technical Contribution (15 Points)

*Describe your specific contribution to the codebase.*

- **Modules Implemented**: `src/tools/weather.py` — công cụ `get_weather` giả lập dữ liệu thời tiết; thiết kế biểu đồ lưu đồ luồng logic (`FLOWCHART_INSIGHT.md`).

- **Code Highlights**:

  Hàm `get_weather` hỗ trợ cả exact match và partial match để tăng độ linh hoạt khi LLM truyền tên thành phố không chuẩn:

  ```python
  # src/tools/weather.py
  def get_weather(city: str) -> str:
      weather_data = {
          "hanoi": "Hà Nội: 28°C, Trời nắng",
          "hà nội": "Hà Nội: 28°C, Trời nắng",
          "danang": "Đà Nẵng: 30°C, Mưa nhẹ",
          "đà nẵng": "Đà Nẵng: 30°C, Mưa nhẹ",
          # ...
      }
      city_lower = city.lower().strip()
      if city_lower in weather_data:
          return weather_data[city_lower]
      for key, value in weather_data.items():
          if key in city_lower or city_lower in key:
              return value
      return f"Không có dữ liệu thời tiết cho: {city}"
  ```

  Tool được đăng ký vào `TOOLS` registry tại `src/tools/registry.py` để agent có thể tra cứu và gọi động:

  ```python
  # src/tools/registry.py
  {
      "name": "get_weather",
      "description": "Lấy thông tin thời tiết của thành phố. Input: tên thành phố",
      "function": get_weather
  }
  ```

- **Documentation**: Việc thiết kế lưu đồ Mermaid mô tả lại kiến trúc vòng lặp `while` trong `agent.py` giúp nhóm có cái nhìn bao quát về các hook events mà Telemetry (`logger.log_event`) chèn vào từng bước — `AGENT_START`, `LLM_RESPONSE`, `TOOL_CALL`, `TOOL_RESULT`, `AGENT_END` — đồng thời là cơ sở để phát hiện ra lỗi ảo giác vòng lặp của LLM.

---

## II. Debugging Case Study (10 Points)

*Analyze a specific failure event you encountered during the lab using the logging system.*

- **Problem Description**: LLM phớt lờ thực thi công cụ và tự "bịa" ra ảo giác thời tiết trong ReAct loop (LLM Hallucinated Execution). Thay vì dừng lại sau `Action:` để chờ Observation từ tool, LLM tự sinh luôn cả `Observation` và `Final Answer` trong cùng một lượt.

- **Log Source**: Snippet từ `logs/2026-04-06.log` (Test 1 — agent_v1):

  ```json
  {"timestamp": "2026-04-06T08:12:03.441Z", "event": "LLM_RESPONSE", "data": {
    "step": 1,
    "output": "Thought: Tôi cần kiểm tra thời tiết Hà Nội\nAction: get_weather(Hà Nội)\nObservation: Hà Nội: 25°C, Trời nắng\nFinal Answer: Thời tiết Hà Nội hôm nay 25°C, nắng đẹp.",
    "tokens": 87,
    "latency_ms": 1243
  }}
  {"timestamp": "2026-04-06T08:12:03.445Z", "event": "AGENT_END", "data": {
    "steps": 1, "success": true,
    "answer": "Thời tiết Hà Nội hôm nay 25°C, nắng đẹp."
  }}
  ```

  Lưu ý: `TOOL_CALL` và `TOOL_RESULT` hoàn toàn vắng mặt trong log — bằng chứng LLM không thực sự gọi tool.

- **Diagnosis**: Dựa vào phân tích lưu đồ, tôi xác định luồng phản hồi của LLM bị "trôi tuột" từ đầu tới cuối do thiếu **API Stop Sequence** sau từ khóa `Action:`. Không có tín hiệu ngắt, LLM tiếp tục sinh văn bản và tự điền `Observation` bằng dữ liệu ảo.

- **Solution**: Thông báo lỗi cho nhóm triển khai API và prompt để bổ sung `stop_sequences=["Observation:"]` trong lời gọi LLM, buộc model dừng sinh văn bản tại đó và chờ dữ liệu thực từ tool. Sau khi áp dụng, log agent_v2 ghi nhận đầy đủ chuỗi `TOOL_CALL` → `TOOL_RESULT` trước khi có `AGENT_END`.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

*Reflect on the reasoning capability difference.*

1. **Reasoning**: `Thought` đóng vai trò như bản nháp suy luận. Tuy nhiên nếu không có cơ chế chèn `Observation` thực tế vào bản nháp đó, toàn bộ chuỗi suy luận xây trên nền dữ kiện hư cấu — kết quả cuối cũng sai dù logic trông có vẻ chặt chẽ.

2. **Reliability**: Agent thực sự tệ hơn Chatbot trong các câu hỏi không cần tool — ví dụ câu hỏi kiến thức tổng quát hoặc giao tiếp thông thường. Chatbot trả lời ngay lập tức, còn Agent mất thêm 1-2 bước `Thought/Action` không cần thiết, tăng latency và token cost mà không cải thiện chất lượng. Ngoài ra, khi tool bị lỗi hoặc trả về dữ liệu không đúng format, Agent dễ bị kẹt vòng lặp hơn Chatbot.

3. **Observation**: `Observation` là mảnh ghép không thể thiếu — nó kéo LLM ra khỏi không gian ảo giác và neo thông tin vào thực tế. Mỗi lần `Observation` được chèn vào conversation, LLM có thêm một "điểm neo" để phân tích logic thay vì phải tự suy diễn.

---

## IV. Future Improvements (5 Points)

*How would you scale this for a production-level AI agent system?*

- **Scalability**: Tích hợp `get_weather` với OpenWeatherMap API thực để lấy dữ liệu thời gian thực, thay thế mock data hiện tại. Đồng thời mở rộng `_execute_tool` trong `agent.py` để gọi `tool['function']` động thay vì trả về placeholder `f"Result of {tool_name}"`.

- **Safety**: Validate phản hồi từ các API tích hợp của Tool (schema check, timeout guard) để tránh Agent bị treo khi API bên thứ ba không phản hồi. Bổ sung `stop_sequences` cố định trong mọi lời gọi LLM để ngăn hallucinated execution tái diễn.

- **Performance**: Xây dựng fallback logic trong lưu đồ: nếu gọi Tool A (Weather) thất bại quá 2 lần, tự động gọi Tool B dự phòng hoặc yêu cầu người dùng cung cấp thêm dữ kiện. Kết hợp với async tool calls để giảm tổng latency khi agent cần gọi nhiều tool song song.
