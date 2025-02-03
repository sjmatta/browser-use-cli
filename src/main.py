import asyncio
import select
import sys

from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv

load_dotenv()

def get_input():
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.read().strip()  # Read from pipe
    else:
        return input("Enter input: ")  # Prompt user

async def main():
    arguments = get_input()
    agent = Agent(
        task=arguments,
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())