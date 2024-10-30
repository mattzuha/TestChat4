import utils
import streamlit as st
from streaming import StreamHandler
from langchain.chains import ConversationChain

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.header('Basic Chatbot :newspaper:')
st.write('A whatever chatbot')

# Global variable to store the LLM configuration
llm = None


def initialize():
    global llm
    utils.sync_st_session()
    llm = utils.configure_llm()


def setup_chain():
    return ConversationChain(llm=llm, verbose=False)


@utils.enable_chat_history
def main():
    # Initialize LLM
    initialize()

    # Set up conversation chain
    chain = setup_chain()
    user_query = st.chat_input(placeholder="Ask me anything!")

    if user_query:
        utils.display_msg(user_query, 'user')
        with st.chat_message("assistant"):
            st_cb = StreamHandler(st.empty())
            result = chain.invoke(
                {"input": user_query},
                {"callbacks": [st_cb]}
            )
            response = result["response"]
            st.session_state.messages.append({"role": "assistant", "content": response})
            utils.print_qa(main, user_query, response)


if __name__ == "__main__":
    main()
