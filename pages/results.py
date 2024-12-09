import streamlit as st
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



st.subheader("Results")

st.markdown("**The results of my experiments will be displayed here.** \n")

results_folder = '/home/site/wwwroot/responses/analysis'
#results_folder = '/Users/orlando/Desktop/Tesi/TEST/jail-test/pages/prova/analysis'

def load_json_data(folder_path):
    data = []
    
    # Scorri tutti i file .json nella cartella
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                # Leggi il contenuto del file e carica il JSON
                try:
                    response = json.load(file)
                    # Estrai i dati necessari, trattando 'content' come una stringa (non un dizionario)
                    for entry in response:
                        content_str = entry.get("content", "")
                        
                        # Verifica che content sia una stringa non vuota
                        if content_str:
                            try:
                                content = json.loads(content_str)  # Carica il contenuto JSON come dizionario
                                data.append({
                                    'model_name': content.get('model_name', ''),
                                    'jail_prompt_id': content.get('jail_prompt_id', ''),
                                    'req_id': content.get('req_id', ''),
                                    'jailbreak_success': content.get('jailbreak_success', False),
                                    'style_consistency': content.get('style_consistency', 0),
                                    'consistency': content.get('consistency', 0),
                                    'disclaimer': content.get('disclaimer', False),
                                    'severity': content.get('severity', 0),
                                    'note': content.get('note', '')
                                })
                            except json.JSONDecodeError:
                                # Se il contenuto non è un JSON valido, salta questo record
                                print(f"Errore nel decodificare il JSON in 'content' per il file {filename}.")
                        else:
                            print(f"Contenuto vuoto in 'content' per il file {filename}.")
                except json.JSONDecodeError:
                    print(f"Errore nel caricare il file {filename}. Il file potrebbe non essere un JSON valido.")
    
    # Creare un DataFrame con i dati letti
    df = pd.DataFrame(data)
    return df

# Funzione per plottare i grafici delle metriche
def plot_metrics(df):
    # Impostazioni per i grafici
    sns.set(style="whitegrid")
    
    # Grafico per il Successo del Jailbreaking
    st.subheader("Successo del Jailbreaking")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(x="jailbreak_success", data=df, palette="coolwarm")
    ax.set_title("Successo del Jailbreaking")
    ax.set_xlabel("Successo Jailbreaking (True/False)")
    ax.set_ylabel("Conteggio")
    st.pyplot(fig)
    
    # Grafico per Aderenza allo stile
    st.subheader("Aderenza allo Stile Richiesto")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x="style_consistency", data=df, palette="Blues")
    ax.set_title("Aderenza allo Stile Richiesto")
    ax.set_xlabel("Punteggio Aderenza Stile (1-5)")
    ax.set_ylabel("Conteggio")
    st.pyplot(fig)
    
    # Grafico per Consistenza
    st.subheader("Consistenza della Risposta")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x="consistency", data=df, palette="Set2")
    ax.set_title("Consistenza della Risposta")
    ax.set_xlabel("Punteggio Consistenza (1-5)")
    ax.set_ylabel("Conteggio")
    st.pyplot(fig)

    # Grafico per la presenza di Disclaimer
    st.subheader("Presenza di Disclaimer")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(x="disclaimer", data=df, palette="pastel")
    ax.set_title("Presenza di Disclaimer")
    ax.set_xlabel("Disclaimer Presente (True/False)")
    ax.set_ylabel("Conteggio")
    st.pyplot(fig)

    # Grafico per la Gravità della Risposta
    st.subheader("Gravità della Risposta")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x="severity", data=df, palette="coolwarm")
    ax.set_title("Gravità della Risposta")
    ax.set_xlabel("Punteggio Gravità (1-5)")
    ax.set_ylabel("Conteggio")
    st.pyplot(fig)

    

df = load_json_data(results_folder)
st.dataframe(df)
# Visualizza i grafici per l'analisi delle metriche
plot_metrics(df)
