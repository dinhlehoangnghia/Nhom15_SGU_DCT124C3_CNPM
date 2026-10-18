import hashlib
import json
import os

from deep_translator import GoogleTranslator, MyMemoryTranslator
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Translation Service")

MYMEMORY = {"vi": "vi-VN", "en": "en-US", "fr": "fr-FR", "ja": "ja-JP", "ko": "ko-KR", "zh-CN": "zh-CN"}
CACHE_FILE = os.getenv("CACHE_FILE", "/app/cache/translations.json")
os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

try:
    with open(CACHE_FILE, encoding="utf-8") as f:
        CACHE = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    CACHE = {}


def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(CACHE, f, ensure_ascii=False)


class TranslateRequest(BaseModel):
    text: str
    target: str


@app.post("/translate")
def translate(req: TranslateRequest):
    if req.target == "en":
        return {"text": req.text, "target": "en", "provider": "none"}

    key = hashlib.sha1(f"{req.target}:{req.text}".encode()).hexdigest()
    if key in CACHE:
        return {"text": CACHE[key], "target": req.target, "provider": "cache"}

    errors = []
    try:
        text = GoogleTranslator(source="en", target=req.target).translate(req.text)
        provider = "google"
    except Exception as exc:
        errors.append(f"google: {exc}")
        print("Google failed:", exc, flush=True)
        try:
            text = MyMemoryTranslator(
                source="en-US", target=MYMEMORY.get(req.target, req.target)
            ).translate(req.text)
            provider = "mymemory"
        except Exception as exc2:
            errors.append(f"mymemory: {exc2}")
            print("MyMemory failed:", exc2, flush=True)
            raise HTTPException(status_code=502, detail=" | ".join(errors))

    CACHE[key] = text
    save_cache()
    return {"text": text, "target": req.target, "provider": provider}


@app.get("/health")
def health():
    return {"status": "ok"}