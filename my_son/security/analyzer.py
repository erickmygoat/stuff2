"""
This module performs static analysis on code to identify potential security threats and malicious patterns.
"""
import ast
import os
import logging

class MalwareAnalyzer:
    """
    Analyzes code for malicious patterns using AST.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Define suspicious calls and imports
        self.suspicious_calls = {
            'system', 'popen', 'run', 'call', 'spawn', # subprocess/os execution
            'connect', 'bind', 'listen', 'accept', # networking
            'eval', 'exec', # dynamic execution
            'base64', 'b64decode', # obfuscation indicators
            'requests.post', 'urlopen' # exfiltration indicators
        }
        self.suspicious_imports = {
            'subprocess', 'os', 'socket', 'requests', 'urllib', 'base64', 'cryptography', 'pynput'
        }

    def analyze_repo(self, repo_path):
        """
        Scans a repository for suspicious patterns.
        Returns a Threat Report.
        """
        report = {
            "repo": repo_path,
            "risk_score": 0,
            "findings": [],
            "capabilities": set()
        }

        print(f"Analyzer: Scanning {repo_path}...")

        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    self._scan_file(file_path, report)

        # Summarize
        if report["risk_score"] > 5:
            report["verdict"] = "High Risk / Malicious"
        elif report["risk_score"] > 0:
            report["verdict"] = "Suspicious / Dual Use"
        else:
            report["verdict"] = "Benign"

        return report

    def _scan_file(self, file_path, report):
        """
        Parses a single file.
        """
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            tree = ast.parse(content)

            for node in ast.walk(tree):
                # Check Imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in self.suspicious_imports:
                            report["findings"].append(f"{os.path.basename(file_path)}: Imports '{alias.name}'")
                            report["risk_score"] += 1
                            report["capabilities"].add(f"Uses {alias.name}")

                elif isinstance(node, ast.ImportFrom):
                    if node.module in self.suspicious_imports:
                        report["findings"].append(f"{os.path.basename(file_path)}: Imports from '{node.module}'")
                        report["risk_score"] += 1
                        report["capabilities"].add(f"Uses {node.module}")

                # Check Function Calls
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Attribute):
                        if node.func.attr in self.suspicious_calls:
                            report["findings"].append(f"{os.path.basename(file_path)}: Calls '{node.func.attr}'")
                            report["risk_score"] += 2
                            report["capabilities"].add(f"Calls {node.func.attr}")
                    elif isinstance(node.func, ast.Name):
                        if node.func.id in self.suspicious_calls:
                            report["findings"].append(f"{os.path.basename(file_path)}: Calls '{node.func.id}'")
                            report["risk_score"] += 2
                            report["capabilities"].add(f"Calls {node.func.id}")

        except SyntaxError:
            pass # Skip invalid python files
        except Exception as e:
            self.logger.warning(f"Failed to scan {file_path}: {e}")
