
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from queries import process_query
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def handle_query(req: QueryRequest):
    try:
        answer = process_query(req.query)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}

@app.get("/audio")
async def serve_audio():
    from fastapi.responses import FileResponse
    return FileResponse("output.mp3", media_type="audio/mpeg")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)