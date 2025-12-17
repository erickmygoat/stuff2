"""
This module provides Security Research capabilities.
"""
import logging
import requests
import os
from my_son.agent.llm import LLMClient
from my_son.brain.deep_learner import DeepLearner
from my_son.security.analyzer import MalwareAnalyzer

class SecurityResearcher:
    """
    Identifies vulnerabilities and searches for exploits.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.llm = LLMClient()
        self.learner = DeepLearner()
        self.analyzer = MalwareAnalyzer()

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

    def analyze_repository(self, repo_path):
        """
        Runs the static malware analyzer on a local repository.
        """
        if not os.path.exists(repo_path):
            return {"error": "Path does not exist."}

        print(f"Security: Analyzing repository at {repo_path}...")
        report = self.analyzer.analyze_repo(repo_path)

        # Optionally enhance with LLM insight
        if report["findings"]:
            findings_text = "\n".join(report["findings"])
            analysis = self.llm.complete(
                findings_text,
                system_prompt="Analyze these findings from a static code scan. Explain the potential threat impact."
            )
            report["llm_analysis"] = analysis

        return report

    def search_exploit_db(self, query):
        """
        Searches for known exploits related to the query.
        """
        print(f"Security: Searching for exploits regarding '{query}'...")

        search_query = f"{query} exploit vulnerability CVE 0-day"

        result = self.learner.study_topic(search_query)

        context = self.llm.memory.retrieve_context(search_query)
        if context:
            summary_prompt = "Based on the recent research, list any specific CVEs or exploit PoCs found."
            summary = self.llm.complete(summary_prompt, system_prompt="You are a Security Researcher.")
            return f"{result}\n\nAnalysis:\n{summary}"

        return result
