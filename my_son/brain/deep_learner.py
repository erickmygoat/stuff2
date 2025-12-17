"""
This module provides the Deep Learning capabilities (Web Search & Scraping).
"""
import logging
import requests
from bs4 import BeautifulSoup
from my_son.brain.memory import Memory

class DeepLearner:
    """
    Acquires knowledge from the web and stores it in memory.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.memory = Memory()
        # In a real app, use a proper search API (Google/Bing/DuckDuckGo).
        # For MVP/Sandbox, we'll simulate search or use a generic scraping approach if URL provided.
        # Since I cannot easily use a Search API without a key, I will rely on a "Simulated Search"
        # or ask the user for URLs if "topic" looks like a URL.
        # But the prompt implies "instant mastery", so I'll try to implement a basic DuckDuckGo scraper
        # or just fallback to scraping provided URLs.

    def study_topic(self, topic):
        """
        Researches a topic and updates memory.
        """
        print(f"DeepLearner: Researching '{topic}'...")

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

    def _search_web(self, query):
        """
        Simulates a web search.
        """
        # If query is a URL, just return it
        if query.startswith("http"):
            return [query]

        # Basic DuckDuckGo HTML scrape (Fragile, but free/MVP)
        # Or use a placeholder list for the sandbox environment if internet is restricted in a specific way.
        # Sandbox has 'google_search' tool available! I should use that if I were the agent calling tools.
        # But here I am writing the *code* for the agent. The agent doesn't have the 'google_search' tool
        # embedded in its python code unless I implement it.

        # Implementation of a simple DDG scraper for MVP:
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

            # Remove script/style
            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text()

            # Clean whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            return text
        except Exception as e:
            print(f"Scrape error: {e}")
            return None
