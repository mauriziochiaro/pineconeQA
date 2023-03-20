import os
import streamlit as st
import openai
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import autorizzazione as auth
# import memories

st.set_page_config(page_title="LexE", page_icon=":robot:")

# hide_streamlit_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             </style>
#             """

# source: https://discuss.streamlit.io/t/remove-made-with-streamlit-from-bottom-of-app/1370/2
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.header("Chat Assistenza Progetto INTEGRA")

# OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
# PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
# PINECONE_API_ENV = os.environ["PINECONE_API_ENV"]

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
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

AUTORIZZATO = auth.autorizzazione_utente()

if AUTORIZZATO: 

    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "questions" not in st.session_state:
        st.session_state.questions = []
    # if "chat_cleared" not in st.session_state:
    #     st.session_state.chat_cleared = False    
        
    placeholder = st.empty()
    def get_text():
        input_text = placeholder.text_input("You: ", value="", key="input")
        return input_text

    user_input = get_text()

    # # Function to clear the conversation
    # def clear_conversation():
    #     st.session_state["answers"] = []
    #     st.session_state["questions"] = []
    #     st.session_state["chat_cleared"] = True

    # # Add a button to clear the conversation
    # if st.button("Nuova chat"):
    #     clear_conversation()

    if user_input != "" and not st.session_state.chat_cleared:
        
        # REFERENCE SOURCE:
        # OpenAI's New GPT 3.5 Embedding Model for Semantic Search => https://youtu.be/ocxq84ocYi0
        # OpenAI GPT 3.5 AI assistant with Langchain + Pinecone #1 => https://youtu.be/15TDwVSpwKc
        index = pinecone.Index(index_name=index_name)
        def integra_bot(query: str): 
            try:       
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
                        {"role": "system", "content": "Sono LexE, una assistente AI e so rispondere solo a domande tecniche sull'utilizzo del software Progetto INTEGRA. Mi vengono fornite delle parti estratte da un lungo documento (Contesto) e una domanda. Mi accerto di essere stata utile, e in caso contrario informo gentilmente di contattare l'assistenza tecnica di Exel. Se la domanda non riguarda Progetto INTEGRA, informo gentilmente che sono istruita solo per rispondere a domande su Progetto INTEGRA."},
                        {"role": "user", "content": f"Contesto: {context}\n\nDomanda: {user_input}\n\nRispondimi con formattazione Markdown."},
                    ],
                    temperature=0,
                )
                print(response["choices"][0]["message"]["content"])
                ChatGPT_res=(response["choices"][0]["message"]["content"])
                return(ChatGPT_res)
            
            except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    return "Sorry, an error occurred while processing your request. Please try again."
            
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

  
