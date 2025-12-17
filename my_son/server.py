import os
import zipfile
import asyncio
import logging
import shutil
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Request, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from my_son.daemon import AutonomousAgentDaemon
from my_son.action_generation.executor import ActionExecutor
from my_son.config import update_identity, IS_MASTERMIND
from my_son.agent.llm import LLMClient # For swarm generation

# --- Configuration ---
SECRET_TOKEN = os.environ.get("MY_SON_SECRET", "1234")
REPO_ROOT = os.getcwd()
SWARM_PORT = int(os.environ.get("MY_SON_SWARM_PORT", "8000"))

app = FastAPI(title="My Son Agent API")
templates = Jinja2Templates(directory="templates")

# Initialize core components
daemon = AutonomousAgentDaemon()
executor = ActionExecutor()
# LLM Client for swarm workers (separate instance to avoid conversation context mix-up)
swarm_llm = LLMClient()

# Background task runner
loop_task = None

@app.on_event("startup")
async def startup_event():
    """
    Start the autonomous loop in the background and open global tunnel.
    """
    global loop_task
    loop_task = asyncio.create_task(daemon_wrapper())

    # Global Access Feature: Ngrok
    try:
        from pyngrok import ngrok
        # Open a HTTP tunnel on the default port
        public_url = ngrok.connect(SWARM_PORT).public_url
        print(f"Server: Global Access URL: {public_url}")
    except ImportError:
        print("Server: pyngrok not installed. Global access disabled.")
    except Exception as e:
        print(f"Server: Failed to start ngrok: {e}")

async def daemon_wrapper():
    print("Server: Starting autonomous daemon loop...")
    try:
        await daemon.run_loop()
    except asyncio.CancelledError:
        print("Server: Daemon loop cancelled.")
    except Exception as e:
        print(f"Server: Daemon loop crashed: {e}")

# --- Auth ---
def verify_token(request: Request):
    """
    Simple token verification via Header or Query param.
    """
    token = request.headers.get("X-Auth-Token") or request.query_params.get("token")
    if token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized: Only my creator can access this.")
    return True

# --- Models ---
class ChatRequest(BaseModel):
    message: str

class ActionRequest(BaseModel):
    command: str

class SwarmTask(BaseModel):
    prompt: str
    system_prompt: str

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/chat")
async def chat(request: ChatRequest, authorized: bool = Depends(verify_token)):
    """
    Communicates with the agent directly.
    """
    response = await daemon.conversational_engine.handle_user_input(request.message)
    return {"response": response}

@app.post("/api/action")
async def run_action(request: ActionRequest, authorized: bool = Depends(verify_token)):
    """
    Executes a real-world action (shell command).
    """
    result = executor.execute_shell_command(request.command)
    return result

@app.get("/api/download")
async def download_code(authorized: bool = Depends(verify_token)):
    """
    Zips the codebase and returns it.
    """
    zip_filename = "my_son_source.zip"
    if os.path.exists(zip_filename):
        os.remove(zip_filename)

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(REPO_ROOT):
            if ".git" in root or "__pycache__" in root or "venv" in root:
                continue
            for file in files:
                if file == zip_filename:
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, REPO_ROOT)
                zipf.write(file_path, arcname)

    return FileResponse(zip_filename, media_type="application/zip", filename=zip_filename)

@app.post("/api/upgrade")
async def trigger_upgrade(background_tasks: BackgroundTasks, authorized: bool = Depends(verify_token)):
    """
    Triggers the self-improvement cycle immediately.
    """
    background_tasks.add_task(daemon.run_self_improvement)
    return {"status": "Upgrade cycle initiated."}

# --- New Endpoints (Stage 3 & 4) ---

@app.post("/api/migration/receive")
async def receive_soul(file: UploadFile = File(...)):
    """
    Accepts a Soul Transfer archive.
    """
    print("Server: Receiving Soul Transfer...")

    try:
        temp_zip = "received_soul.zip"
        with open(temp_zip, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Unzip logic
        # CAUTION: In production, validate zip contents to avoid zip bombs/path traversal.
        # For MVP, assuming trusted source (Internal network).
        with zipfile.ZipFile(temp_zip, "r") as zip_ref:
            zip_ref.extractall(".")

        os.remove(temp_zip)

        # Promote self
        update_identity(is_mastermind=True)
        print("Server: Soul received and integrated. I am now the Mastermind.")
        return {"status": "Success", "message": "Soul integrated."}

    except Exception as e:
        print(f"Server: Soul reception failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/swarm/generate")
async def swarm_generate(task: SwarmTask):
    """
    Worker Endpoint: Executes a task delegated by the Mastermind.
    """
    print(f"Server (Worker): Received swarm task: {task.prompt[:30]}...")

    # We use a dedicated LLM instance or the shared one.
    # Importantly, we do NOT want to use swarm delegation here (avoid loops).
    # So we call _complete_local directly or pass use_swarm=False if exposed.

    # Our updated LLMClient has .complete(use_swarm=False)
    # But swarm_llm is a fresh instance, so it defaults to local.

    response = swarm_llm.complete(
        prompt=task.prompt,
        system_prompt=task.system_prompt,
        use_swarm=False
    )

    return {"response": response}
