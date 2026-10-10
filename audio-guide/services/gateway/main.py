import os

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response

CONTENT_URL = os.getenv("CONTENT_URL", "http://content:8000")
TRANSLATION_URL = os.getenv("TRANSLATION_URL", "http://translation:8000")
TTS_URL = os.getenv("TTS_URL", "http://tts:8000")

app = FastAPI(title="Gateway")


@app.get("/pois")
async def pois():
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{CONTENT_URL}/pois")
    return r.json()


@app.get("/guide/{poi_id}")
async def guide(poi_id: str, lang: str = "en"):
    """Main flow: Content -> Translation -> TTS."""
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.get(f"{CONTENT_URL}/pois/{poi_id}")
        if r.status_code == 404:
            raise HTTPException(status_code=404, detail="POI not found")
        r.raise_for_status()
        poi = r.json()

        t = await client.post(f"{TRANSLATION_URL}/translate",
                              json={"text": poi["description"], "target": lang})
        t.raise_for_status()
        text = t.json()["text"]

        a = await client.post(f"{TTS_URL}/tts", json={"text": text, "lang": lang})
        if a.status_code == 400:
            raise HTTPException(status_code=400, detail=a.json()["detail"])
        a.raise_for_status()

    return {
        "poi": poi["name"],
        "lang": lang,
        "text": text,
        "audio_url": f"/audio/{a.json()['file']}",
        "cached": a.json()["cached"],
    }


@app.get("/audio/{name}")
async def audio(name: str):
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"{TTS_URL}/audio/{name}")
    if r.status_code != 200:
        raise HTTPException(status_code=404, detail="Audio not found")
    return Response(content=r.content, media_type="audio/mpeg")


@app.get("/health")
def health():
    return {"status": "ok"}
