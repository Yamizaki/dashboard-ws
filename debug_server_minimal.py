#!/usr/bin/env python3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# CORS muy permisivo para debug
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/debug")
async def debug_page():
    """Servir página de debug"""
    with open("debug_mixed_content.html", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/images")
async def images_endpoint():
    """Endpoint de imágenes para testing"""
    return {
        "success": True,
        "message": "Debug images endpoint working",
        "data": [],
        "pagination": {"total": 0, "limit": 50, "offset": 0}
    }

@app.get("/")
async def root():
    return {"message": "Debug server running", "endpoints": ["/debug", "/images"]}

if __name__ == "__main__":
    print("🚀 Starting debug server...")
    print("📍 Visit: http://localhost:8000/debug")
    uvicorn.run(app, host="0.0.0.0", port=8000)
