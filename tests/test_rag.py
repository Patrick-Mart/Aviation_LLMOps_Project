import os
import json
import pytest
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
from legal_engine import get_aviation_answer

load_dotenv()

def load_cases():
    with open("test_cases.json", "r") as f:
        return json.load(f)

@pytest.fixture(scope="module")
def rag_tools():
    """Initializes the real resources once for the whole test session."""
    client = OpenAI(
        api_key=os.getenv("CAMPUSAI_API_KEY"),
        base_url=os.getenv("CAMPUSAI_API_URL")
    )

    db = chromadb.PersistentClient(path="./data/vector_db")
    collection = db.get_collection(name="eu_aviation_regs")
    return client, collection

@pytest.mark.parametrize("case", load_cases())
def test_aviation_rag(rag_tools, case):
    client, collection = rag_tools
    
    # Run your logic
    response = get_aviation_answer(client, collection, case["question"])
    response_text = response.lower()

    # Verify Article citation exists in the response
    for article in case["expected_articles"]:
        assert article.lower() in response_text, f"Failed Case {case['id']}: Response missed {article}"

    # Verify key legal concepts are mentioned
    matches = [kw for kw in case["expected_keywords"] if kw.lower() in response_text]
    assert len(matches) >= (len(case["expected_keywords"]) / 2), f"Failed Case {case['id']}: Insufficient keywords found."