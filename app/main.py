from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.api.routes import router
from app.models import ChatRequest
from app.services import ai_service  # Assuming ai_service is defined in app.services

app = FastAPI(
    title="AI Voice Assistant API",
    description="API for AI voice assistant with speech-to-text, text-to-speech, and chat capabilities",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the index.html template"""
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Process text-based chat requests
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    result = await ai_service.generate_response(request.message)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)