

class CurriculumGenerator:
    """
    A module for creating structured learning plans for any given topic.
    """
    def __init__(self):
        """
        Initializes the CurriculumGenerator with a set of predefined curricula.
        """
        self.curricula = {
            "python": [
                "1. Python Fundamentals (Syntax, Data Types, Control Flow)",
                "2. Intermediate Python (Functions, Classes, Modules)",
                "3. Advanced Python (Decorators, Generators, Metaclasses)",
                "4. Standard Library Deep Dive (os, sys, collections, etc.)",
                "5. Web Development (Flask/Django)",
                "6. Data Science & ML (NumPy, Pandas, Scikit-learn)",
                "7. Concurrency & Parallelism (asyncio, threading, multiprocessing)"
            ],
            "c++": [
                "1. C++ Basics (Syntax, Pointers, Memory Management)",
                "2. Object-Oriented Programming (Classes, Inheritance, Polymorphism)",
                "3. Standard Template Library (STL)",
                "4. Advanced C++ (Templates, RAII, Smart Pointers)",
                "5. Concurrency in C++ (std::thread, std::mutex)",
                "6. Build Systems & Toolchains (CMake, Make)",
                "7. Performance Optimization & Low-Level Programming"
            ],
            "java": [
                "1. Java Core Concepts (JVM, Syntax, OOP)",
                "2. Java Collections Framework",
                "3. Concurrency and Multithreading",
                "4. Java I/O and Networking",
                "5. Build Tools (Maven, Gradle)",
                "6. Spring Framework (Core, Boot, MVC)",
                "7. JVM Internals and Performance Tuning"
            ]
        }

    def generate_curriculum(self, topic):
        """
        Generates a curriculum for the given topic.

        Args:
            topic (str): The topic to generate a curriculum for.

        Returns:
            list: A list of curriculum steps, or a default message if the topic is not found.
        """
        return self.curricula.get(topic.lower(), ["No predefined curriculum found. The agent will need to generate one dynamically."])

# Example Usage:
if __name__ == '__main__':
    generator = CurriculumGenerator()

    topic = "Python"
    python_curriculum = generator.generate_curriculum(topic)

    print(f"--- Generated Curriculum for '{topic}' ---")
    for step in python_curriculum:
        print(step)

    topic = "Go"
    go_curriculum = generator.generate_curriculum(topic)

    print(f"\\n--- Generated Curriculum for '{topic}' ---")
    for step in go_curriculum:
        print(step)
