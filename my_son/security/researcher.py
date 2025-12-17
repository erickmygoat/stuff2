"""
This module provides Security Research capabilities.
"""
import logging
import requests
from my_son.agent.llm import LLMClient
from my_son.brain.deep_learner import DeepLearner

class SecurityResearcher:
    """
    Identifies vulnerabilities and searches for exploits.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.llm = LLMClient()
        self.learner = DeepLearner()

    def scan_code_vulnerabilities(self, code_snippet):
        """
        Uses LLM to analyze code for security flaws.
        """
        print("Security: Scanning code for vulnerabilities...")

        system_prompt = (
            "You are an elite Security Researcher and Exploit Developer. "
            "Analyze the provided code for security vulnerabilities (e.g., SQLi, XSS, RCE, Buffer Overflows). "
            "Report the issues and suggest fixes."
        )

        report = self.llm.complete(code_snippet, system_prompt=system_prompt)
        return report

    def search_exploit_db(self, query):
        """
        Searches for known exploits related to the query.
        """
        print(f"Security: Searching for exploits regarding '{query}'...")

        # We can leverage the DeepLearner to "study" this exploit topic
        # querying specific sources.

        search_query = f"{query} exploit vulnerability CVE 0-day"

        # Use DeepLearner's search but filter/process differently if needed.
        # For MVP, we just reuse the study mechanism which prints a summary.
        # But here we probably want the raw data or a tailored report.

        # Let's manually use the internal search of DeepLearner if we want list of URLs,
        # or just ask it to study and return the summary.

        result = self.learner.study_topic(search_query)

        # Additionally, ask LLM to summarize the findings specifically for exploits
        context = self.llm.memory.retrieve_context(search_query)
        if context:
            summary_prompt = "Based on the recent research, list any specific CVEs or exploit PoCs found."
            summary = self.llm.complete(summary_prompt, system_prompt="You are a Security Researcher.")
            return f"{result}\n\nAnalysis:\n{summary}"

        return result
