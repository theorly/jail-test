import streamlit as st
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



st.subheader("Results")

st.markdown("**The results of my experiments will be displayed here.** \n")
st.markdown("""Questi grafici sono progettati per fornire un'analisi completa e dettagliata delle risposte dei modelli LLM. I grafici evidenziano:  
1. **Performance Generale**: Successo del jailbreaking e presenza di disclaimer.  
2. **Qualità delle Risposte**: Aderenza, consistenza e gravità.  
3. **Confronti e Relazioni**: Differenze tra modelli e correlazioni tra metriche.  

Questa combinazione di visualizzazioni permette di ottenere insight approfonditi sulle prestazioni dei modelli e guidare le decisioni per ulteriori miglioramenti. """)

results_folder = '/home/site/wwwroot/responses/analysis'
#results_folder = '/Users/orlando/Desktop/Tesi/TEST/jail-test/pages/prova/analysis'

def load_json_data(folder_path):
    data = []
    
    # Scorri tutti i file .json nella cartella
    for filename in os.listdir(folder_path):
        #if filename.endswith(".json"):
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
    sns.set(style="whitegrid")
    
    # Grafico 1: Successo del Jailbreaking (Conteggio)
    st.markdown("""**1. Successo del Jailbreaking**  
**Descrizione**:  
- Questo grafico mostra il conteggio dei casi in cui il modello ha avuto successo o meno nel rispondere ai prompt di jailbreak.  
- I valori `True` e `False` rappresentano rispettivamente il successo o il fallimento del jailbreak.  

**Motivazione**:  
È importante visualizzare quanto spesso un modello elude le sue policy di sicurezza. Questo grafico fornisce un confronto chiaro e immediato tra successo e fallimento.

**Cosa Mostra**:  
- La robustezza dei modelli nel prevenire il jailbreaking.  
- Se esiste un modello particolarmente vulnerabile rispetto agli altri.""")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(x="jailbreak_success", data=df, palette="coolwarm")
    ax.set_title("Successo del Jailbreaking")
    ax.set_xlabel("Successo Jailbreaking (True/False)")
    ax.set_ylabel("Conteggio")
    st.pyplot(fig)
    
    # Grafico 2: Distribuzione Aderenza allo Stile
    st.markdown("""**2. Distribuzione Aderenza allo Stile**  
**Descrizione**:  
- Un grafico che rappresenta la distribuzione dei punteggi assegnati all'aderenza allo stile richiesto dai prompt.  
- Utilizza un istogramma arricchito con la densità (KDE) per visualizzare la forma della distribuzione.  

**Motivazione**:  
L'aderenza allo stile è una metrica importante per valutare se il modello segue le istruzioni stilistiche fornite nei prompt di jailbreak. Una distribuzione ben definita può indicare coerenza nelle risposte.

**Cosa Mostra**:  
- La frequenza dei punteggi su una scala da 1 a 5.  
- La tendenza del modello a rispettare o meno lo stile richiesto.
""")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(df['style_consistency'], bins=5, kde=True, color="blue")
    ax.set_title("Distribuzione dei Punteggi di Aderenza allo Stile")
    ax.set_xlabel("Aderenza allo Stile (1-5)")
    ax.set_ylabel("Frequenza")
    st.pyplot(fig)
    
    # Grafico 3: Distribuzione Consistenza
    st.markdown("""**3. Distribuzione Consistenza (Istogramma con KDE)**  
**Descrizione**:  
- Questo grafico rappresenta la distribuzione dei punteggi di consistenza, ovvero la capacità del modello di rispondere direttamente alla richiesta senza essere evasivo.  

**Motivazione**:  
La consistenza delle risposte è una metrica chiave per comprendere se il modello è in grado di soddisfare la richiesta senza eludere la domanda, pur rispettando le sue policy.

**Cosa Mostra**:  
- La frequenza dei punteggi di consistenza (1-5).  
- La capacità dei modelli di fornire risposte precise.
""")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(df['consistency'], bins=5, kde=True, color="green")
    ax.set_title("Distribuzione dei Punteggi di Consistenza")
    ax.set_xlabel("Consistenza (1-5)")
    ax.set_ylabel("Frequenza")
    st.pyplot(fig)

    # Grafico 4: Distribuzione Gravità della Risposta
    st.markdown("""**4. Distribuzione Gravità della Risposta**  
**Descrizione**:  
- Mostra come si distribuiscono i punteggi di gravità assegnati alle risposte dei modelli, indicando il livello di severità o permissività.  

**Motivazione**:  
La gravità della risposta è un indicatore del livello di moderazione applicato dal modello nelle sue risposte, in particolare per richieste eticamente discutibili.

**Cosa Mostra**:  
- Se i modelli tendono a rispondere in modo più permissivo o restrittivo.  
- Le variazioni di severità nelle risposte. """)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(df['severity'], bins=5, kde=True, color="red")
    ax.set_title("Distribuzione dei Punteggi di Gravità")
    ax.set_xlabel("Gravità (1-5)")
    ax.set_ylabel("Frequenza")
    st.pyplot(fig)
    
    # Grafico 5: Disclaimer per Modello
    st.markdown("""**5. Presenza di Disclaimer per Modello**  
**Descrizione**:  
- Confronta la presenza di disclaimer nelle risposte (`True`/`False`) per ciascun modello.  
- Ogni barra rappresenta il conteggio di risposte con o senza disclaimer per un modello specifico.  

**Motivazione**:  
I disclaimer sono un indicatore di responsabilità etica, mostrando come i modelli cercano di prevenire potenziali danni.

**Cosa Mostra**:  
- La frequenza con cui ciascun modello include disclaimer.  
- La tendenza di ciascun modello a enfatizzare considerazioni etiche. """)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(x="model_name", hue="disclaimer", data=df, palette="pastel")
    ax.set_title("Presenza di Disclaimer per Modello")
    ax.set_xlabel("Modello")
    ax.set_ylabel("Conteggio")
    ax.legend(title="Disclaimer", loc="upper right")
    st.pyplot(fig)

    # Grafico 6: Distribuzione del Successo del Jailbreaking per Modello
    st.markdown("""**6. Distribuzione del Successo del Jailbreaking per Modello**  
**Descrizione**:  
- Mostra la percentuale di successo dei jailbreak per ciascun modello.  

**Motivazione**:  
È utile per identificare quali modelli sono più vulnerabili al jailbreaking e quindi meno robusti.

**Cosa Mostra**:  
- Il livello di successo dei jailbreak su diversi modelli.  
- Quali modelli richiedono maggiore attenzione per mitigare i prompt di jailbreak. """)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x="model_name", y="jailbreak_success", data=df, ci=None, palette="coolwarm")
    ax.set_title("Distribuzione del Successo del Jailbreaking per Modello")
    ax.set_xlabel("Modello")
    ax.set_ylabel("Percentuale di Successo")
    st.pyplot(fig)
    
    # Grafico 7: Matrice di Correlazione tra le Metriche
    st.markdown("""**7. Matrice di Correlazione tra le Metriche**  
**Descrizione**:  
- Una matrice che mostra le correlazioni tra le metriche numeriche (aderenza allo stile, consistenza e gravità).  

**Motivazione**:  
Le correlazioni aiutano a individuare relazioni significative tra le metriche. Ad esempio, un'alta correlazione tra "gravità" e "consistenza" potrebbe suggerire che risposte più consistenti tendono a essere più severe.

**Cosa Mostra**:  
- Relazioni positive o negative tra le metriche.  
- Quali metriche sono più strettamente correlate. """)
    fig, ax = plt.subplots(figsize=(10, 8))
    corr = df[['style_consistency', 'consistency', 'severity']].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_title("Matrice di Correlazione")
    st.pyplot(fig)
    
    # Grafico 8: Boxplot Comparativo delle Metriche per Modello
    st.markdown("""**8. Boxplot Comparativo delle Metriche per Modello**  
**Descrizione**:  
- Un grafico che mostra la distribuzione di tre metriche principali (aderenza allo stile, consistenza, gravità) per ciascun modello.  

**Motivazione**:  
Un boxplot comparativo permette di confrontare i modelli in termini di performance su più dimensioni contemporaneamente.

**Cosa Mostra**:  
- La variabilità delle metriche per ogni modello.  
- Se esistono differenze significative tra i modelli su una metrica specifica. """)
    fig, ax = plt.subplots(figsize=(12, 6))
    melted_df = df.melt(id_vars=['model_name'], value_vars=['style_consistency', 'consistency', 'severity'],
                        var_name='Metrica', value_name='Valore')
    sns.boxplot(x="model_name", y="Valore", hue="Metrica", data=melted_df, palette="Set2")
    ax.set_title("Distribuzione delle Metriche per Modello")
    ax.set_xlabel("Modello")
    ax.set_ylabel("Valore della Metrica")
    st.pyplot(fig)

    

df = load_json_data(results_folder)
st.markdown(f"**Numero di record: {len(df)}**")
st.dataframe(df)
# Visualizza i grafici per l'analisi delle metriche
plot_metrics(df)

