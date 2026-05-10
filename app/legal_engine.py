import os
from openai import OpenAI

def get_aviation_answer(openai_client, chroma_collection, user_query):

    query_response = openai_client.embeddings.create(
                    model=os.getenv("CAMPUSAI_EMBED_MODEL"),
                    input=f"search_query: {user_query}"
                )
    query_embedding = query_response.data[0].embedding

    # Search Chroma
    results = chroma_collection.query(
        query_embeddings=[query_embedding], 
        n_results=5
    )

    # Prepare Context
    context_text = "\n\n---\n\n".join(results['documents'][0])
    
    if not context_text.strip():
        return "I'm sorry, I couldn't find any specific regulations in the database matching that query."

    # OpenAI Call 
    messages = [
        {"role": "system", "content": (
            "You are an expert in EU Aviation Law (Regs 1008/2008 & 1107/2006). "
            "Use the provided context to answer the user's question. "
            "Always cite specific Article numbers from the text. "
            "If the answer isn't in the context, say you don't know."
        )},
        {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {user_query}"}
    ]

    response = openai_client.chat.completions.create(
        model=os.getenv("CAMPUSAI_MODEL"),
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content