from swarm.repl import run_demo_loop
from agents import close_event_loop, aptos_agent
import asyncio

if __name__ == "__main__":
    try:
        asyncio.run(run_demo_loop(aptos_agent, stream=True))
    finally:
        # Close the loop after all tasks are done
        close_event_loop()
