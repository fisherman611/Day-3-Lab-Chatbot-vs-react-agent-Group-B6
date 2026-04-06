import requests

def get_weather_live(city: str) -> str:
    """
    Lấy thông tin thời tiết thực tế từ Open-Meteo API (không cần API key).

    Args:
        city: Tên thành phố

    Returns:
        Thông tin thời tiết hiện tại
    """
    try:
        # Bước 1: Geocoding - chuyển tên thành phố sang tọa độ
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_resp = requests.get(geo_url, params={"name": city, "count": 1, "language": "vi"}, timeout=10)
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()

        results = geo_data.get("results")
        if not results:
            return f"Không tìm thấy thành phố: {city}"

        location = results[0]
        lat = location["latitude"]
        lon = location["longitude"]
        city_name = location.get("name", city)
        country = location.get("country", "")

        # Bước 2: Lấy thời tiết hiện tại
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_resp = requests.get(weather_url, params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            "timezone": "auto"
        }, timeout=10)
        weather_resp.raise_for_status()
        weather_data = weather_resp.json()

        current = weather_data.get("current", {})
        temp = current.get("temperature_2m", "N/A")
        humidity = current.get("relative_humidity_2m", "N/A")
        wind = current.get("wind_speed_10m", "N/A")
        code = current.get("weather_code", 0)

        condition = _weather_code_to_text(code)

        return (
            f"Thời tiết tại {city_name}, {country}:\n"
            f"  Nhiệt độ: {temp}°C\n"
            f"  Trạng thái: {condition}\n"
            f"  Độ ẩm: {humidity}%\n"
            f"  Gió: {wind} km/h"
        )

    except requests.exceptions.Timeout:
        return f"Lỗi: Timeout khi lấy thời tiết cho '{city}'"
    except requests.exceptions.RequestException as e:
        return f"Lỗi kết nối khi lấy thời tiết: {str(e)}"
    except Exception as e:
        return f"Lỗi không xác định: {str(e)}"


def _weather_code_to_text(code: int) -> str:
    """Chuyển WMO weather code sang mô tả tiếng Việt."""
    if code == 0:
        return "Trời quang"
    elif code in (1, 2, 3):
        return "Ít mây" if code == 1 else ("Có mây" if code == 2 else "Nhiều mây")
    elif code in (45, 48):
        return "Sương mù"
    elif code in range(51, 68):
        return "Mưa phùn" if code < 60 else "Mưa"
    elif code in range(71, 78):
        return "Tuyết"
    elif code in range(80, 83):
        return "Mưa rào"
    elif code in (95, 96, 99):
        return "Giông bão"
    return "Không xác định"
