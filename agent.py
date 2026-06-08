"""Weather & News Agent - CLI entry point.

A single-purpose AI agent that uses Ollama function calling
to answer weather and news queries with live data.
"""

import sys
import asyncio
from llm_client import chat

# Fix Chinese input/output on Windows terminals
if sys.platform == "win32":
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")


async def main():
    print("=" * 50)
    print("Weather & News Agent")
    print("=" * 50)
    print("Tools: get_weather, get_news")
    print("LLM:   Ollama (qwen2.5:7b)")
    print("Type 'quit' or 'exit' to stop")
    print("=" * 50)

    history = []

    while True:
        try:
            user_input = input("\n>>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        history.append({"role": "user", "content": user_input})
        print()  # blank line before response
        response = await chat(history)
        print(response)
        history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    asyncio.run(main())
