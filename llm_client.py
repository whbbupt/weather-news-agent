"""Ollama chat client with tool-calling orchestration."""

import json
import httpx
from tool_schemas import TOOLS

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:7b"


SYSTEM_PROMPT = """You are a helpful weather and news assistant. You can:

1. Check current weather for any city using the get_weather tool.
2. Search recent news headlines using the get_news tool.

Rules:
- When asked about weather, ALWAYS call get_weather first, then summarize the result in natural language.
- When asked about news, ALWAYS call get_news first, then list the headlines with brief summaries.
- If a tool returns an error, explain the error to the user in a friendly way.
- Answer in the same language the user used (Chinese or English).
- Keep responses concise and informative.
- If the user asks something unrelated to weather or news, politely remind them you can only help with weather and news queries."""


async def chat(messages: list[dict]) -> str:
    """Send messages to Ollama, handling tool-calling loop.

    If the model returns tool_calls, executes them and feeds results
    back into context until a final text response is produced.
    """
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    async with httpx.AsyncClient() as client:
        for _ in range(5):  # max rounds to prevent infinite loops
            resp = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "messages": full_messages,
                    "tools": TOOLS,
                    "stream": False,
                },
                timeout=60,
            )
            data = resp.json()
            msg = data["message"]

            if msg.get("tool_calls"):
                from tools import get_weather, get_news

                tool_results = []
                for tc in msg["tool_calls"]:
                    fn = tc["function"]
                    name = fn["name"]
                    args = fn["arguments"]

                    if name == "get_weather":
                        result = await get_weather(**args)
                    elif name == "get_news":
                        result = await get_news(**args)
                    else:
                        result = {"error": f"Unknown tool: {name}"}

                    tool_results.append({
                        "role": "tool",
                        "content": json.dumps(result, ensure_ascii=False),
                    })

                full_messages.append(msg)
                full_messages.extend(tool_results)
            else:
                return msg.get("content", "")

        return "抱歉，工具调用轮次过多，请简化您的问题后重试。"
