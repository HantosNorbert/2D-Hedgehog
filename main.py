# The main entry point for the Hedgehog 2D application. For the web application, we have to use asyncio.

from hedgehog2d import Hedgehog2D
import asyncio

hedgehog = Hedgehog2D()

async def main():
    while True:
        is_running = hedgehog.display()
        await asyncio.sleep(0)

        if not is_running:
            return


asyncio.run(main())
