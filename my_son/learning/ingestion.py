import requests
from bs4 import BeautifulSoup
from googlesearch import search

class KnowledgeIngestionEngine:
    """
    A module for autonomously finding, downloading, and processing information
    from online sources.
    """
    def __init__(self, num_results=5):
        """
        Initializes the KnowledgeIngestionEngine.

        Args:
            num_results (int): The number of search results to retrieve.
        """
        self.num_results = num_results

    def search_online(self, query):
        """
        Performs a Google search for the given query.

        Args:
            query (str): The search query.

        Returns:
            list: A list of URLs from the search results.
        """
        print(f"Searching online for: '{query}'")
        try:
            return list(search(query, num=self.num_results))
        except Exception as e:
            print(f"An error occurred during search: {e}")
            return []

    def scrape_website(self, url):
        """
        Scrapes the text content of a given URL.

        Args:
            url (str): The URL of the website to scrape.

        Returns:
            str: The text content of the website, or an empty string if scraping fails.
        """
        print(f"Scraping content from: {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()

            # Get text and clean it up
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\\n'.join(chunk for chunk in chunks if chunk)

            return text
        except requests.RequestException as e:
            print(f"Error scraping {url}: {e}")
            return ""

    def ingest(self, query):
        """
        Performs a search and scrapes the content of the top results.

        Args:
            query (str): The topic to learn about.

        Returns:
            dict: A dictionary where keys are URLs and values are the scraped content.
        """
        urls = self.search_online(query)
        ingested_data = {}
        for url in urls:
            content = self.scrape_website(url)
            if content:
                ingested_data[url] = content
        return ingested_data

# Example Usage:
if __name__ == '__main__':
    engine = KnowledgeIngestionEngine()

    # Let's learn about a fundamental computer science topic
    topic = "Quicksort algorithm"
    knowledge_base = engine.ingest(topic)

    print(f"\\n--- Knowledge Ingested for '{topic}' ---")
    for url, content in knowledge_base.items():
        print(f"\\n--- Source: {url} ---")
        # Print the first 500 characters of the content
        print(content[:500] + "...")
