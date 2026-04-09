from algorithms import astar_search, depth_limited_search, greedy_best_first_search, uniform_cost_search
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
from map import Map
import pytesseract
import numpy as np
import json
import cv2
import io
import re

ALGORITHMS = {
    "ucs": uniform_cost_search,
    "dls": depth_limited_search,
    "greedy": greedy_best_first_search,
    "astar": astar_search
}

app = FastAPI()

# Allowed origins
origins = [
    "http://localhost:5173", # Vue frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/graph")
def default_graph():
    with open("data/map.json") as f:
        return json.load(f)

class SearchRequest(BaseModel):
    map_json: dict
    start: str
    goal: str
    algorithm: str
    depth: int = 10
    heuristic: dict = {}

class SearchResponse(BaseModel):
    status: str
    cost: float | None
    path: list    


@app.post("/api/search")
def search(req: SearchRequest):
    m = Map.from_json(req.map_json)

    algorithm = ALGORITHMS.get(req.algorithm)

    if not algorithm:
        raise HTTPException(400, "Unknown algorithm")

    result = algorithm(
        m,
        req.start,
        req.goal,
        heuristic=req.heuristic,
        depth=req.depth
    )

    return SearchResponse(status=result[0], cost=result[1], path=result[2])


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(image: np.ndarray):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold (helps OCR a lot)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh

def clean_text(text: str):
    # Keep only alphanumeric (typical for plates)
    text = re.sub(r'[^A-Z0-9]', '', text.upper())
    return text

@app.post("/api/ocr/license-plate")
async def read_license_plate(file: UploadFile = File(...)):
    try:
        print(file.filename)
        # Read file into memory
        contents = await file.read()

        # Convert to PIL Image
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        # Convert to OpenCV format
        image_np = np.array(image)
        image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Preprocess
        processed = preprocess_image(image_cv)

        # OCR
        custom_config = r'--oem 3 --psm 7'  # good for single line text
        text = pytesseract.image_to_string(processed, config=custom_config)

        # Clean result
        plate = clean_text(text)

        if not plate:
            raise HTTPException(status_code=400, detail="No plate detected")

        return {
            "plate": plate
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
