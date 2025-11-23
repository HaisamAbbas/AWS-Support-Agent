import asyncio
import logging
import aiohttp
from typing import List, Set, Tuple
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from ratelimit import limits, sleep_and_retry
import json
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

CALLS = 10
PERIOD = 60

def normalize_url(url: str) -> str:
    """
    Normalize a URL by removing fragments, query parameters, and trailing slashes.

    Args:
        url (str): The URL to normalize.

    Returns:
        str: The normalized URL.
    """
    parsed = urlparse(url)
    return parsed._replace(fragment="", query="").geturl().rstrip("/")


def is_valid_url(url: str, base: str) -> bool:
    """
    Check if the given URL is valid, belongs to the base domain, and is not a non-HTML resource.

    Args:
        url (str): The URL to check (e.g., 'https://aws.amazon.com/ec2/').
        base (str): The base domain (e.g., 'aws.amazon.com').

    Returns:
        bool: True if the URL is valid and belongs to the base domain, False otherwise.

    Examples:
        >>> is_valid_url("https://aws.amazon.com/ec2/", "aws.amazon.com")
        True
        >>> is_valid_url("https://example.com", "aws.amazon.com")
        False
        >>> is_valid_url("https://aws.amazon.com/file.pdf", "aws.amazon.com")
        False
    """
    if not url.startswith(("http://", "https://")):
        return False
    parsed = urlparse(url)
    if not (parsed.netloc and parsed.netloc.endswith(base)):
        return False

    if parsed.path.endswith((".pdf", ".jpg", ".png", ".js", ".css")):
        return False
    return True


async def is_allowed_by_robots(url: str, session: aiohttp.ClientSession) -> bool:
    """
    Check if crawling the URL is allowed by the site's robots.txt.

    Args:
        url (str): The URL to check.
        session (aiohttp.ClientSession): The HTTP session for async requests.

    Returns:
        bool: True if crawling is allowed, False otherwise.
    """
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = RobotFileParser()
    try:
        async with session.get(robots_url, timeout=10) as response:
            if response.status == 200:
                rp.parse((await response.text()).splitlines())
                return rp.can_fetch("*", url)
            else:
                logger.warning(f"Could not fetch robots.txt for {url}: HTTP {response.status}")
                return True 
    except Exception as e:
        logger.warning(f"Error fetching robots.txt for {url}: {e}")
        return True
    

@sleep_and_retry
@limits(calls=CALLS, period=PERIOD)
async def get_all_links(url: str, base: str, session: aiohttp.ClientSession) -> List[str]:
    """
    Retrieve all valid links from a given URL with the same base asynchronously.

    Args:
        url (str): The page URL to retrieve links from.
        base (str): The base domain (e.g., 'aws.amazon.com').
        session (aiohttp.ClientSession): The HTTP session for async requests.

    Returns:
        List[str]: A list of valid links with the same base.
    """
    start_time = asyncio.get_event_loop().time()
    links = []
    try:
        if not await is_allowed_by_robots(url, session):
            logger.info(f"Crawling disallowed by robots.txt: {url}")
            return links

        async with session.get(url, timeout=10) as response:
            if response.status != 200:
                logger.error(f"Failed to fetch {url}: HTTP {response.status}")
                return links
            soup = BeautifulSoup(await response.text(), "html.parser")
            for link in soup.find_all("a", href=True):
                href = link["href"]
                full_url = urljoin(url, href)
                cleaned_url = normalize_url(full_url)
                if is_valid_url(cleaned_url, base):
                    links.append(cleaned_url)
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
    
    logger.debug(f"Fetched {len(links)} links from {url} in {asyncio.get_event_loop().time() - start_time:.2f} seconds")
    return links


async def crawl(url: str, base: str, session: aiohttp.ClientSession, visited: Set[str] = None, visited_file: str = "visited.json") -> Set[str]:
    """
    Asynchronously crawl pages, retrieving all valid links with the same base.

    Args:
        url (str): The starting URL.
        base (str): The base domain.
        session (aiohttp.ClientSession): The HTTP session for async requests.
        visited (Set[str]): A set of already visited URLs.
        visited_file (str): File to persist visited URLs.

    Returns:
        Set[str]: A set of all valid links with the same base.
    """
    if visited is None:
        try:
            with open(visited_file, "r") as f:
                visited = set(json.load(f))
        except FileNotFoundError:
            visited = set()

    normalized_url = normalize_url(url)
    if normalized_url in visited:
        return visited

    visited.add(normalized_url)
    links = await get_all_links(normalized_url, base, session)

    tasks = []
    for link in links:
        if normalize_url(link) not in visited:
            tasks.append(crawl(link, base, session, visited, visited_file))
    
    await asyncio.gather(*tasks, return_exceptions=True)
    
    with open(visited_file, "w") as f:
        json.dump(list(visited), f)
    
    return visited


async def get_all_pages(url: str) -> List[str]:
    """
    Retrieve all pages with the same base as the given URL.

    Args:
        url (str): The root page URL.

    Returns:
        List[str]: A list of all discovered pages with the same base.
    """
    if not url.startswith(("http://", "https://")):
        logger.error(f"Invalid URL scheme: {url}")
        return []
    
    logger.debug(f"Scraping all pages from {url}...")
    base_url = urlparse(url).netloc
    async with aiohttp.ClientSession() as session:
        pages = await crawl(url, base_url, session)
    logger.debug(f"Found {len(pages)} pages.")
    logger.debug("Done scraping pages.")
    return list(pages)


@sleep_and_retry
@limits(calls=CALLS, period=PERIOD)
async def get_repo_docs(repo_url: str, session: aiohttp.ClientSession) -> Tuple[List[str], List[str]]:
    """
    Retrieve folder and README links from a GitHub repository using the GitHub API.

    Args:
        repo_url (str): The URL of the GitHub repository.
        session (aiohttp.ClientSession): The HTTP session for async requests.

    Returns:
        Tuple[List[str], List[str]]: Folder links and README links.
    """
    repo_path = urlparse(repo_url).path
    api_url = f"https://api.github.com/repos{repo_path}/contents"
    headers = {"Accept": "application/vnd.github+json"}
    
    try:
        async with session.get(api_url, headers=headers, timeout=10) as response:
            if response.status != 200:
                logger.error(f"Failed to fetch {api_url}: HTTP {response.status}")
                return [], []
            contents = await response.json()
            folder_links = [item["html_url"] for item in contents if item["type"] == "dir"]
            readme_links = [item["html_url"] for item in contents if item["name"].lower() == "readme.md"]
            return folder_links, readme_links
    except Exception as e:
        logger.error(f"Failed to fetch {api_url}: {e}")
        return [], []
    

async def get_nested_readme_urls(repo_url: str) -> List[str]:
    """
    Retrieve all nested README links from a GitHub repository.

    Args:
        repo_url (str): The GitHub repository URL.

    Returns:
        List[str]: All nested README links.
    """
    async with aiohttp.ClientSession() as session:
        folder_links, readme_links = await get_repo_docs(repo_url, session)
        tasks = [get_repo_docs(folder_link, session) for folder_link in folder_links]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, tuple):
                _, nested_readme_links = result
                readme_links.extend(nested_readme_links)
    
    return readme_links

