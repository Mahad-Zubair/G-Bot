from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import markdown2

# App setup
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
genai.configure(api_key="AIzaSyDBpwDcLPGqEZkyPvzkds_6A4YBPe5-myk")  # Replace with your actual key
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

# Templates and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Session memory store
chat_memory = {}

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def serve_front(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_endpoint(request: Request, chat_data: ChatRequest):
    user_ip = request.client.host
    user_input = chat_data.message.strip()

    if not user_input:
        return JSONResponse({"error": "No message provided."}, status_code=400)

    # Initialize memory if not present
    if user_ip not in chat_memory:
        chat_memory[user_ip] = []

    # Append user message to memory
    chat_memory[user_ip].append(f"User: {user_input}")

    # Keep only last 10 messages
    history = chat_memory[user_ip][-10:]
    context = "\n".join(history)

    # Always act as travel assistant
    prompt = (
        "You are a helpful Travel Assistant. Respond in Markdown (use bold, bullet points, etc.).\n\n"
        f"{context}\nAssistant:"
    )

    try:
        response = model.generate_content(prompt)
        # Append bot response to memory
        chat_memory[user_ip].append(f"Assistant: {response.text}")
        # Convert markdown to HTML and wrap in a class for styling
        formatted_response = f'<div class="markdown-content">{markdown2.markdown(response.text)}</div>'
    except Exception as e:
        print("Gemini Error:", e)
        formatted_response = "⚠️ Sorry, something went wrong while generating a response."

    return {"response": formatted_response}