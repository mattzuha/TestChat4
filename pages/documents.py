import os
import utils
import streamlit as st
from streaming import StreamHandler

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_text_splitters import RecursiveCharacterTextSplitter

st.set_page_config(page_title="ChatPDF", page_icon="📄")
st.header('Chat With Your Documents :books:')
st.write('Upload your pdfs file and get answer from your pdfs')
st.write('[![view source code ](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/mattzuha/TestChat4/blob/main/pages/documents.py)')

# Global variable to store the LLM and embedding model configuration
llm = None
embedding_model = None


def initialize():
    global llm, embedding_model
    utils.sync_st_session()
    llm = utils.configure_llm()
    embedding_model = utils.configure_embedding_model()


def save_file(file):
    folder = 'tmp'
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = f'./{folder}/{file.name}'
    with open(file_path, 'wb') as f:
        f.write(file.getvalue())
    return file_path


@st.spinner('Analyzing documents..')
def setup_qa_chain(uploaded_files):
    # Load documents
    docs = []
    for file in uploaded_files:
        file_path = save_file(file)
        loader = PyPDFLoader(file_path)
        docs.extend(loader.load())

    # Split documents and store in vector db
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(docs)
    vectordb = DocArrayInMemorySearch.from_documents(splits, embedding_model)

    # Define retriever
    retriever = vectordb.as_retriever(
        search_type='mmr',
        search_kwargs={'k': 2, 'fetch_k': 4}
    )

    # Setup memory for contextual conversation
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        output_key='answer',
        return_messages=True
    )

    # Setup LLM and QA chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        verbose=False
    )
    return qa_chain


@utils.enable_chat_history
def main():
    # Initialize LLM and embedding model
    initialize()

    # User Inputs
    uploaded_files = st.sidebar.file_uploader(label='Upload PDF files', type=['pdf'], accept_multiple_files=True)
    if not uploaded_files:
        st.error("Please upload PDF documents to continue!")
        st.stop()

    user_query = st.chat_input(placeholder="Ask me anything!")

    if uploaded_files and user_query:
        qa_chain = setup_qa_chain(uploaded_files)

        utils.display_msg(user_query, 'user')

        with st.chat_message("assistant"):
            st_cb = StreamHandler(st.empty())
            result = qa_chain.invoke(
                {"question": user_query},
                {"callbacks": [st_cb]}
            )
            response = result["answer"]
            st.session_state.messages.append({"role": "assistant", "content": response})
            utils.print_qa(main, user_query, response)

            # to show references
            for idx, doc in enumerate(result['source_documents'], 1):
                filename = os.path.basename(doc.metadata['source'])
                page_num = doc.metadata['page']
                ref_title = f":blue[Reference {idx}: *{filename} - page.{page_num}*]"
                with st.popover(ref_title):
                    st.caption(doc.page_content)


if __name__ == "__main__":
    main()
