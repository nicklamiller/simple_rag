import logging
import os
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

from simple_rag.utils import quiet_httpx_logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def fetch_html_as_raw_text(
    source_urls: list[str] | None = None,
    target_folder: str | Path = Path("/tmp/raw_docs/"),
) -> None:
    """Takes input URLs and saves them to a target folder. Returns fp"""
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
        logger.info(f"Created target folder: {target_folder}")
    if source_urls is None:
        source_urls = [
            "https://en.wikipedia.org/wiki/Retrieval-augmented_generation",
            "https://en.wikipedia.org/wiki/Vector_database",
            "https://en.wikipedia.org/wiki/Information_retrieval",
        ]
    with quiet_httpx_logging():
        for url in source_urls:
            response = httpx.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                paragraphs = soup.find_all("p")
                plain_text = "\n".join([p.get_text() for p in paragraphs])
                file_path = Path(target_folder) / f"{url.split('/')[-1]}.txt"
                with open(file_path, "w") as f:
                    f.write(plain_text)
                logger.info(f"Successfully downloaded {url} to {file_path}.")
            else:
                print(f"Failed to download {url}")
    logger.info("Done fetching HTML's as raw text.")


def run_rag_pipeline():
    """RAG pipeline."""
    fetch_html_as_raw_text()


if __name__ == "__main__":
    run_rag_pipeline()
