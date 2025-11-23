from typing import List
def url_scraper(
    docs_url: str = "https://docs.aws.amazon.com/",
    repo_url: str = "https://github.com/aws-samples/",
    website_url: str = "https://aws.amazon.com/",
) -> List[str]:
    """Generates a list of AWS-related URLs to scrape.

    Args:
        docs_url: Base URL for AWS documentation.
        repo_url: URL to AWS sample repositories.
        website_url: URL to the AWS main site.

    Returns:
        List of URLs to scrape for AWS knowledge base generation.
    """

    all_urls = [website_url, docs_url, repo_url]

    print(f"Using {len(all_urls)} predefined URLs to avoid async crawling issues")

    return all_urls
