import os
import chromadb
from dotenv import load_dotenv
from openai import OpenAI

# 1. SETUP
load_dotenv()
client = OpenAI(
    api_key=os.getenv("CAMPUSAI_API_KEY"),
    base_url=os.getenv("CAMPUSAI_API_URL")
)

# Connect to Chroma
chroma_client = chromadb.PersistentClient(path="./data/vector_db")
collection = chroma_client.get_collection(name="eu_aviation_regs")

# 2. DEFINE THE QUERY
user_query = user_query = "Compare the requirements for an operating licence in 1008/2008 with the obligations for assisting disabled passengers in 1107/2006."

# 3. GENERATE QUERY EMBEDDING (Crucial step!)
# We must use the same model and a matching prefix ('search_query:')
query_response = client.embeddings.create(
    model=os.getenv("CAMPUSAI_EMBED_MODEL"),
    input=f"search_query: {user_query}"
)
query_embedding = query_response.data[0].embedding

# 4. RETRIEVE FROM CHROMA
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

retrieved_context = "\n---\n".join(results['documents'][0])
metadata = results['metadatas'][0]

# 5. GENERATE ANSWER
prompt = f"""
You are an expert in European Aviation Law. Use the provided Context (extracted from EU Regulations 1008/2008 and 1107/2006) to answer the question.

Instructions:
- Cite the specific Article number if available in the metadata or text.
- If the context does not contain information on one of the regulations, clearly state that.
- Maintain a formal, legalistic tone.

Context:
{retrieved_context}

Question: {user_query}
"""

response = client.chat.completions.create(
    model=os.getenv("CAMPUSAI_MODEL"),
    messages=[{"role": "user", "content": prompt}],
    temperature=0.0 # Extreme precision for legal testing
)

# 6. PRINT RESULTS
print("\n" + "="*30)
print("SOURCES RETRIEVED FROM CHROMADB")
print("="*30)
for i, m in enumerate(metadata):
    print(f"[{i+1}] File: {m['source']} | Reference: {m['reference']}")

print("\n" + "="*30)
print("CAMPUS AI RESPONSE")
print("="*30)
print(response.choices[0].message.content)