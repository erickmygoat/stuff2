import os
import zipfile
import asyncio
import logging
import shutil
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Request, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from my_son.daemon import AutonomousAgentDaemon
from my_son.action_generation.executor import ActionExecutor
from my_son.config import update_identity, IS_MASTERMIND
from my_son.agent.llm import LLMClient
from my_son.interface.state import state_manager
from my_son.interface.vision import VisionInterface

# --- Configuration ---
SECRET_TOKEN = os.environ.get("MY_SON_SECRET", "1234")
REPO_ROOT = os.getcwd()
SWARM_PORT = int(os.environ.get("MY_SON_SWARM_PORT", "8000"))

app = FastAPI(title="My Son Agent API")
templates = Jinja2Templates(directory="templates")

# Mount static files
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize core components
daemon = AutonomousAgentDaemon()
executor = ActionExecutor()
swarm_llm = LLMClient()
vision = VisionInterface()

# Background task runner
loop_task = None

@app.on_event("startup")
async def startup_event():
    """
    Start the autonomous loop in the background and open global tunnel.
    """
    global loop_task
    loop_task = asyncio.create_task(daemon_wrapper())

    try:
        from pyngrok import ngrok
        public_url = ngrok.connect(SWARM_PORT).public_url
        print(f"Server: Global Access URL: {public_url}")
        await state_manager.log_activity(f"Global Access enabled: {public_url}")
    except ImportError:
        print("Server: pyngrok not installed. Global access disabled.")
    except Exception as e:
        print(f"Server: Failed to start ngrok: {e}")

async def daemon_wrapper():
    print("Server: Starting autonomous daemon loop...")
    await state_manager.update_state("status", "Running")
    try:
        await daemon.run_loop()
    except asyncio.CancelledError:
        print("Server: Daemon loop cancelled.")
        await state_manager.update_state("status", "Stopped")
    except Exception as e:
        print(f"Server: Daemon loop crashed: {e}")
        await state_manager.update_state("status", "Crashed")
        await state_manager.log_activity(f"Daemon crashed: {e}")

# --- Auth ---
def verify_token(request: Request):
    token = request.headers.get("X-Auth-Token") or request.query_params.get("token")
    if token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized: Only my creator can access this.")
    return True

# --- WebSocket ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await state_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        state_manager.disconnect(websocket)

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

@app.get("/mobile", response_class=HTMLResponse)
async def read_mobile(request: Request):
    return templates.TemplateResponse(request=request, name="mobile.html")

@app.get("/manifest.json")
async def manifest(request: Request):
    return templates.TemplateResponse(request=request, name="manifest.json", media_type="application/json")

@app.post("/api/chat")
async def chat(request: ChatRequest, authorized: bool = Depends(verify_token)):
    await state_manager.update_state("current_task", "Processing User Input")
    await state_manager.log_activity(f"User: {request.message}")

    response = await daemon.conversational_engine.handle_user_input(request.message)

    await state_manager.log_activity(f"Agent: {response}")
    await state_manager.update_state("current_task", "Idle")

    return {"response": response}

@app.post("/api/action")
async def run_action(request: ActionRequest, authorized: bool = Depends(verify_token)):
    await state_manager.log_activity(f"Executing action: {request.command}")
    result = executor.execute_shell_command(request.command)
    await state_manager.log_activity(f"Action result: {result}")
    return result

@app.get("/api/download")
async def download_code(authorized: bool = Depends(verify_token)):
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

    await state_manager.log_activity("Codebase downloaded.")
    return FileResponse(zip_filename, media_type="application/zip", filename=zip_filename)

@app.post("/api/upgrade")
async def trigger_upgrade(background_tasks: BackgroundTasks, authorized: bool = Depends(verify_token)):
    await state_manager.log_activity("Manual upgrade triggered.")
    background_tasks.add_task(daemon.run_self_improvement)
    return {"status": "Upgrade cycle initiated."}

# --- Vision Endpoint ---
@app.post("/api/vision/analyze")
async def analyze_image(file: UploadFile = File(...), prompt: str = "Describe this image", authorized: bool = Depends(verify_token)):
    """
    Analyzes an uploaded image using the Vision capabilities.
    """
    await state_manager.log_activity(f"Vision: Analyzing image with prompt '{prompt}'...")
    try:
        # Read image
        image_bytes = await file.read()

        # Process/Encode
        encoded_image = vision.process_image(image_bytes)
        if not encoded_image:
            raise HTTPException(status_code=400, detail="Invalid image data")

        # Send to LLM
        # Use daemon.agent.llm or a new instance? Daemon has one.
        response = daemon.conversational_engine.llm.complete(
            prompt=prompt,
            system_prompt="You are a Vision AI. Describe the image in detail.",
            images=[encoded_image]
        )

        await state_manager.log_activity(f"Vision Result: {response}")
        return {"response": response}
    except Exception as e:
        await state_manager.log_activity(f"Vision failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- New Endpoints (Stage 3 & 4) ---

@app.post("/api/migration/receive")
async def receive_soul(file: UploadFile = File(...)):
    await state_manager.log_activity("Receiving Soul Transfer...")
    try:
        temp_zip = "received_soul.zip"
        with open(temp_zip, "wb") as f:
            shutil.copyfileobj(file.file, f)
        with zipfile.ZipFile(temp_zip, "r") as zip_ref:
            zip_ref.extractall(".")
        os.remove(temp_zip)
        update_identity(is_mastermind=True)
        await state_manager.log_activity("Soul integrated. I am now the Mastermind.")
        return {"status": "Success", "message": "Soul integrated."}
    except Exception as e:
        await state_manager.log_activity(f"Soul reception failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/swarm/generate")
async def swarm_generate(task: SwarmTask):
    await state_manager.log_activity(f"Processing Swarm Task: {task.prompt[:20]}...")
    response = swarm_llm.complete(
        prompt=task.prompt,
        system_prompt=task.system_prompt,
        use_swarm=False
    )
    return {"response": response}
