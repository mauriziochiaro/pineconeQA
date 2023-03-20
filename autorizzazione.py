import streamlit as st
from datetime import date
import http.client

MAX_EXECUTIONS_PER_CLIENT = 10

@st.cache_resource
def get_executions():
    return {}

def autorizzazione_utente(RELOAD: bool):
    # Function to get the client's IP address
    def get_client_ip():
        conn = http.client.HTTPConnection("ifconfig.me")
        conn.request("GET", "/ip")
        response = conn.getresponse()
        return response.read().decode("utf-8")

    executions = get_executions()

    # Get the current date
    current_date = date.today()

    # Get the client's IP address
    client_ip = get_client_ip()

    if client_ip not in executions:
        executions[client_ip] = {"executions": 0, "last_execution_date": current_date}

    # Check if the current date is different from the last execution date and reset the counter if needed
    if executions[client_ip]["last_execution_date"] != current_date:
        executions[client_ip]["executions"] = 0
        executions[client_ip]["last_execution_date"] = current_date

    print(executions[client_ip])
    # Check if the client has reached the maximum number of script executions
    if executions[client_ip]["executions"] < MAX_EXECUTIONS_PER_CLIENT:
        if not RELOAD:
            executions[client_ip]["executions"] += 1

        st.success("Buongiorno! Sono LexE, l'assistente AI per il software Progetto INTEGRA. Sono istruita per rispondere a domande tecniche sull'utilizzo del software. Come posso aiutarla?")  

        st.info("Numero di richieste giornaliere effettuate: {} su {}".format(executions[client_ip]["executions"], MAX_EXECUTIONS_PER_CLIENT))

        return True

    else:
        st.warning("Raggiunto numero massimo di richieste giornaliere disponibili: ({}).".format(MAX_EXECUTIONS_PER_CLIENT))

        return False
