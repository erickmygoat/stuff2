import os
import zipfile
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from my_son.daemon import AutonomousAgentDaemon
from my_son.action_generation.executor import ActionExecutor

# --- Configuration ---
# In a real app, use environment variables for secrets
SECRET_TOKEN = os.environ.get("MY_SON_SECRET", "1234")  # Simple MVP auth
REPO_ROOT = os.getcwd()

app = FastAPI(title="My Son Agent API")
templates = Jinja2Templates(directory="templates")

# Initialize core components
daemon = AutonomousAgentDaemon()
executor = ActionExecutor()

# Background task runner for the autonomous loop
loop_task = None

@app.on_event("startup")
async def startup_event():
    """
    Start the autonomous loop in the background.
    """
    global loop_task
    # We run the daemon loop as a background task.
    # Since daemon.run_loop is an infinite loop, we wrap it.
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
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
async def chat(request: ChatRequest, authorized: bool = Depends(verify_token)):
    """
    Communicates with the agent.
    """
    # Inject input into the agent's flow
    # Since the daemon reads from input.txt, we can write to it,
    # OR we can expose a direct method in ConversationalEngine.
    # For MVP consistency with previous architecture, let's write to input.txt
    # and wait for output.txt (or modify engine to return directly).

    # Better approach for "App": Direct call
    response = await daemon.conversational_engine.handle_user_input(request.message)
    # Note: handle_user_input in previous code wrote to file and didn't return.
    # I should probably update ConversationalEngine to return the response too.
    # For now, I'll read the output file or just return a confirmation.

    # Let's assume handle_user_input returns None but writes to output.txt.
    # I will modify ConversationalEngine in a moment to return the string.

    # Fallback if engine doesn't return
    if not response:
        if os.path.exists("output.txt"):
            with open("output.txt", "r") as f:
                response = f.read()
        else:
            response = "Agent received your message."

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
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(REPO_ROOT):
            # Exclude git, pycache, venv, and the zip itself
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
