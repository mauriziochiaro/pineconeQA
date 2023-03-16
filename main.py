import os
import streamlit as st
import openai
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
# import memories

st.set_page_config(page_title="LexE", page_icon=":robot:")
st.header("Chat Assistenza Progetto INTEGRA")

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
# PINECONE_API_ENV = st.secret["PINECONE_API_ENV"]
PINECONE_API_ENV = "us-east-1-aws"

embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)
index_name = "indexpinecone1"

docsearch = Pinecone.from_existing_index(embedding=embedding, index_name=index_name)

llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, max_tokens=1000)
qa_chain = load_qa_chain(llm, chain_type="stuff")

st.success("Buongiorno! Sono l'assistente AI per il software Progetto INTEGRA. Sono istruito per rispondere a domande tecniche sull'utilizzo del software. Come posso aiutarla?")   

if "answers" not in st.session_state:
    st.session_state.answers = []
if "questions" not in st.session_state:
    st.session_state.questions = []
if "chat_cleared" not in st.session_state:
    st.session_state.chat_cleared = False    
    
placeholder = st.empty()
def get_text():
    input_text = placeholder.text_input("You: ", value="", key="input")
    return input_text

user_input = get_text()

# Function to clear the conversation
CLEARED_CONVO=False
def clear_conversation():
    st.session_state["answers"] = []
    st.session_state["questions"] = []
    st.session_state["chat_cleared"] = True

# Add a button to clear the conversation
if st.button("Nuova chat"):
    clear_conversation()
    # user_input = ""
    # placeholder.text_input("You: ", value="")

if user_input != "" and not st.session_state.chat_cleared:

#||||||||||||||||||||||||||||||||||||||| METODO 1

    # docs = docsearch.similarity_search(user_input, include_metadata=True)
    # template = f"""Sei Lino, un assistente AI e sai rispondere a domande tecniche sull'uso del software Progetto INTEGRA.
    # Ti vengono fornite le seguenti parti estratte da un lungo documento e una domanda. Fornisci una risposta colloquiale.
    # Se non conosci la risposta, dì semplicemente "Hmm, non ne sono sicuro, la invito a contattare l'assistenza tecnica". Non cercare di inventare una risposta.
    # Se la domanda non riguarda Progetto INTEGRA, informali gentilmente che sei istruito solo per rispondere a domande su Progetto INTEGRA.
    # Domanda: {user_input}
    # Fornisci la risposta e interessati se il cliente ha bisogno di ulteriori informazioni:"""
    # answer = qa_chain.run(input_documents=docs[:2], question=template)
    # print(answer)

#||||||||||||||||||||||||||||||||||||||| METODO 2
    
    # REFERENCE SOURCE:
    # OpenAI's New GPT 3.5 Embedding Model for Semantic Search => https://youtu.be/ocxq84ocYi0
    # OpenAI GPT 3.5 AI assistant with Langchain + Pinecone #1 => https://youtu.be/15TDwVSpwKc
    index = pinecone.Index(index_name=index_name)
    def integra_bot(query: str):        
        model='text-embedding-ada-002'
        res=openai.Embedding.create(
            input=query,
            engine=model
        )
        # print(res['data'][0]['embedding'])
        xq=(res['data'][0]['embedding'])
        xc=index.query(xq,top_k=5,include_metadata=True)
        context=""
        for match in xc['matches']:
            context+=f"\n{(match['metadata']['text'])}"

        MODEL = "gpt-3.5-turbo"
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Sei LexE, un assistente AI e sai rispondere solo a domande tecniche sull'utilizzo del software Progetto INTEGRA. Se la domanda non riguarda Progetto INTEGRA, informa gentilmente che sei istruito solo per rispondere a domande su Progetto INTEGRA."},
                {"role": "user", "content": "Come si crea un BD personalizzata?"},
                {"role": "assistant", "content": "Per creare una base dati personalizzata, è necessario aprire la base dati CaviCustom.bd tramite il menu File Apri Base dati CaviCustom.bd (dal percorso di installazione che, di default, è il seguente: C: \Integra\libbd).\n\nQuindi, è necessario salvare la base dati utilizzando il comando Salva come con un altro nome (ad esempio “Custom-il proprio numero di licenza” che è univoco).\n\nSe ha bisogno di ulteriori informazioni, sono a Sua completa disposizione.\nSe non sono riuscito a darle le informazioni che cercava, la invito a contattare l'assistenza tecnica di exel."},
                {"role": "user", "content": f"{user_input}"},
            ],
            temperature=0,
        )
        print(response["choices"][0]["message"]["content"])
        ChatGPT_res=(response["choices"][0]["message"]["content"])
        return(ChatGPT_res)

    answer=integra_bot(user_input)
    st.session_state.questions.append(user_input)
    st.session_state.answers.append(answer)

    if st.session_state.answers:
        for i in range(len(st.session_state.answers) - 1, -1, -1):
            st.markdown(f'<p style="font-weight: bold; display: inline;"><em>Domanda: {st.session_state.questions[i]}</em><br /><br /></p> {st.session_state.answers[i]}', unsafe_allow_html=True)
            if i != 0:
                st.markdown("---")
# Reset the chat_cleared variable after displaying the answers
st.session_state.chat_cleared = False            

  
