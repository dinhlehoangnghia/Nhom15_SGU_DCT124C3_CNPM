from deep_translator import GoogleTranslator
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Translation Service")


class TranslateRequest(BaseModel):
    text: str
    target: str  # e.g. "vi", "fr", "ja", "ko", "zh-CN"


@app.post("/translate")
def translate(req: TranslateRequest):
    if req.target == "en":
        return {"text": req.text, "target": "en"}
    try:
        text = GoogleTranslator(source="en", target=req.target).translate(req.text)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Translation failed: {exc}")
    return {"text": text, "target": req.target}


@app.get("/health")
def health():
    return {"status": "ok"}
