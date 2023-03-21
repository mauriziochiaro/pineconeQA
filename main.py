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

# # source: https://discuss.streamlit.io/t/remove-made-with-streamlit-from-bottom-of-app/1370/2
# hide_streamlit_style = """
#             <style>
#             footer {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.header("Assistenza Progetto INTEGRA")

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

# AUTORIZZATO = auth.autorizzazione_utente()

# if AUTORIZZATO: 
RELOAD = False
if "answers" not in st.session_state:
    st.session_state.answers = []
    RELOAD = True
if "questions" not in st.session_state:
    st.session_state.questions = []
# if "chat_cleared" not in st.session_state:
#     st.session_state.chat_cleared = False    

# DEMO Q&A:
demo_inst_q="Come si installa Progetto INTEGRA?"
demo_inst_a='''Per installare Progetto INTEGRA, è necessario seguire i seguenti passaggi:
1. Se si desidera installare il programma su un singolo PC, selezionare un percorso locale (ad esempio C:\Integra511) durante la selezione della cartella di installazione. Se si desidera installare il programma su più PC condividendo gli archivi su un server, selezionare uno spazio condiviso come lettera di unità visualizzato univocamente da tutti gli utenti (ad esempio "M:\"), specificando il percorso del server durante la selezione della cartella di installazione.

2. Inserire il proprio numero di licenza (n. 5 caratteri numerici) ed i propri dati identificativi.

3. Indicare il percorso librerie (cartella "\lib" contenente tutti gli archivi grafici e i files dwg/xls) e il percorso Apparecchiature e prezzari pubblici (cartella "\libbd" contenente tutte le basi dati ed i prezzari). È consigliabile inserire entrambe le cartelle sul server all'interno di una directory che identifica la versione attuale (ad esempio M:\Integra\lib e M:\Integra\libbd).

4. Premere Avanti per proseguire fino a terminare l'installazione.

5. Dopo l'installazione, è possibile eseguire il programma dal PC pilota. Per eseguire il programma da altre postazioni, è necessario creare un Operatore per ogni utilizzatore tramite la procedura che permette di gestire gli Operatori e realizzare il collegamento a Progetto Integra (collegamento al file integra5_64.exe presente sul Server) su ogni altra postazione.
'''

demo_bd_q="Domanda: Come creo una BD personalizzata?"
demo_bd_a='''Per creare una base dati personalizzata in Progetto INTEGRA, segui i seguenti passaggi:

1. Apri la base dati CaviCustom.bd tramite il menu File Apri Base dati CaviCustom.bd (dal percorso di installazione che, di default, è il seguente: C:\Integra\libbd);
2. Salvala utilizzando il comando Salva come con un altro nome (ad esempio “CaviCustom-il proprio numero di licenza” che è univoco);
3. Quindi, dal menu Modifica Impostazioni di progetto, seleziona il disco di backup di tutti i dati personalizzati che non possono essere disponibili facendo semplicemente una nuova installazione del programma.

In questo modo avrai creato una nuova base dati personalizzata.
'''

demo_ge_q="Domanda: Come inserisco un Gruppo Elettrogeno?"
demo_ge_a='''Per inserire un Gruppo Elettrogeno in un impianto già esistente, è possibile utilizzare la funzione "Collega a nuovo GE" presente nel pulsante Elaborazioni (Ingranaggio) oppure seguire la procedura di seguito riportata:

1. Aggiungere una nuova Fornitura tramite il pulsante "Aggiungi" a destra.
2. Selezionare "Gruppo Elettrogeno" dall'apposito sottomenu di selezione.
3. Inserire i dati descrittivi di identificazione e i dati tecnici determinati dall'impianto a monte del quadro principale, in particolare la corrente di cortocircuito.
4. Confermare i dati inseriti.
5. Il programma realizzerà automaticamente l'impianto impostando la commutazione con le due forniture.

In alternativa, se il progetto è già stato realizzato, è possibile aggiungere una commutazione Rete-Gruppo tramite la procedura sopra descritta, ma occorre prima aggiungere una Fornitura di tipo Gruppo Elettrogeno con al di sotto una quadro generale con una partenza.
'''

# you can create columns to better manage the flow of your page
# this command makes 3 columns of equal width
col1, col2, col3 = st.columns(3)
with col1:
# Add an example button 
    btn_demo1=st.button(label="Come si installa Progetto INTEGRA?",key="demo_inst")
if btn_demo1:
    RELOAD=True
    st.markdown(f'<p style="font-weight: bold; display: inline;"><em>Domanda: {demo_inst_q}</em><br /><br /></p> {demo_inst_a}', unsafe_allow_html=True)
# this will put a button in the middle column
with col2:
    btn_demo2=st.button(label="Come creo una BD personalizzata?",key="demo_bd")
if btn_demo2:
    RELOAD=True
    st.markdown(f'<p style="font-weight: bold; display: inline;"><em>Domanda: {demo_bd_q}</em><br /><br /></p> {demo_bd_a}', unsafe_allow_html=True)   
with col3:
    btn_demo3=st.button(label="Come inserisco un Gruppo Elettrogeno?",key="demo_ge")
if btn_demo3:
    RELOAD=True
    st.markdown(f'<p style="font-weight: bold; display: inline;"><em>Domanda: {demo_ge_q}</em><br /><br /></p> {demo_ge_a}', unsafe_allow_html=True)    

AUTORIZZATO = auth.autorizzazione_utente(RELOAD)

if AUTORIZZATO:         
    placeholder = st.empty()
    def get_text():
        input_text = placeholder.text_input("Domanda: ", value="", key="input")
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

    # if user_input != "" and not st.session_state.chat_cleared:
    if user_input != "" :
        
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
# # Reset the chat_cleared variable after displaying the answers
# st.session_state.chat_cleared = False  
