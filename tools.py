"""Agent tool implementations: get_weather and get_news."""

import asyncio
import httpx
import feedparser

# Open-Meteo weather code → human-readable description
WEATHER_CODES = {
    0: "晴天", 1: "大部晴朗", 2: "多云", 3: "阴天",
    45: "雾", 48: "霜雾",
    51: "小雨", 53: "中雨", 55: "大雨",
    61: "雷阵雨", 63: "大雨", 65: "暴雨",
    71: "小雪", 73: "中雪", 75: "大雪",
    80: "阵雨", 81: "中阵雨", 82: "大阵雨",
    95: "雷暴", 96: "冰雹雷暴", 99: "强冰雹雷暴",
}


async def get_weather(city: str) -> dict:
    """Fetch current weather for a city using Open-Meteo API (free, no key needed)."""
    async with httpx.AsyncClient() as client:
        # Step 1: geocode city → lat/lon
        geo_resp = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "zh"},
            timeout=10,
        )
        geo_data = geo_resp.json()
        if not geo_data.get("results"):
            return {"error": f"找不到城市: {city}"}

        result = geo_data["results"][0]
        lat = result["latitude"]
        lon = result["longitude"]
        display_name = result.get("name", city)

        # Step 2: fetch current weather
        weather_resp = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,weather_code",
            },
            timeout=10,
        )
        weather_data = weather_resp.json()
        current = weather_data["current"]
        code = current["weather_code"]

        return {
            "city": display_name,
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "weather": WEATHER_CODES.get(code, f"未知 ({code})"),
        }


# Domestic RSS feeds that work without proxy in China
_RSS_FEEDS = [
    ("https://www.ithome.com/rss/", "IT之家"),
    ("https://36kr.com/feed", "36氪"),
]


async def get_news(topic: str, count: int = 5) -> dict:
    """Fetch recent news headlines for a topic via domestic RSS feeds.

    Fetches from multiple sources, then filters by keyword match against topic.
    """
    count = max(1, min(count, 10))
    loop = asyncio.get_running_loop()

    all_articles = []
    for url, source_name in _RSS_FEEDS:
        try:
            feed = await loop.run_in_executor(None, feedparser.parse, url)
            for entry in feed.entries:
                all_articles.append({
                    "title": entry.get("title", "No title"),
                    "summary": entry.get("summary", "").strip()[:300],
                    "link": entry.get("link", ""),
                    "source": source_name,
                })
        except Exception:
            continue

    if not all_articles:
        return {"topic": topic, "articles": [], "message": "暂无法获取新闻"}

    # Filter by topic keyword (case-insensitive)
    topic_lower = topic.lower()
    matched = []
    for a in all_articles:
        text = (a["title"] + a["summary"]).lower()
        if topic_lower in text:
            matched.append(a)
        elif topic_lower in ("news", "新闻", "最新", "headlines"):
            matched.append(a)

    # If no keyword match or topic is generic, return all
    if not matched:
        matched = all_articles

    return {"topic": topic, "articles": matched[:count]}
