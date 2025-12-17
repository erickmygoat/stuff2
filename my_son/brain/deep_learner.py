"""
This module provides the Deep Learning capabilities (Web Search & Scraping).
"""
import logging
import requests
import os
import shutil
from bs4 import BeautifulSoup
from my_son.brain.memory import Memory
from my_son.agent.tool_library import ToolLibrary
from my_son.security.analyzer import MalwareAnalyzer

class DeepLearner:
    """
    Acquires knowledge from the web and stores it in memory.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.memory = Memory()
        self.tool_library = ToolLibrary()
        self.malware_analyzer = MalwareAnalyzer()

    def study_topic(self, topic):
        """
        Researches a topic and updates memory.
        """
        print(f"DeepLearner: Researching '{topic}'...")

        # Identify high-risk topics for Safe Mode
        safe_mode = False
        if "malware" in topic.lower() or "virus" in topic.lower() or "exploit" in topic.lower():
            safe_mode = True
            print("DeepLearner: High-risk topic detected. Enabling Safe Mode (Analysis Only).")

        # Special case: GitHub Topic URL
        if "github.com/topics/" in topic:
            return self.learn_from_github_topic(topic, safe_mode=safe_mode)

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

    def learn_from_github_topic(self, url, safe_mode=False):
        """
        Scrapes a GitHub topic page, clones top repositories, and ingests them.
        If safe_mode is True, repos are analyzed and deleted, NOT installed as tools.
        """
        print(f"DeepLearner: Learning from GitHub topic: {url}...")

        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')

            # Find repo links (same logic as before)
            repos = []
            for article in soup.find_all('article', class_='border rounded-2 box-shadow-bg-gray-mktg my-4'):
                link = article.find('a', class_='text-bold wb-break-word')
                if link:
                    repos.append(f"https://github.com{link.get('href')}")

            if not repos:
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href and href.count('/') == 2 and not href.startswith('/topics') and not href.startswith('/features'):
                         full_url = f"https://github.com{href}"
                         if full_url not in repos:
                             repos.append(full_url)

            top_repos = repos[:5]
            print(f"DeepLearner: Found repos: {top_repos}")

            results = []
            for repo_url in top_repos:
                # If Safe Mode, we clone to a temp dir, analyze, ingest report, and delete.
                if safe_mode:
                    print(f"DeepLearner: Analyzing {repo_url} for threat signatures...")
                    try:
                        # Manual clone to temp
                        repo_name = repo_url.split("/")[-1]
                        temp_path = f"temp_analysis/{repo_name}"
                        if os.path.exists(temp_path):
                            shutil.rmtree(temp_path)

                        # Use ToolLibrary's logic or git directly? ToolLibrary puts in tools/
                        # We don't want it in tools/. Let's clone manually.
                        # Assuming gitpython is available since ToolLibrary uses it.
                        import git
                        git.Repo.clone_from(repo_url, temp_path)

                        # Run Analyzer
                        report = self.malware_analyzer.analyze_repo(temp_path)

                        # Ingest Report
                        report_text = f"Threat Analysis for {repo_name}:\n{report}"
                        self.memory.store_memory(report_text, metadata={"source": repo_url, "type": "threat_analysis"})

                        results.append(f"{repo_name} (Analyzed)")

                        # Cleanup
                        shutil.rmtree(temp_path)

                    except Exception as e:
                        print(f"DeepLearner: Failed to analyze {repo_url}: {e}")
                else:
                    # Normal Mode: Install as Tool
                    tool_path = self.tool_library.install_from_github(repo_url)
                    if tool_path:
                        print(f"DeepLearner: Ingesting knowledge from {tool_path}...")
                        self.memory.ingest_bulk_folder(tool_path)
                        results.append(repo_url)

            return f"I have acquired new knowledge. Processed {len(results)} repositories from {url}."

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
