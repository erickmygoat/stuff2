import requests
from bs4 import BeautifulSoup

class KnowledgeIngestionEngine:
    """
    Fetches and extracts knowledge from various sources.
    """

    def __init__(self):
        pass

    def ingest_url(self, url: str) -> str:
        """
        Ingests knowledge from a single URL.

        :param url: The URL to ingest.
        :return: The text content of the URL.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script_or_style in soup(['script', 'style']):
                script_or_style.decompose()

            # Get text and clean it up
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\\n'.join(chunk for chunk in chunks if chunk)

            return text
        except requests.exceptions.RequestException as e:
            return f"Error ingesting URL {url}: {e}"
