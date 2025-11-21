from typing import List, Dict
from my_son.learning.build_x_parser import BuildXParser

class CurriculumGenerator:
    """
    Generates a structured learning curriculum for a given topic.
    """

    def __init__(self, curriculum: Dict[str, List[Dict[str, str]]]):
        """
        Initializes the CurriculumGenerator.

        :param curriculum: The curriculum parsed from the 'Build Your Own X' repository.
        """
        self.curriculum = curriculum

    def generate_curriculum(self, topic: str) -> List[Dict[str, str]]:
        """
        Generates a curriculum for a given topic.

        :param topic: The topic to generate a curriculum for.
        :return: A list of tutorials for the given topic.
        """
        if topic in self.curriculum:
            return self.curriculum[topic]
        else:
            # Simple keyword matching as a fallback
            for key in self.curriculum:
                if topic.lower() in key.lower():
                    return self.curriculum[key]
            return []

if __name__ == '__main__':
    # Test case for the CurriculumGenerator
    with open('build_your_own_x_readme.md', 'r') as f:
        readme_content = f.read()

    parser = BuildXParser(readme_content)
    parsed_curriculum = parser.parse()

    generator = CurriculumGenerator(parsed_curriculum)

    # Test with a specific topic
    git_curriculum = generator.generate_curriculum("Git")
    print("Curriculum for Git:")
    import json
    print(json.dumps(git_curriculum, indent=2))

    # Test with a fallback topic
    docker_curriculum = generator.generate_curriculum("Docker")
    print("\\nCurriculum for Docker:")
    print(json.dumps(docker_curriculum, indent=2))
