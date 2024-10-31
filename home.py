import streamlit as st

st.set_page_config(
    page_title="Ultimate Chatbot",
    page_icon=':hibiscus:',
    layout='wide'
)

st.header("Chatbot Implementations with Langchain")
st.write("""
[![view source code ](https://img.shields.io/badge/GitHub%20Repository-gray?logo=github)](https://github.com/mattzuha/TestChat4)
""")
st.write("""Please use llama3.1:8b due to financial issues
""")
st.write("""
- **Basic Chatbot**: Normal.
- **Chat with your documents**: Read custom documents, provide answers based on the referenced information.
""")