"""
This module provides the Deep Learning capabilities (Web Search & Scraping).
"""
import logging
import requests
from bs4 import BeautifulSoup
from my_son.brain.memory import Memory
from my_son.agent.tool_library import ToolLibrary

class DeepLearner:
    """
    Acquires knowledge from the web and stores it in memory.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.memory = Memory()
        self.tool_library = ToolLibrary()

    def study_topic(self, topic):
        """
        Researches a topic and updates memory.
        """
        print(f"DeepLearner: Researching '{topic}'...")

        # Special case: GitHub Topic URL
        if "github.com/topics/" in topic:
            return self.learn_from_github_topic(topic)

        # 1. Search for URLs
        urls = self._search_web(topic)
        if not urls:
             return f"I could not find any sources for '{topic}'."

        # 2. Scrape & Ingest
        count = 0
        for url in urls[:5]: # Top 5
            try:
                print(f"DeepLearner: Reading {url}...")
                content = self._scrape_url(url)
                if content:
                    # Store in memory
                    self.memory.store_memory(
                        content,
                        metadata={"source": url, "topic": topic, "type": "research"}
                    )
                    count += 1
            except Exception as e:
                self.logger.warning(f"Failed to process {url}: {e}")

        return f"I have researched '{topic}', read {count} sources, and updated my internal knowledge base."

    def learn_from_github_topic(self, url):
        """
        Scrapes a GitHub topic page, clones top repositories, and ingests them.
        """
        print(f"DeepLearner: Learning from GitHub topic: {url}...")

        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')

            # Find repo links
            repos = []
            for article in soup.find_all('article', class_='border rounded-2 box-shadow-bg-gray-mktg my-4'):
                link = article.find('a', class_='text-bold wb-break-word')
                if link:
                    href = link.get('href')
                    full_url = f"https://github.com{href}"
                    repos.append(full_url)

            # Fallback scraper if class names changed
            if not repos:
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href and href.count('/') == 2 and not href.startswith('/topics') and not href.startswith('/features'):
                         # Heuristic for /user/repo
                         full_url = f"https://github.com{href}"
                         if full_url not in repos:
                             repos.append(full_url)

            # Limit to top 5 to avoid overloading
            top_repos = repos[:5]
            print(f"DeepLearner: Found repos: {top_repos}")

            results = []
            for repo_url in top_repos:
                tool_path = self.tool_library.install_from_github(repo_url)
                if tool_path:
                    # Ingest the tool's documentation/code
                    print(f"DeepLearner: Ingesting knowledge from {tool_path}...")
                    self.memory.ingest_bulk_folder(tool_path)
                    results.append(repo_url)

            return f"I have acquired new skills. Installed and studied {len(results)} tools from {url}."

        except Exception as e:
            self.logger.error(f"GitHub learning failed: {e}")
            return f"Error learning from GitHub: {e}"

    def _search_web(self, query):
        """
        Simulates a web search.
        """
        if query.startswith("http"):
            return [query]

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            url = f"https://html.duckduckgo.com/html/?q={query}"
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')

            results = []
            for link in soup.find_all('a', class_='result__a'):
                href = link.get('href')
                if href and href.startswith('http'):
                    results.append(href)
            return results
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            return []

    def _scrape_url(self, url):
        """
        Fetches and extracts text from a URL.
        """
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')

            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text()

            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            return text
        except Exception as e:
            print(f"Scrape error: {e}")
            return None
