import hashlib
import os

import edge_tts
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="TTS Service")
AUDIO_DIR = os.getenv("AUDIO_DIR", "/app/audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICES = {
    "en": "en-US-AriaNeural",
    "vi": "vi-VN-HoaiMyNeural",
    "fr": "fr-FR-DeniseNeural",
    "ja": "ja-JP-NanamiNeural",
    "ko": "ko-KR-SunHiNeural",
    "zh-CN": "zh-CN-XiaoxiaoNeural",
}


class TTSRequest(BaseModel):
    text: str
    lang: str = "en"


@app.post("/tts")
async def tts(req: TTSRequest):
    voice = VOICES.get(req.lang)
    if not voice:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {req.lang}")
    # Simple cache: same (lang, text) -> same file
    name = hashlib.sha1(f"{req.lang}:{req.text}".encode()).hexdigest() + ".mp3"
    path = os.path.join(AUDIO_DIR, name)
    cached = os.path.exists(path)
    if not cached:
        await edge_tts.Communicate(req.text, voice).save(path)
    return {"file": name, "cached": cached}


@app.get("/audio/{name}")
def audio(name: str):
    path = os.path.join(AUDIO_DIR, os.path.basename(name))
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Audio not found")
    return FileResponse(path, media_type="audio/mpeg")


@app.get("/health")
def health():
    return {"status": "ok"}
