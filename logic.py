import asyncio
import json
from typing import Any
from httpx import AsyncClient
from time import sleep
from sys import argv
from tools.console import info, error, warning

class CheckNetwork:
    def __init__(self, target: str, delay: int):
        self.target = f"https://{target}" if "http" not in target else target
        self.delay = delay

    async def request_handler(self) -> Any:
        async with AsyncClient() as client:
            try:
                response = await client.get(self.target, timeout=self.delay)
                await asyncio.sleep(sleep)
                return response.status_code
            except Exception as e:
                error(f"Error on {self.target}: {e}")
                return None

    async def check(self) -> Any:
        try:
            status = await self.request_handler()
            if status == 200:
                info(f"HOST IS UP Site: {self.target} Status_code: {status}")
            else:
                warning(f"Site: {self.target} Status_code: {status}")
        except Exception as e:
            error(f"Exception on {self.target}: {e}")

async def main():
    with open('targets.json', 'r') as file:
        targets = json.load(file)

    while True:
        tasks = []
        for target_data in targets:
            target = target_data['url']
            delay = target_data.get('delay', 1)
            check = CheckNetwork(target, delay)
            tasks.append(check.check())

        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            error(f"Error in gather: {e}")


if __name__ == '__main__':
    asyncio.run(main())