"""
The high-level program structure will look like this:

- Read a sequence of URLs from a local file, urls.txt.

- Send GET requests for the URLs and decode the resulting content. If this fails, stop there for a URL.

- Search for the URLs within href tags in the HTML of the responses.

- Write the results to foundurls.txt.

Do all of the above as asynchronously and concurrently as possible.
(Use aiohttp for the requests, and aiofiles for the file-appends.
These are two primary examples of IO that are well-suited for the async IO model.)
"""

from typing import List
from pathlib import Path
import time
import asyncio
from urllib.parse import urlparse

import aiohttp
import aiofiles
from bs4 import BeautifulSoup


URLS_FILE_PATH = Path(__file__).parent.resolve() / "urls.txt"
FOUND_URLS_FILE_PATH = Path(__file__).parent.resolve() / "foundurls.txt"


def get_urls_from_file(urls_file_path: Path = URLS_FILE_PATH) -> List[str]:
    with open(urls_file_path, 'r') as f:
        return [url.strip("\n") for url in f.readlines()]


def is_valid_url(text: str) -> bool:
    parsed_url = urlparse(text)
    return all([parsed_url.scheme, parsed_url.netloc])


async def find_urls_in_href_tags(url: str, session: aiohttp.ClientSession) -> List[str]:
    async with session.get(url) as response:
        status = response.status
        print(f"url {url} responded with status {status}")
        html = await response.text()
    soup = BeautifulSoup(html, 'html.parser')
    urls = [tag['href'] for tag in soup.find_all('a', href=True) if is_valid_url(tag['href'])]
    return urls


async def write_found_urls(urls: List[str], file_path: Path = FOUND_URLS_FILE_PATH):
    async with aiofiles.open(file_path, 'a') as f:
        await f.writelines([url + '\n' for url in urls])


async def find_and_write_referenced_urls(url: str, session: aiohttp.ClientSession):
    urls = await asyncio.create_task(find_urls_in_href_tags(url, session))
    await write_found_urls(urls)


async def main():
    start = time.perf_counter()
    urls = get_urls_from_file()
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[asyncio.create_task(find_and_write_referenced_urls(url, session)) for url in urls])
    end = time.perf_counter() - start
    print(f"urls parsed in {end}s")


asyncio.run(main())

