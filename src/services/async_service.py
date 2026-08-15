import asyncio
from time import perf_counter

import aiohttp


async def fetch_url_async(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()


async def fetch_multiple_urls_async(urls: list[str]):
    """Параллельные запросы к нескольким URL."""
    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [fetch_url_async(session, url) for url in urls]
        return await asyncio.gather(*tasks)


async def main():
    urls = [
        "https://example.com/api/1",
        "https://example.com/api/2",
        "https://example.com/api/3",
    ]

    start = perf_counter()

    result = await fetch_multiple_urls_async(urls)

    end = perf_counter()

    print(f"Время работы: {end - start:.2f}")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
