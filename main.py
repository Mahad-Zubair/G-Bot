#FastAPI-Backend

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates #used to create HTML, XML, or other markup formats returned to user via HTTP response
import google.generativeai as genai
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware 
import os

app = FastAPI()

#Configure CORS (for frontend Communication)
#a security mechanism that allows a web page to access resources from a different domain.

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

#Configure Gemini API
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-pro")

#Mount static Files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"),name="static")

#loading templates (HTML)
templates = Jinja2Templates(directory="templates")

#Data Model for User Inpit
class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class = HTMLResponse)
async def serve_front(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request:ChatRequest):
    user_input = request.message
    if not user_input:
        return JSONResponse({"error":"No Message Provided"}, status_code=400)
    
    response = model.generate_content(user_input)
    try:
        formatted_response = response.text.replace("\n", "<br>")
    except ValueError as e:
        formatted_response = "I'm sorry, but I can't provide a response due to content restrictions."
    
    return {"response": formatted_response}
