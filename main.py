import asyncio
import json
import socket
from typing import Any
from httpx import AsyncClient
from time import sleep
from sys import argv
from tools.console import info, error, warning

def send_log_to_server(log_msg: str):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('127.0.0.1', 8000)) 
            s.sendall(json.dumps({"log": log_msg}).encode())
    except Exception as e:
        error(f"Failed to send log: {e}")

class CheckNetwork:
    def __init__(self, target: str, delay: int):
        self.target = f"https://{target}" if "http" not in target else target
        self.delay = delay

    async def request_handler(self) -> Any:
        async with AsyncClient() as client:
            try:
                response = await client.get(self.target, timeout=self.delay)
                await asyncio.sleep(self.delay)
                return response.status_code
            except Exception as e:
                error(f"Error on {self.target}: {e}")
                return None

    async def check(self) -> Any:
        try:
            status = await self.request_handler()
            if status == 200:
                info_msg = f"HOST IS UP Site: {self.target} Status_code: {status}"
                info(info_msg)
                send_log_to_server(info_msg)
            else:
                warning_msg = f"Site: {self.target} Status_code: {status}"
                warning(warning_msg)
                send_log_to_server(warning_msg)
        except Exception as e:
            error_msg = f"Exception on {self.target}: {e}"
            error(error_msg)
            send_log_to_server(error_msg)

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
            send_log_to_server(f"Error in gather: {e}")

if __name__ == '__main__':
    asyncio.run(main())
