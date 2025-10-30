#!/usr/bin/env python3
"""
Servidor de test simple para verificar el procesamiento de templates
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/test-photos")
async def test_photos(request: Request):
    """Endpoint de test para verificar procesamiento"""
    print(f"TEST REQUEST:")
    print(f"   URL: {request.url}")
    print(f"   Scheme: {request.url.scheme}")
    print(f"   Netloc: {request.url.netloc}")
    
    # HTML simple para test
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Test Mixed Content</title></head>
    <body>
        <h1>Test de URLs - Mixed Content Debug</h1>
        <div id="info">
            <p><strong>Request URL:</strong> {request.url}</p>
            <p><strong>Base URL:</strong> {request.url.scheme}://{request.url.netloc}</p>
            <p><strong>Expected API URL:</strong> {request.url.scheme}://{request.url.netloc}/images</p>
        </div>
        
        <div id="results"></div>
        
        <script>
            console.log("Request URL:", "{request.url}");
            console.log("Base URL:", "{request.url.scheme}://{request.url.netloc}");
            
            // Test de fetch con URL dinamica
            const apiUrl = "{request.url.scheme}://{request.url.netloc}/images";
            console.log("API URL:", apiUrl);
            
            document.getElementById('results').innerHTML = 
                '<p><strong>JavaScript API URL:</strong> ' + apiUrl + '</p>';
            
            // Test de fetch
            fetch(apiUrl)
                .then(response => {{
                    console.log("Fetch success:", response.status);
                    document.getElementById('results').innerHTML += 
                        '<p style="color: green;">Fetch SUCCESS: ' + response.status + '</p>';
                }})
                .catch(error => {{
                    console.log("Fetch error:", error);
                    document.getElementById('results').innerHTML += 
                        '<p style="color: red;">Fetch ERROR: ' + error + '</p>';
                }});
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.get("/images")
async def test_images():
    """Endpoint de test para simular /images"""
    return {"success": True, "message": "Test images endpoint working"}

if __name__ == "__main__":
    print("Starting test server...")
    print("Visit: http://localhost:8000/test-photos")
    uvicorn.run(app, host="0.0.0.0", port=8000)