import os
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st
from streamlit_chat import message

st.set_page_config(page_title="Integra Q&A", page_icon=":robot:")
st.header("Integra Q&A")

from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
PINECONE_API_ENV = st.secret["PINECONE_API_ENV"]

embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)
index_name = "indexpinecone1"

docsearch = Pinecone.from_existing_index(embedding=embedding, index_name=index_name)

from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, max_tokens=1000)
chain = load_qa_chain(llm, chain_type="stuff")

st.success("Puoi chiedermi informazioni riguardo la documentazione di Progetto INTEGRA")   

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

placeholder = st.empty()
def get_text():
    input_text = placeholder.text_input("You: ", value="", key="input")
    return input_text

user_input = get_text()

if user_input:
    query = user_input
    print(query)

    docs = docsearch.similarity_search(query, include_metadata=True)

    answer = chain.run(input_documents=docs, question=query)

    st.session_state.past.append(user_input)
    print(st.session_state.past)
    st.session_state.generated.append(answer)
    print(st.session_state.past)

if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")    
