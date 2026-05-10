# EU Aviation Law Assistant (RAG)

## Description
A Retrieval-Augmented Generation (RAG) app that answers complex legal queries regarding EU Regulations 1008/2008,  1107/2006 and 261/2004.

## System Architecture
1. **Data Layer**: PDF regulations chunked and stored in ChromaDB (Vector Store).
2. **Retrieval Layer**: Semantic search using `text-embedding-ada-002`.
3. **Generation Layer**: OpenAI GPT-4 (via CampusAI) synthesizing legal answers.

## How to Run
1. Add your `.env` file with `CAMPUSAI_API_KEY`.
2. Build Docker: `docker build -t aviation-rag .`
3. Run Docker: `docker run -p 8501:8501 aviation-rag`

## Generate Embeddings (ChromaDB)

```python
uv run ingest.py
```

This creates the database with the vector embeddings for the HTML files inside `data/vector_db`.

## API Documentation
- `POST /ask`: Accepts JSON `{"text": "query"}` and returns legal analysis.
- `GET /health`: Returns service status.

## Evaluation
- **Qualitative**: The system correctly identifies Article 4 requirements for licensing and distinguishes between the two primary regulations.
- **Quantitative**: Retrieval hit rate is approximately 90% for direct Article mentions.





