import json
import os
import logging
import time
from my_son.agent.llm import LLMClient

class SEALEngine:
    """
    Self-Adapting Engine based on the SEAL framework concepts.
    Generates Self-Edits (Rules/Knowledge), Evaluates them, and Updates the System.
    """
    def __init__(self, memory_path="brain_memory/learned_rules.json"):
        self.llm = LLMClient()
        self.memory_path = memory_path
        self.logger = logging.getLogger(__name__)

        if not os.path.exists(os.path.dirname(self.memory_path)):
            os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)

    def perform_adaptation(self, topic, content):
        """
        Main loop: Research -> Self-Edit -> Evaluate -> Commit.
        """
        print(f"SEAL: Initiating adaptation for '{topic}'...")

        # 1. Generate Self-Edit (Candidate Rules & Synthetic Data)
        rules, qa_pairs = self._generate_self_edit(topic, content)
        if not rules:
            print("SEAL: Failed to generate self-edit.")
            return False

        # 2. Evaluate
        score = self._evaluate_edit(rules, qa_pairs)
        print(f"SEAL: Evaluation Score: {score}/100")

        # 3. Commit if good enough
        if score > 60: # Threshold (lenient for now)
            self._commit_update(topic, rules)
            return True
        else:
            print("SEAL: Update rejected (Score too low).")
            return False

    def _generate_self_edit(self, topic, content):
        prompt = f"""
        Topic: {topic}
        Source Content: {content[:4000]}...

        Task:
        1. Distill this content into concise behavioral RULES or KNOWLEDGE POINTS for an AI agent.
        2. Generate 3 Question-Answer pairs to test this knowledge.

        Format as JSON:
        {{
            "rules": ["rule 1", "rule 2"],
            "qa_pairs": [
                {{"q": "question 1", "a": "answer 1"}},
                ...
            ]
        }}
        """
        try:
            response = self.llm.complete(prompt, system_prompt="You are a Knowledge Distillation Engine. Output JSON only.")
            # Clean json
            clean_resp = response.strip()
            if clean_resp.startswith("```json"):
                clean_resp = clean_resp.replace("```json", "").replace("```", "")

            data = json.loads(clean_resp)
            return data.get("rules", []), data.get("qa_pairs", [])
        except Exception as e:
            print(f"SEAL Gen Error: {e}")
            return None, None

    def _evaluate_edit(self, rules, qa_pairs):
        """
        Test the model's ability to answer Qs using the new rules.
        """
        correct = 0
        rules_str = "\n".join([f"- {r}" for r in rules])

        if not qa_pairs: return 0

        for qa in qa_pairs:
            # Ask LLM with rules injected
            prompt = f"""
            System Rules:
            {rules_str}

            Question: {qa['q']}
            """
            response = self.llm.complete(prompt, system_prompt="You are an agent following specific rules.")

            # Grader
            grade_prompt = f"""
            Question: {qa['q']}
            Reference Answer: {qa['a']}
            Agent Answer: {response}

            Is the Agent Answer correct based on the Reference? (YES/NO)
            """
            grade = self.llm.complete(grade_prompt, max_tokens=5).strip().upper()
            if "YES" in grade:
                correct += 1

        return (correct / len(qa_pairs)) * 100

    def _commit_update(self, topic, rules):
        print(f"SEAL: Committing {len(rules)} new rules for '{topic}'.")
        current_rules = []
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, 'r') as f:
                    current_rules = json.load(f)
            except: pass

        # Append new rules
        new_entry = {
            "topic": topic,
            "rules": rules,
            "timestamp": time.time()
        }
        current_rules.append(new_entry)

        with open(self.memory_path, 'w') as f:
            json.dump(current_rules, f, indent=2)

        print("SEAL: Knowledge integrated.")
