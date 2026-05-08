import os
import re
import asyncio
from pathlib import Path
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import AsyncOpenAI
import chromadb

MAX_CHUNK_SIZE = 2000  # Max characters per chunk
MIN_CHUNK_SIZE = 50    # Skip tiny chunks

BATCH_SIZE = 10  # Process 10 chunks per batch
DELAY_BETWEEN_BATCHES = 1  # 1 second between batches


# SETUP
load_dotenv()
client = AsyncOpenAI(
    api_key=os.getenv("CAMPUSAI_API_KEY"),
    base_url=os.getenv("CAMPUSAI_API_URL")
)

chroma_client = chromadb.PersistentClient(path="./data/vector_db")
collection = chroma_client.get_or_create_collection(name="eu_aviation_regs")

# 2. The Parser (Handle both structures, since one of the HTML files has different structure)
def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, "lxml")
    
    chunks = []

    # Step 1: Check for Highly Structured ELI (divs with art_ IDs)
    articles = soup.find_all("div", id=re.compile(r'^art_\d+'))
    
    if articles:
        print(f" -> Detected ELI Structure for {file_path.name}")
        for art in articles:
            art_id = art.get('id', 'unknown')
            text = art.get_text(separator=" ", strip=True)

            # Filter by size
            if MIN_CHUNK_SIZE <= len(text) <= MAX_CHUNK_SIZE:
                ref = art_id.replace('_', ' ').title()
                chunks.append({"ref": ref, "text": text})
            else:
                print(f" (Skipped {art_id}: {len(text)} chars)")
    

            # # Clean up the reference name (e.g., art_1 -> Article 1)
            # ref = art_id.replace('_', ' ').title()
            # chunks.append({"ref": ref, "text": text})
            
    # Step 2: Handle the <TXT_TE> Blob structure
    else:
        txt_te_area = soup.find("TXT_TE")
        if txt_te_area:
            print(f"   -> Detected Blob Structure for {file_path.name}")
            # Use a separator to ensure "Article 1" stays on its own line for the regex
            full_text = txt_te_area.get_text(separator="\n")
            
            # Use regex split with a "lookahead" to split the text every time it sees "Article [Number]" 
            # keep the word "Article" at the start of the next chunk.
            raw_chunks = re.split(r'\n(?=Article \d+)', full_text)
            
            for i, c in enumerate(raw_chunks):
                clean_c = c.strip()
                if "Article" in clean_c:
                    # Extract the first "Article X" found to use as metadata
                    match = re.search(r'Article \d+', clean_c)
                    ref = match.group(0) if match else f"Section {i}"
                    chunks.append({"ref": ref, "text": clean_c})
        else:
            print(f"Warning: No standard structure found in {file_path.name}")

    return chunks

# 3. PROCESSING & EMBEDDING
async def process_file(file_path):
    print(f"Parsing: {file_path.name}")
    chunks = parse_html(file_path)
    
    if not chunks:
        print(f" -> No chunks extracted from {file_path.name}")
        return

    # Process in batches with delay of 1 second
    for batch_idx in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[batch_idx:batch_idx + BATCH_SIZE]
        
        for i, item in enumerate(batch):
            global_idx = batch_idx + i
            try:
                # Generate Embedding 
                response = await client.embeddings.create(
                    model=os.getenv("CAMPUSAI_EMBED_MODEL"),
                    input=f"search_document: {item['text']}"
                )
                embedding = response.data[0].embedding
                
                # Store in Chroma
                collection.add(
                    ids=[f"{file_path.name}_{global_idx}"],
                    embeddings=[embedding],
                    documents=[item['text']],
                    metadatas=[{
                        "source": file_path.name,
                        "reference": item['ref']
                    }]
                )
            except Exception as e:
                print(f"Error embedding chunk {global_idx}: {e}")
                continue
        
        # Delay between batches to avoid rate limiting
        if batch_idx + BATCH_SIZE < len(chunks):
            await asyncio.sleep(DELAY_BETWEEN_BATCHES)
    
    print(f"Indexed {len(chunks)} sections from {file_path.name}")

async def main():
    os.makedirs("./data/vector_db", exist_ok=True)
    raw_path = Path("./data/raw")
    files = list(raw_path.glob("*.html"))
    
    if not files:
        print("Error: No HTML files found in ./data/raw/")
        return

    for f in files:
        await process_file(f)
    print("\n Ingestion complete")

if __name__ == "__main__":
    asyncio.run(main())