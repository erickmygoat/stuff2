from my_son.learning.curriculum_generator import CurriculumGenerator
from my_son.learning.knowledge_ingestion import KnowledgeIngestionEngine
from my_son.learning.mastery_verification import MasteryVerificationProtocol
from my_son.learning.build_x_parser import BuildXParser
from my_son.learning.skill_generator import SkillGenerator

class LearningManager:
    """
    Manages the agent's learning process.
    """

    def __init__(self):
        # In a real application, the README content would be fetched dynamically.
        with open('build_your_own_x_readme.md', 'r') as f:
            readme_content = f.read()

        parser = BuildXParser(readme_content)
        curriculum_data = parser.parse()

        self.curriculum_generator = CurriculumGenerator(curriculum_data)
        self.knowledge_ingestion_engine = KnowledgeIngestionEngine()
        self.mastery_verification_protocol = MasteryVerificationProtocol()
        self.skill_generator = SkillGenerator()

    def start_learning_process(self, topic: str):
        """
        Starts the learning process for a given topic.
        """
        print(f"--- Starting learning process for topic: {topic} ---")

        # 1. Generate curriculum
        curriculum = self.curriculum_generator.generate_curriculum(topic)
        if not curriculum:
            print(f"No curriculum found for topic: {topic}")
            return

        print(f"Generated curriculum with {len(curriculum)} items.")

        # 2. Ingest knowledge from each item in the curriculum
        for item in curriculum:
            print(f"Ingesting knowledge from: {item['url']}")
            knowledge = self.knowledge_ingestion_engine.ingest_url(item['url'])

            if "Error ingesting URL" in knowledge:
                print(knowledge)
                continue

            # 3. Verify mastery
            verification = self.mastery_verification_protocol.verify_mastery(item['title'], knowledge)
            print(f"Mastery verification for '{item['title']}':")
            import json
            print(json.dumps(verification, indent=2))

            # 4. Generate a skill from the learned knowledge
            if verification.get("mastery_level") != "beginner":
                self.skill_generator.generate_skill(item['title'], knowledge)

        print(f"--- Learning process for topic: {topic} complete ---")

if __name__ == '__main__':
    learning_manager = LearningManager()
    learning_manager.start_learning_process("Git")
