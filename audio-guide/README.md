# Multilingual Audio Guide

A microservices backend that turns a point-of-interest (POI) description into a translated audio narration. Built for the Software Engineering course.

## How it works

```
Client -> Gateway -> Content -> Translation -> TTS -> audio (mp3)
```

| Service | Role | Tech |
|---|---|---|
| gateway | Single entry point, orchestrates the flow | FastAPI, httpx |
| content | POI data | FastAPI |
| translation | Text translation with cache and fallback provider | deep-translator |
| tts | Text-to-speech with audio cache | edge-tts |

Services communicate over REST inside a Docker network.

## Quick start

Requirements: Docker Desktop, internet connection.

```bash
git clone https://github.com/dinhlehoangnghia/multilingual-audio-guide.git
cd multilingual-audio-guide
docker compose up --build
```

Open http://localhost:8000/docs and try:

```
GET /guide/hoi-an?lang=vi
```

Available POIs: `hoi-an`, `ben-thanh`, `independence-palace`
Languages: `en`, `vi`, `fr`, `ja`, `ko`, `zh-CN`

## CI/CD

GitHub Actions runs lint and Docker build on every push and pull request.

## Team (Group 15)

| Member | GitHub | Responsibilities |
|---|---|---|
| Dinh Le Hoang Nghia | @dinhlehoangnghia | gateway, content, Docker Compose |
| <Name B> | @<username> | translation, tts |
| <Name C> | @<username> | CI/CD, tests, documentation |

## Workflow

Feature branches + pull requests with peer review. No direct pushes to `main`.

## Project status (Week 7)

- [x] Service skeleton and Docker Compose
- [x] GitHub Actions CI
- [ ] Translation cache and fallback provider
- [ ] Automated tests
- [ ] Architecture diagram and API docs

## Roadmap

- Message queue (RabbitMQ) for asynchronous processing
- Simple web UI for the demo
- More languages and voices
