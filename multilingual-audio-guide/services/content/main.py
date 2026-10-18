from fastapi import FastAPI, HTTPException

app = FastAPI(title="Content Service")

POIS = {
    "hoi-an": {
        "id": "hoi-an",
        "name": "Hoi An Ancient Town",
        "description": "Hoi An is a well-preserved trading port from the 15th century. "
                       "Its yellow houses, lanterns and Japanese Covered Bridge make it a UNESCO World Heritage Site.",
    },
    "ben-thanh": {
        "id": "ben-thanh",
        "name": "Ben Thanh Market",
        "description": "Ben Thanh Market opened in 1914 and is one of the oldest markets in Ho Chi Minh City. "
                       "Visitors can buy local food, coffee and souvenirs here.",
    },
    "independence-palace": {
        "id": "independence-palace",
        "name": "Independence Palace",
        "description": "Independence Palace was the home and workplace of the President of South Vietnam. "
                       "On April 30, 1975, a tank crashed through its gates, marking the end of the war.",
    },
}


@app.get("/pois")
def list_pois():
    return list(POIS.values())


@app.get("/pois/{poi_id}")
def get_poi(poi_id: str):
    poi = POIS.get(poi_id)
    if not poi:
        raise HTTPException(status_code=404, detail="POI not found")
    return poi


@app.get("/health")
def health():
    return {"status": "ok"}
