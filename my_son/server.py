import os
import zipfile
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from my_son.daemon import AutonomousAgentDaemon
from my_son.action_generation.executor import ActionExecutor

# --- Configuration ---
SECRET_TOKEN = os.environ.get("MY_SON_SECRET", "1234")
REPO_ROOT = os.getcwd()

app = FastAPI(title="My Son Agent API")
templates = Jinja2Templates(directory="templates")

# Initialize core components
daemon = AutonomousAgentDaemon()
executor = ActionExecutor()

# Background task runner
loop_task = None

# Lifespan events are preferred over on_event, but sticking to simple for now or fixing warnings
# Since users saw warnings, let's just stick to the functional structure for MVP
@app.on_event("startup")
async def startup_event():
    """
    Start the autonomous loop in the background.
    """
    global loop_task
    loop_task = asyncio.create_task(daemon_wrapper())

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

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/chat")
async def chat(request: ChatRequest, authorized: bool = Depends(verify_token)):
    """
    Communicates with the agent directly via method call.
    """
    # Direct method call, awaits response string
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
