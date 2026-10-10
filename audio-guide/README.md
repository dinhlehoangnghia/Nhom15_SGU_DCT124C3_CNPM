# Multilingual Audio Guide

Microservices backend that turns a point of interest (POI) description into a translated audio narration.

## Architecture
Client -> Gateway -> Content -> Translation -> TTS (audio cached by text+language).

| Service | Role |
|---|---|
| gateway | Single entry point, orchestrates the flow |
| content | POI data |
| translation | Text translation (deep-translator) |
| tts | Text-to-speech (edge-tts) + audio cache |

## Run
```bash
docker compose up --build
```
Open http://localhost:8000/docs, then try `GET /guide/hoi-an?lang=vi`.

## Team
- Member A: gateway, content, CI/CD
- Member B: translation, tts, testing
