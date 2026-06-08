"""Ollama-compatible JSON Schema definitions for agent tools."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的当前天气，返回温度、天气状况和湿度。Get current weather conditions for a city, returns temperature, weather description, and humidity.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称 (中文或英文均可)，如 北京、上海、London、Tokyo",
                    }
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_news",
            "description": "搜索指定话题的最近新闻头条和摘要。Search recent news headlines and summaries for a topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "新闻话题关键词，如 technology、sports、AI、business、science",
                    },
                    "count": {
                        "type": "integer",
                        "description": "返回的新闻条数 (1-10)，默认 5",
                    },
                },
                "required": ["topic"],
            },
        },
    },
]
