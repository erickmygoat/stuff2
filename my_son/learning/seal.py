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

        # Also store in Vector DB
        for rule in rules:
            self.llm.memory.store_rule(rule, topic)

        print("SEAL: Knowledge integrated.")

    def consolidate_knowledge(self):
        """
        Meta-Optimization: Reads all rules, merges duplicates, refines logic.
        Surpasses SEAL by preventing rule bloat and catastrophic forgetting.
        """
        print("SEAL: Consolidating Knowledge Base...")
        if not os.path.exists(self.memory_path):
            return

        try:
            with open(self.memory_path, 'r') as f:
                data = json.load(f)
        except: return

        if not data: return

        # 1. Flatten Rules
        all_rules_text = ""
        for entry in data:
            all_rules_text += f"Topic: {entry['topic']}\nRules:\n" + "\n".join(entry['rules']) + "\n\n"

        # 2. Ask LLM to optimize
        prompt = f"""
        Current Knowledge Base:
        {all_rules_text[:10000]}

        Task:
        1. Merge duplicate rules.
        2. Remove obsolete or conflicting rules (keep the most recent/accurate).
        3. Refine wording for clarity and efficiency.
        4. Group by Topic.

        Output JSON:
        [
            {{"topic": "topic name", "rules": ["rule 1", "rule 2"]}},
            ...
        ]
        """
        try:
            response = self.llm.complete(prompt, system_prompt="You are a Knowledge Architect.")
            clean_resp = response.strip().replace("```json", "").replace("```", "")
            new_data = json.loads(clean_resp)

            # 3. Update JSON
            with open(self.memory_path, 'w') as f:
                json.dump(new_data, f, indent=2)

            # 4. Re-index Vector DB
            self.llm.memory.reset_rules()
            for entry in new_data:
                for rule in entry['rules']:
                    self.llm.memory.store_rule(rule, entry['topic'])

            print("SEAL: Knowledge Consolidated and Optimized.")

        except Exception as e:
            print(f"Consolidation Failed: {e}")
