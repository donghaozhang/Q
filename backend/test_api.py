from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="Q Project Test API")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Q Project backend is running!"}

@app.get("/")
async def root():
    return {"message": "Welcome to Q Project API", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001) 