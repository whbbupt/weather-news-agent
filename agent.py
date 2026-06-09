"""Weather & News Agent - CLI entry point.

A single-purpose AI agent that uses Ollama function calling
to answer weather and news queries with live data.
"""

import sys
import asyncio
import httpx
from llm_client import chat


async def check_ollama() -> bool:
    """Verify Ollama is running and the model is available."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("http://localhost:11434/api/tags", timeout=5)
            if resp.status_code == 200:
                return True
    except Exception:
        pass
    return False


async def main():
    print("=" * 50)
    print("Weather & News Agent")
    print("=" * 50)
    print("Tools: get_weather, get_news")
    print("LLM:   Ollama (qwen2.5:7b)")

    # Startup check
    print("Checking Ollama connection...", end=" ")
    if await check_ollama():
        print("OK")
    else:
        print("FAILED")
        print()
        print("ERROR: Cannot connect to Ollama.")
        print("Please ensure Ollama is running:")
        print("  1. Start the Ollama desktop app, or")
        print('  2. Run: ollama serve')
        print("  3. Pull the model: ollama pull qwen2.5:7b")
        sys.exit(1)

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
        print()
        try:
            response = await chat(history)
            print(response)
        except Exception as e:
            print(f"Error: {e}")
            history.pop()
            continue
        history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    asyncio.run(main())
