from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.responses import FileResponse
import os, time

app = FastAPI(title="EN→ES Translator")

# --- Serve index.html at "/" ---
BASE = os.path.dirname(__file__)
@app.get("/")
def home():
    return FileResponse(os.path.join(BASE, "index.html"))

# --- Translation API ---
translator = pipeline("translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es")

class Item(BaseModel):
    text: str

@app.post("/translate")
def translate(item: Item):
    out = translator(item.text, max_length=400)
    return {"translation": out[0]["translation_text"]}

@app.get("/health")
def health():
    return {"ok": True, "time": time.time()}
