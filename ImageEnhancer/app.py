from fastapi import FastAPI
from fastapi import Body
from fastapi import UploadFile, File
from io import BytesIO
import numpy as np
import base64
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image
import fastapi as _fapi
import schemas as _schemas
import services as _services
import traceback

app = FastAPI()

# Allow requests from your frontend
origins = [
    "http://localhost:5173",  # dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Photo Enhancer API"}

# Endpoint to test the backend
@app.get("/api")
async def root():
    return {"message": "Welcome to the AI Photo Enhancer with FastAPI"}

@app.post("/api/enhance/")
async def enhance_image(enhanceBase: _schemas._EnhanceBase = Body(...)):
    print("Received enhance request")
    print(f"EnhanceBase: {enhanceBase}")
    # Validate the enhanceBase object
    if not enhanceBase.encoded_base_img:
        return {"message": "No image provided"}
    if not enhanceBase.encoded_base_img[0]:
        return {"message": "Image is empty"}
    try:
        encoded_img = await _services.enhance(enhanceBase=enhanceBase)
    except Exception as e:
        print(traceback.format_exc())
        return {"message": f"{e.args}"}
    
    payload = {
        "mime" : "image/jpg",
        "image": encoded_img
        }
    
    print("Image enhanced successfully")
    print(f"Payload: {payload}")
    # Return the enhanced image as a base64 encoded string      
    return payload
