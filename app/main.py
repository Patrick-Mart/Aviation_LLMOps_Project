from fastapi import FastAPI
from pydantic import BaseModel
from legal_engine import get_aviation_answer, init_resources

app = FastAPI()
client, collection = init_resources()

class Query(BaseModel):
    text: str

@app.post("/ask")
async def ask_lawyer(query: Query):
    # This calls your working RAG logic
    answer = get_aviation_answer(client, collection, query.text)
    return {"query": query.text, "answer": answer}

@app.get("/health")
async def health():
    return {"status": "online"}
