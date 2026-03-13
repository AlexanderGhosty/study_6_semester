from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head><title>FastAPI Docker App</title></head>
        <body>
            <h1>Welcome to Dockerized FastAPI App!</h1>
        </body>
    </html>
    """