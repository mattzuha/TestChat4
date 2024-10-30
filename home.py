import streamlit as st

st.set_page_config(
    page_title="Firefly's Chatbot",
    page_icon=':hibiscus:',
    layout='wide'
)

st.header("Chatbot Implementations with Langchain")
st.write("""

- **Basic Chatbot**: Normal.
- **Chat with your documents**: Read custom documents, provide answers based on the referenced information.
""")