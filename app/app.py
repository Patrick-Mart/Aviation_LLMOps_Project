import streamlit as st
import os
import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from legal_engine import get_aviation_answer # Updated import

load_dotenv()
st.set_page_config(page_title="EU Aviation Law Assistant", page_icon="⚖️")
st.title("EU Aviation Law Assistant")

@st.cache_resource
def init_resources():
    client = OpenAI(
        api_key=os.getenv("CAMPUSAI_API_KEY"), 
        base_url=os.getenv("CAMPUSAI_API_URL")
    )
    chroma_client = chromadb.PersistentClient(path="./data/vector_db")
    collection = chroma_client.get_collection(name="eu_aviation_regs")
    return client, collection

client, collection = init_resources()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Ask about EU aviation law..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Searching regulations..."):
            try:
                # Direct call to our new safety function
                answer = get_aviation_answer(client, collection, user_query)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"System Error: {e}")