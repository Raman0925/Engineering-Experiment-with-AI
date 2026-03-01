from fastapi import FastAPI,Request
from pydantic import BaseModel
from openai import OpenAI
from groq import Groq
from google import genai
import logging
from api.core.config import config

import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def run_llm(provider, model_name, messages, max_tokens=500):
    if provider == "OpenAi":
        key = config.OpenAI_API_KEY
        if not key:
            return "Set OPENAI_API_KEY in app secrets (Streamlit Cloud) or in .env locally."
        client = OpenAI(api_key=key)
    elif provider == "Groq":
        key = config.GROQ_API_KEY
        if not key:
            return "Set GROQ_API_KEY in app secrets (Streamlit Cloud) or in .env locally."
        client = groq.Groq(api_key=key)
    else:
        key = config.GOOGLE_API_KEY
        if not key:
            return "Set GOOGLE_API_KEY in app secrets (Streamlit Cloud) or in .env locally."
        client = genai.Client(api_key=key)
    if provider == "Google":
        return client.models.generate_content(model=model_name, contents=[message["content"] for message in messages]).text
    elif provider == "Groq":
        return client.chat.completions.create(model=model_name, messages=messages, max_tokens=max_tokens).choices[0].message.content
    else:
        return client.chat.completions.create(model=model_name, messages=messages, max_tokens=max_tokens).choices[0].message.content


class ChatRequest(BaseModel):
    provider: str
    model_name: str
    messages: list[dict]

class Chatresponse(BaseModel):
    message: str

app = FastAPI()

@app.post("/chat")
def chat(request: Request, response: Chatresponse)->Chatresponse:
    try:
        result = run_llm(request.provider, request.model_name, request.messages)
        return Chatresponse(message=result)
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

