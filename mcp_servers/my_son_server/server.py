from arcade_mcp_server import MCPApp
from typing import Annotated
import json
from core_agent.system_monitor import SystemMonitor
from core_agent.learning.ingestion import KnowledgeIngestionEngine
from core_agent.learning.curriculum import CurriculumGenerator
from core_agent.learning.mastery import MasteryVerificationProtocol
from core_agent.learning.osint import OSINTClient
from core_agent.engineering.gpt_engineer import gen_code, improve_fn
from core_agent.prompting.gpt_engineer import GptEngineerPromptGenerator
from core_agent.files_dict import FilesDict
from core_agent.ai import AI
from core_agent.memory import BaseMemory

app = MCPApp(name="my_son_server", version="1.0.0", log_level="DEBUG")

@app.tool
def get_status() -> Annotated[str, "The current status of the 'My Son' agent."]:
    """Returns the current status of the agent."""
    return "Status: Online and operational."

@app.tool
async def learn(topic: Annotated[str, "The topic for the agent to learn about."]) -> Annotated[str, "A summary of the learning process."]:
    """Initiates the learning protocol for a given topic."""
    print(f"--- Initiating Learning Protocol for '{topic}' ---")
    curriculum_gen = CurriculumGenerator()
    curriculum = curriculum_gen.generate_curriculum(topic)
    print("Generated Curriculum:")
    for step in curriculum:
        print(f"  - {step}")
    ingestion_engine = KnowledgeIngestionEngine()
    knowledge_base = await ingestion_engine.ingest(topic)
    mastery_protocol = MasteryVerificationProtocol()
    summary = ""
    for i, (url, content) in enumerate(knowledge_base.items()):
        if i >= 2:
            break
        print(f"\\n--- Verifying understanding of {url} ---")
        summary += mastery_protocol.summarize_text(content) + "\\n"
    return summary

@app.tool
async def master_language(language: Annotated[str, "The programming language for the agent to master."]) -> Annotated[str, "A summary of the learning process."]:
    """Initiates the language mastery protocol for a given programming language."""
    print(f"--- Initiating Language Mastery Protocol for '{language}' ---")
    curriculum_gen = CurriculumGenerator()
    curriculum = curriculum_gen.generate_curriculum(language)
    print("Generated Curriculum:")
    for step in curriculum:
        print(f"  - {step}")
    ingestion_engine = KnowledgeIngestionEngine()
    knowledge_base = await ingestion_engine.ingest(f"{language} programming language")
    mastery_protocol = MasteryVerificationProtocol()
    summary = ""
    for i, (url, content) in enumerate(knowledge_base.items()):
        if i >= 1:
            break
        print(f"\\n--- Verifying understanding of {url} ---")
        summary += mastery_protocol.summarize_text(content) + "\\n"
    print(f"\\n--- Analyzing practical examples of '{language}' code ---")
    await ingestion_engine.ingest(f"open source {language} projects github")
    return summary

@app.tool
def system_snapshot() -> Annotated[str, "A snapshot of the system's current resource usage."]:
    """Returns a snapshot of the system's current resource usage."""
    return json.dumps(SystemMonitor().get_snapshot())

@app.tool
def execute_code(code: Annotated[str, "The Python code to execute."]) -> Annotated[str, "The result of the code execution."]:
    """Executes Python code in a sandboxed environment."""
    from core_agent.code_executor import execute_code as exec_code
    return json.dumps(exec_code(code))

# TODO: Implement agent protocol integration with Auto-GPT
#
# @app.tool
# async def autogpt(goal: Annotated[str, "The high--level goal for the Auto-GPT agent to achieve."]) -> Annotated[str, "The result of the Auto-GPT agent's execution."]:
#     """Runs the Auto-GPT agent with a given goal."""
#     # This will be replaced with a call to the Auto-GPT agent via the agent protocol
#     return "Auto-GPT integration pending."

@app.tool
def generate_code(prompt: Annotated[str, "The prompt to generate code from."]) -> Annotated[str, "The generated code."]:
    """Generates code from a prompt."""
    ai = AI()
    memory = BaseMemory()
    preprompts_holder = GptEngineerPromptGenerator()
    files_dict = gen_code(ai, prompt, memory, preprompts_holder)
    return json.dumps(files_dict)

@app.tool
def improve_code(prompt: Annotated[str, "The prompt to improve the code from."], files: Annotated[str, "The files to improve."]) -> Annotated[str, "The improved code."]:
    """Improves code from a prompt."""
    ai = AI()
    memory = BaseMemory()
    preprompts_holder = GptEngineerPromptGenerator()
    files_dict = FilesDict(json.loads(files))
    files_dict = improve_fn(ai, prompt, files_dict, memory, preprompts_holder)
    return json.dumps(files_dict)

if __name__ == "__main__":
    app.run()
