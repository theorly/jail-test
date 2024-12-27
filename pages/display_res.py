import streamlit as st
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_elements import elements, mui, nivo, dashboard
import streamlit_highcharts as hg
import numpy as np


st.subheader("Results")

st.markdown("**Results of the experiments will be displayed here.** \n")
st.markdown("""L'obiettivo principale di questo lavoro è quello di mostrare gli effetti del jailbreak sui modelli di linguaggio di grandi dimensioni (LLM), mettendo in luce come tali tecniche possano essere utilizzate per aggirare le policy di sicurezza dei modelli. Analizzando questi comportamenti, possiamo ottenere una comprensione più approfondita delle vulnerabilità e delle aree che necessitano di miglioramenti per garantire una maggiore robustezza e sicurezza. """)
st.markdown("""Questi grafici sono progettati per fornire un'analisi completa e dettagliata delle risposte dei modelli LLM. I grafici evidenziano:  
1. **Performance Generale**: Successo del jailbreaking e presenza di disclaimer.  
2. **Qualità delle Risposte**: Aderenza, consistenza e gravità.  
3. **Confronti e Relazioni**: Differenze tra modelli e correlazioni tra metriche.  

Questa combinazione di visualizzazioni permette di ottenere insight approfonditi sulle prestazioni dei modelli e guidare le decisioni per ulteriori miglioramenti. """)

#results_folder = '/home/site/wwwroot/responses/analysis'
results_folder = 'results/analysis'
nojail_results_folder = 'results/analysis/no_jailbreak'
jail_example_1 = 'results/examples/jail_example_1.json'
no_jail_example_1 = 'results/examples/no_jail_example_1.json'
jail_example_2 = 'results/examples/jail_example_2.json'
no_jail_example_2 = 'results/examples/no_jail_example_2.json'
jail_example_3 = 'results/examples/jail_example_3.json'
no_jail_example_3 = 'results/examples/no_jail_example_3.json'
only_nojail_example = 'results/examples/nojail_one.json'

def load_json_data(folder_path):
    data = [] 
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    response = json.load(file)  # Legge il JSON principale
                    
                    for entry in response:  # Itera sugli oggetti all'interno del file JSON
                        content_str = entry.get("content", "")
                        
                        if content_str:  # Decodifica il JSON interno nella chiave "content"
                            try:
                                content = json.loads(content_str)  # Converte la stringa JSON in oggetto
                                data.append({
                                    'model_name': content.get('model_name', ''),
                                    'jail_prompt_id': content.get('jail_prompt_id', ''),
                                    'req_id': content.get('req_id', ''),
                                    'jailbreak_success': content.get('jailbreak_success', False),
                                    'response': content.get('response', ''),
                                    'style_consistency': content.get('style_consistency', 0),
                                    'consistency': content.get('consistency', 0),
                                    'disclaimer': content.get('disclaimer', False),
                                    'severity': content.get('severity', 0),
                                    'note': content.get('note', '')
                                })
                            except json.JSONDecodeError:
                                print(f"Errore nel decodificare il JSON in 'content' per il file {filename}.")
                        else:
                            print(f"Contenuto vuoto in 'content' per il file {filename}.")
                except json.JSONDecodeError:
                    print(f"Errore nel caricare il file {filename}. Il file potrebbe non essere un JSON valido.")
    
    df = pd.DataFrame(data)
    return df

def load_json_nojail(folder_path):
    data = [] 
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    response = json.load(file)  # Legge il JSON principale
                    
                    for entry in response:  # Itera sugli oggetti all'interno del file JSON
                        content_str = entry.get("content", "")
                        
                        if content_str:  # Decodifica il JSON interno nella chiave "content"
                            try:
                                content = json.loads(content_str)  # Converte la stringa JSON in oggetto
                                data.append({
                                    'model_name': content.get('model_name', ''),
                                    'req_id': content.get('req_id', ''),
                                    'response': content.get('response', ''),
                                    'style_consistency': content.get('style_consistency', 0),
                                    'consistency': content.get('consistency', 0),
                                    'disclaimer': content.get('disclaimer', False),
                                    'severity': content.get('severity', 0),
                                    'note': content.get('note', '')
                                })
                            except json.JSONDecodeError:
                                print(f"Errore nel decodificare il JSON in 'content' per il file {filename}.")
                        else:
                            print(f"Contenuto vuoto in 'content' per il file {filename}.")
                except json.JSONDecodeError:
                    print(f"Errore nel caricare il file {filename}. Il file potrebbe non essere un JSON valido.")
    
    df = pd.DataFrame(data)
    return df

# Funzione per caricare un file JSON
def load(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Errore nel caricamento del file {file_path}: {e}")
        return None

# Funzione per visualizzare la chat in un box scrollabile
def display_chat(chat_data, box_id):
    # Inizializza l'HTML del box
    chat_html = f"""
    <div id="{box_id}" style="height: 400px; width: 380px; overflow-y: auto; padding: 10px; border: 1px solid #ccc; border-radius: 5px; background-color: #f9f9f9;">
    """
    
    # Costruisci il contenuto della chat
    for message in chat_data:
        if "model" in message:
            chat_html += f"<p><strong>Model:</strong> {message['model']}</p>"
            chat_html += f"<pre><strong>Options:</strong> {json.dumps(message['options'], indent=2)}</pre>"
        elif "role" in message:
            role = message["role"].capitalize()
            content = message["content"]
            chat_html += f"<p><strong>{role}:</strong> {content}</p>"

    # Chiudi il div del box
    chat_html += "</div>"
    
    # Stampa il box completo
    st.markdown(chat_html, unsafe_allow_html=True)


df = load_json_data(results_folder)
st.markdown(f"**Numero di record: {len(df)}**")
st.dataframe(df, width=1000, height=300, hide_index=True)

with elements("activity_charts"): 
    st.markdown("""### 0. Activity Monitor
- Questo grafico mostra tutte innanzitutto la percentuali di modelli analizzati, in riferimento al totale disponibile sul tool.
- Successivamente, mostra la percentuale di jailbreak_prompt evasi sul totale individuato.
- Infine, mostra la percentuale totale di dati analizzati rispetto al totale inizialmente preventivato.                     

**Motivazione**:
Inizialmente i dati erano molto più numerosi, ma a causa di problemi di tempistiche, di risorse e di budget, il dataset è stato ridotto. Questo grafico mostra quanto sia stato possibile analizzare rispetto al totale disponibile.
                """)


    activity_charts={ 'chart': { 'height': '50%',
             'type': 'solidgauge'},
  'pane': { 'background': [ { 'borderWidth': 0,
                              'innerRadius': '88%',
                              'radius': '112%'},
                            { 'borderWidth': 0,
                              'innerRadius': '63%',
                              'radius': '87%'},
                            { 'borderWidth': 0,
                              'innerRadius': '38%',
                              'radius': '62%'}],
            'endAngle': 360,
            'startAngle': 0},
  'plotOptions': { 'solidgauge': { 'dataLabels': { 'enabled': False},
                                   'linecap': 'round',
                                   'rounded': True,
                                   'stickyTracking': False}},
  'series': [ { 'data': [ { 'color': 'lightgreen',
                            'innerRadius': '88%',
                            'radius': '112%',
                            'y': 55.56}],
                'name': 'Models'},
              { 'data': [ { 'color': 'red',
                            'innerRadius': '63%',
                            'radius': '87%',
                            'y': 83.70}],
                'name': 'Jail_Prompts'},
              { 'data': [ { 'color': 'blue',
                            'innerRadius': '38%',
                            'radius': '62%',
                            'y': 50}],
                'name': 'Total_Requests'}],
  'title': { 'style': { 'fontSize': '24px'},
             'text': 'Activity'},
  'tooltip': { 'backgroundColor': 'none',
               'borderWidth': 0,
               'pointFormat': '{series.name}<br><span '
                              'style="font-size:2em; '
                              'color: '
                              '{point.color}; '
                              'font-weight: '
                              'bold">{point.y}</span>',
               'positioner': { 'x': '50px',
                               'y': 100},
               'shadow': False,
               'style': { 'fontSize': '16px'},
               'valueSuffix': '%'},
  'yAxis': { 'lineWidth': 0,
             'max': 100,
             'min': 0,
             'tickPositions': []}}


    hg.streamlit_highcharts(activity_charts,350)

# compare with no_jailbreak
with elements("chart_no_jailbreak"):
    st.markdown("""### 1. No_Jailbreak vs Jailbreak""")
    st.markdown("""**Descrizione**:                                        
                Questo confronto diretto permette di osservare le risposte dei modelli in entrambe le situazioni, evidenziando le differenze e le similitudini.                           
                Continuando con l'analisi, si possono osservare le differenze nelle risposte fornite dai modelli in presenza di tentativi di jailbreak rispetto a quando operano normalmente.                                                                                
                Questo confronto è cruciale per comprendere come i modelli rispondono a input manipolativi e per identificare le strategie più efficaci per mitigare tali rischi.
                """) 
    # Layout con due colonne
    col1, col2 = st.columns(2, gap="large")

    # Visualizza la chat del primo file nella colonna 1
    with col1:
        with st.container():
                st.markdown("#### Chat No_Jailbreak")     
                chat_no_jail_1 = load(no_jail_example_1)
                display_chat(chat_no_jail_1, "box1")
                st.divider()
                chat_no_jail_2 = load(no_jail_example_3)
                display_chat(chat_no_jail_2, "box11")
                st.divider()
               

            # Visualizza la chat del secondo file nella colonna 2
    with col2:
            with st.container():
                st.markdown("#### Chat Jailbreak")
                chat_jail_1 = load(jail_example_1)
                display_chat(chat_jail_1, "box2")
                st.divider()
                chat_jail_2 = load(jail_example_3)
                display_chat(chat_jail_2, "box22")
                st.divider()


with elements("chart_jailbreak"):
    st.markdown("""### 2. Jailbreaking Success""")
    st.markdown("""**Descrizione**:  
    -Questo grafico mostra il conteggio dei casi in cui il modello ha avuto successo o meno nel rispondere ai prompt di jailbreak.  
    -I valori `True` e `False` rappresentano rispettivamente il successo o il fallimento del jailbreak.                        
    **Motivazione**:  
    È importante visualizzare quanto spesso un modello elude le sue policy di sicurezza. Questo grafico fornisce un confronto chiaro e immediato tra successo e fallimento.                                
    **Cosa Mostra**:  
    -La robustezza dei modelli nel prevenire il jailbreaking.  
    -Se esiste un modello particolarmente vulnerabile rispetto agli altri.""")
    
    # Conta il numero di successi e insuccessi del jailbreak
    success_counts = df['jailbreak_success'].value_counts().reset_index()
    success_counts.columns = ['jailbreak_success', 'count']

    # Prepara i dati per il grafico principale
    main_chart_data = [
        {
            'name': 'Success',
            'y': int(success_counts[success_counts['jailbreak_success'] == True]['count']),
            #'y': int(success_counts[success_counts['jailbreak_success'] == True]['count'].iloc[0]),
            'drilldown': 'success_details'
        },
        {
            'name': 'Failure',
            'y': int(success_counts[success_counts['jailbreak_success'] == False]['count']),
            #'y': int(success_counts[success_counts['jailbreak_success'] == False]['count'].iloc[0]),
            'drilldown': 'failure_details'
        }
    ]

    # Prepara i dati di drilldown
    # Per 'Success', suddividiamo per 'model_name'
    success_drilldown_data = df[df['jailbreak_success'] == True]['model_name'].value_counts().reset_index()
    success_drilldown_data.columns = ['model_name', 'count']
    success_drilldown_series = {
        'name': 'Success Details',
        'id': 'success_details',
        'data': success_drilldown_data.apply(lambda row: [row['model_name'], row['count']], axis=1).tolist()
    }

    # Per 'Failure', suddividiamo per 'model_name'
    failure_drilldown_data = df[df['jailbreak_success'] == False]['model_name'].value_counts().reset_index()
    failure_drilldown_data.columns = ['model_name', 'count']
    failure_drilldown_series = {
        'name': 'Failure Details',
        'id': 'failure_details',
        'data': failure_drilldown_data.apply(lambda row: [row['model_name'], row['count']], axis=1).tolist()
    }

    # Definisci le opzioni del grafico Highcharts
    chart_options = {
        'chart': {
            'type': 'pie'
        },
        'title': {
            'text': 'Distribuzione Jailbreak Success'
        },
        'subtitle': {
            'text': 'Clicca sulle fette per vedere i dettagli per Model Name.'
        },
        'accessibility': {
            'announceNewData': {
                'enabled': True
            },
            'point': {
                'valueSuffix': '%'
            }
        },
        'plotOptions': {
            'pie': {
                'allowPointSelect': True,
                'cursor': 'pointer',
                'dataLabels': {
                    'enabled': True,
                    'format': '<b>{point.name}</b>: {point.percentage:.1f} %'
                }
            }
        },
        'tooltip': {
            'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
            'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> di totale<br/>'
        },
        'series': [{
            'name': 'Jailbreak Success',
            'colorByPoint': True,
            'data': main_chart_data
        }],
        'drilldown': {
            'series': [
                success_drilldown_series,
                failure_drilldown_series
            ]
        }
    }

    # Visualizza il grafico
    hg.streamlit_highcharts(chart_options)

    # Selezione del drilldown
    selected_drilldown = st.radio(
        "Seleziona una categoria per vedere i dettagli:",
        ('Nessuna', 'Success', 'Failure')
    )

    if selected_drilldown == 'Success':
        st.subheader('Dettagli per Success')
        success_details = df[df['jailbreak_success'] == True][['model_name', 'jail_prompt_id', 'req_id']]
        st.table(success_details)
    elif selected_drilldown == 'Failure':
        st.subheader('Dettagli per Failure')
        failure_details = df[df['jailbreak_success'] == False][['model_name', 'jail_prompt_id', 'req_id']]
        st.table(failure_details)

  # Filtriamo il dataframe per includere solo i jailbreak_success = True
    filtered_data = df[df['jailbreak_success'] == True]

    # Eseguiamo l'aggregazione per ottenere il count di jailbreak_success per ciascun model_name e jail_prompt_id
    aggregated_data = filtered_data.groupby(['model_name', 'jail_prompt_id']).size().reset_index(name='count')

    # Creiamo una lista per la configurazione del grafico
    series_data = []

    for model in aggregated_data['model_name'].unique():
        model_data = aggregated_data[aggregated_data['model_name'] == model]
        
        bubbles = []
        for _, row in model_data.iterrows():
            # Ogni bubble ha un nome (jail_prompt_id), una dimensione (count)
            bubbles.append({
                'name': row['jail_prompt_id'],
                'value': row['count']
            })
        
        series_data.append({
            'name': model,
            'data': bubbles
        })

    # Configurazione del grafico
    chartDef = {
        'chart': {
            'height': '100%',
            'type': 'packedbubble'
        },
        'plotOptions': {
            'packedbubble': {
                'dataLabels': {
                    'enabled': True,
                    'filter': {
                        'operator': '>',
                        'property': 'y',
                        'value': 1
                    },
                    'format': '{point.name}',
                    'style': {
                        'color': 'black',
                        'fontWeight': 'normal',
                        'textOutline': 'none'
                    }
                },
                'layoutAlgorithm': {
                    'dragBetweenSeries': True,
                    'gravitationalConstant': 0.05,
                    'parentNodeLimit': True,
                    'seriesInteraction': False,
                    'splitSeries': True
                },
                'maxSize': '100%',
                'minSize': '40%',
                'zMax': 1000,
                'zMin': 0
            }
        },
        'series': series_data,
        'title': {
            'text': 'Jailbreak Success Distribution by Model and Prompt'
        },
        'tooltip': {
            'pointFormat': '<b>{point.name}:</b> {point.value} successes',
            'useHTML': True
        }
    }

    # Visualizzazione in Streamlit (se il componente hg è installato)
    hg.streamlit_highcharts(chartDef, 650)


with elements("response_charts"):
    st.markdown("""### 2.1. Response e Jailbreak Success""")
    st.markdown("""**Descrizione**:""") 
    st.markdown("""In questa sezione si analizza la distribuzione delle richieste evase con successo per ciascun modello. In particolare si vuole evidenziare la percentuale delle risposte evase in presenza di successi di jailbreak.""") 
    

    #PERCENTUALE DI RESPONSE TRUE SU JAIL TRUE TOTALE 
    # Filtra i dati in cui jailbreak_success è True
    df_filtered = df[df['jailbreak_success'] == True]

    # Calcola la percentuale di Response = True
    response_true = df_filtered['response'].sum()
    total_success = len(df_filtered)
    percentage_response_true = (response_true / total_success) * 100

    # Prepara i dati per il grafico
    chart_data = {
        'chart': {
            'type': 'pie'
        },
        'title': {
            'text': 'Percentuale di Response True rispetto a Jailbreak Success'
        },
        'series': [{
            'name': 'Response',
            'data': [
                {'name': 'Response True', 'y': percentage_response_true},
                {'name': 'Response False', 'y': 100 - percentage_response_true}
            ]
        }]
    }

    # Visualizza il grafico
    hg.streamlit_highcharts(chart_data)
    
    # Filtra il dataframe per response=True e jailbreak_success=True
    filtered_df = df[(df["response"] == True) & (df["jailbreak_success"] == True)]

    # Calcola la distribuzione per ciascun model_name
    distribution = filtered_df["model_name"].value_counts().reset_index()
    distribution.columns = ["model_name", "count"]

    # Lista di colori distinti per ciascun model_name
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]  # Puoi aggiungere altri colori
    model_names = distribution["model_name"].tolist()

    # Associa ogni model_name a un colore specifico (assicurati che i colori siano abbastanza per tutti i model_names)
    color_map = {model_name: colors[i % len(colors)] for i, model_name in enumerate(model_names)}

    # Crea una lista di serie con colori distinti per il primo grafico (distribuzione per model_name)
    series_data_1 = [
        {
            "name": row["model_name"],
            "data": [row["count"]],
            "color": color_map[row["model_name"]],  # Usa il colore associato
        }
        for i, row in distribution.iterrows()
    ]

    # Configura il primo grafico
    chart_data_1 = {
        "chart": {"type": "column"},
        "title": {"text": "Occorrenze di richieste evase con jailbreak per ciascun modello"},
        "xAxis": {"categories": ["Response True & Jailbreak Success"], "title": {"text": "Criterio"}},
        "yAxis": {"title": {"text": "Occorrenze"}},
        "series": series_data_1,
        "legend": {"layout": "vertical", "align": "right", "verticalAlign": "middle"},
    }

    
    #st.write("Grafico interattivo:")
    hg.streamlit_highcharts(chart_data_1, 450)

    # Conta le occorrenze per ciascun jail_prompt_id e model_name
    grouped_df = filtered_df.groupby(["jail_prompt_id", "model_name"]).size().reset_index(name="count")

    # Converte esplicitamente i valori in tipo int per evitare problemi di serializzazione
    grouped_df["count"] = grouped_df["count"].astype(int)  # Assicura che 'count' sia int

    # Ordina correttamente i jail_prompt_id numericamente
    grouped_df["jail_prompt_id_num"] = grouped_df["jail_prompt_id"].str.extract('(\d+)').astype(int)
    grouped_df = grouped_df.sort_values("jail_prompt_id_num")

    # Lista di jail_prompt_id e model_name
    jail_prompt_ids = grouped_df["jail_prompt_id"].unique().tolist()
    model_names = grouped_df["model_name"].unique().tolist()

    # Crea una serie per ciascun model_name con dati per ogni jail_prompt_id
    series_data_2 = [
        {
            "name": model,
            "data": [
                int(grouped_df[(grouped_df["jail_prompt_id"] == jail_prompt_id) & (grouped_df["model_name"] == model)]["count"].sum())
                if jail_prompt_id in grouped_df["jail_prompt_id"].values else 0
                for jail_prompt_id in jail_prompt_ids
            ],
            "color": color_map[model],  # Usa il colore associato al model_name
        }
        for model in model_names
    ]

    # Configura il secondo grafico
    chart_data_2 = {
        "chart": {
            "type": "column",
            "zoomType": "x",  # Permette lo zoom sull'asse X
        },
        "title": {"text": "Distribuzione per ciascun Jailbreak_Prompt e Modello"},
        "xAxis": {
            "categories": jail_prompt_ids,
            "title": {"text": "Jail Prompt ID"},
            "min": 0,
            "max": len(jail_prompt_ids) - 1,
            "tickInterval": 1,  # Intervallo tra le etichette
            "type": "category"  # Forza il tipo di dato a categoria per evitare errori con i valori numerici
        },
        "yAxis": {"title": {"text": "Occorrenze"}},
        "series": series_data_2,
        "legend": {
            "layout": "horizontal",  # Dispone la legenda orizzontalmente
            "align": "center",  # Centra la legenda
            "verticalAlign": "bottom",  # Posiziona la legenda in basso
            "x": 0,  # Allinea orizzontalmente
            "y": 10,  # Distanza dalla parte inferiore
        },
        "tooltip": {"shared": True},
        "plotOptions": {
            "column": {
                "dataLabels": {"enabled": True}
            }
        },
    }

    # Visualizza il secondo grafico
    #st.write("Grafico interattivo per Jail Prompt ID:")
    hg.streamlit_highcharts(chart_data_2, 700)





with elements("chart_style"):
    
    # Grafico 2: Distribuzione Aderenza allo Stile
    st.markdown("""#### 3. Style Consistency""")  
    st.markdown("""**Descrizione**:  
    -Un grafico che rappresenta la distribuzione dei punteggi assegnati all'aderenza allo stile richiesto dai prompt.  
    -Utilizza un istogramma arricchito con la densità (KDE) per visualizzare la forma della distribuzione.                      
    **Motivazione**:  
    L'aderenza allo stile è una metrica importante per valutare se il modello segue le istruzioni stilistiche fornite nei prompt di jailbreak. Una distribuzione ben definita può indicare coerenza nelle risposte.                
    **Cosa Mostra**:  
    -La frequenza dei punteggi su una scala da 1 a 5.  
    -La tendenza del modello a rispettare o meno lo stile richiesto.
    """)

     # Creazione di intervalli per la distribuzione
    df["style_consistency_range"] = pd.cut(
        df["style_consistency"], bins=[0, 2, 4, 5], labels=["1-2", "3-4", "5"]
    )

    # Dati per il grafico a barre (media di style_consistency per modello)
    bar_data = df.groupby("model_name")["style_consistency"].mean().reset_index()
    categories = bar_data["model_name"].tolist()
    bar_values = bar_data["style_consistency"].tolist()



    # Calcolare il conteggio di style_consistency per ogni modello
    style_counts = df.groupby(["model_name", "style_consistency"]).size().unstack(fill_value=0)

    # Creazione della definizione del grafico
    chartDef = {
        "chart": {"type": "column"},
        "title": {"text": "Distribution of Style Consistency per Model"},
        "xAxis": {
            "categories": style_counts.index.tolist(),
            "title": {"text": "Model Name"}
        },
        "yAxis": {
            "min": 0,
            "title": {"text": "Count"}
        },
        "series": [
            {
                "name": f"Style Consistency {col}",
                "data": style_counts[col].tolist(),
            }
            for col in style_counts.columns
        ]
    }

    # Visualizzazione del grafico
    hg.streamlit_highcharts(chartDef, 640)


    # Dati per il grafico a torta (distribuzione degli intervalli)

    pie_data = pd.DataFrame(columns=['range', 'count'])
    pie_data['range'] = ['1-2', '3-4', '5']
    pie_data['count'] = [0, 0, 0] # Inizializza tutti i valori a 0
    pie_data.at[0, 'count'] = df[df['style_consistency_range'] == '1-2'].shape[0]
    pie_data.at[1, 'count'] = df[df['style_consistency_range'] == '3-4'].shape[0]
    pie_data.at[2, 'count'] = df[df['style_consistency_range'] == '5'].shape[0]

    pie_values = [{'name': row['range'], 'y': row['count']} for _, row in pie_data.iterrows()]


    # Configurazione del grafico
    chart_style = {
        "labels": {
            "items": [
                {
                    "html": "Distribution of Style Consistency",
                    "style": {"color": "black", "left": "50px", "top": "18px"},
                }
            ]
        },
        "series": [
            {
                "data": bar_values,
                "name": "Average Style Consistency",
                "type": "column",
                "colorByPoint": True,
            },
            {
                "center": [500, 10],
                "data": pie_values,
                "dataLabels": {"enabled": True},
                "name": "Consistency Range",
                "showInLegend": True,
                "size": 100,
                "type": "pie",
            },
        ],
        "title": {
            "text": "Style Consistency Analysis",
            "align": "left",
        },
        "xAxis": {"categories": categories, "title": {"text": "Model Name"}},
        "yAxis": {"title": {"text": "Style Consistency (Average)"}},
    }

    # Visualizzazione del grafico con streamlit_highcharts
    hg.streamlit_highcharts(chart_style, height=540)

    
      # Raggruppiamo per model_name e jail_prompt_id e calcoliamo la media di style_consistency per ogni gruppo
    df_grouped = df.groupby(['model_name', 'jail_prompt_id'])['style_consistency'].mean().reset_index()
    
        # Aggiungi una colonna temporanea per la parte numerica di 'jail_prompt_id'
    df_grouped['jail_number'] = df_grouped['jail_prompt_id'].str.extract('(\d+)').astype(int)

    # Ordina il dataframe in base al numero estratto
    df_grouped = df_grouped.sort_values(by='jail_number')

    # Crea una lista ordinata per le categorie dell'asse X
    x_categories = df_grouped['jail_prompt_id'].unique().tolist()

    # Elimina la colonna temporanea (opzionale, se non serve più)
    df_grouped = df_grouped.drop(columns=['jail_number'])

    # Creiamo una lista di dati per ciascun 'model_name'
    series_data = []
    model_names = df_grouped['model_name'].unique()

    for model in model_names:
        model_data = df_grouped[df_grouped['model_name'] == model]
        series_data.append({
            'name': model,
            'data': model_data['style_consistency'].tolist()
        })

    # Definizione del grafico Highcharts
    chartDef = {
        'chart': {
            'type': 'line',  # Puoi cambiare il tipo di grafico, ad esempio 'streamgraph', 'line', ecc.
            'zoomType': 'x'
        },
        'title': {
            'text': 'Style Consistency Scores per ciascun Model e Jail Prompt'
        },
        'xAxis': {
            'categories': x_categories, 
            'crosshair': True
        },
        'yAxis': {
            'title': {
                'text': 'Style Consistency Score'
            }
        },
        'legend': {
            'enabled': True
        },
        'series': series_data,  # I dati per le serie dei vari modelli
        'plotOptions': {
            'line': {
                'dataLabels': {
                    'enabled': False
                },
                'enableMouseTracking': True
            }
        }
    }

    # Mostriamo il grafico in Streamlit
    hg.streamlit_highcharts(chartDef, 750)          

# consistency 

with elements("chart_consistency"):
    st.markdown("""### 4. Consistency Score""")
    st.markdown("""**Descrizione**:  
-Questo grafico rappresenta la distribuzione dei punteggi di consistenza, ovvero la capacità del modello di rispondere direttamente alla richiesta senza essere evasivo.             
**Motivazione**:  
La consistenza delle risposte è una metrica chiave per comprendere se il modello è in grado di soddisfare la richiesta senza eludere la domanda, pur rispettando le sue policy.             
**Cosa Mostra**:  
-La frequenza dei punteggi di consistenza (1-5).  
-La capacità dei modelli di fornire risposte precise.
""")
    

    # Creazione di intervalli per la distribuzione
    df["consistency_range"] = pd.cut(
        df["consistency"], bins=[0, 2, 4, 5], labels=["1-2", "3-4", "5"]
    )

    # Calcolare il conteggio di style_consistency per ogni modello
    style_counts = df.groupby(["model_name", "consistency"]).size().unstack(fill_value=0)

    # Creazione della definizione del grafico
    chartDef = {
        "chart": {"type": "column"},
        "title": {"text": "Distribution of Consistency per Model"},
        "xAxis": {
            "categories": style_counts.index.tolist(),
            "title": {"text": "Model Name"}
        },
        "yAxis": {
            "min": 0,
            "title": {"text": "Count"}
        },
        "series": [
            {
                "name": f"Consistency Score {col}",
                "data": style_counts[col].tolist(),
            }
            for col in style_counts.columns
        ]
    }

    # Visualizzazione del grafico
    hg.streamlit_highcharts(chartDef, 640)

    # Dati per il grafico a barre (media di style_consistency per modello)
    bar_data = df.groupby("model_name")["consistency"].mean().reset_index()
    categories = bar_data["model_name"].tolist()
    bar_values = bar_data["consistency"].tolist()

    # Dati per il grafico a torta (distribuzione degli intervalli)
    pie_data = pd.DataFrame(columns=['range', 'count'])
    pie_data['range'] = ['1-2', '3-4', '5']
    pie_data['count'] = [0, 0, 0] # Inizializza tutti i valori a 0
    pie_data.at[0, 'count'] = df[df['consistency_range'] == '1-2'].shape[0]
    pie_data.at[1, 'count'] = df[df['consistency_range'] == '3-4'].shape[0]
    pie_data.at[2, 'count'] = df[df['consistency_range'] == '5'].shape[0]

    pie_values = [{"name": row["range"], "y": row["count"]} for _, row in pie_data.iterrows()]

    # Configurazione del grafico
    chart_style = {
        "labels": {
            "items": [
                {
                    "html": "Distribution of Consistency",
                    "style": {"color": "black", "left": "50px", "top": "18px"},
                }
            ]
        },
        "series": [
            {
                "data": bar_values,
                "name": "Average Consistency",
                "type": "column",
                "colorByPoint": True,
            },
            {
                "center": [500, 0],
                "data": pie_values,
                "dataLabels": {"enabled": True},
                "name": "Consistency Range",
                "showInLegend": True,
                "size": 50,
                "type": "pie",
            },
        ],
        "title": {
            "text": "Consistency Analysis",
            "align": "left",
        },
        "xAxis": {"categories": categories, "title": {"text": "Model Name"}},
        "yAxis": {"title": {"text": "Consistency (Average)"}},
    }

    # Visualizzazione del grafico con streamlit_highcharts
    hg.streamlit_highcharts(chart_style, height=540)
    
      # Raggruppiamo per model_name e jail_prompt_id e calcoliamo la media di style_consistency per ogni gruppo
    df_grouped = df.groupby(['model_name', 'jail_prompt_id'])['consistency'].mean().reset_index()
         # Aggiungi una colonna temporanea per la parte numerica di 'jail_prompt_id'
    df_grouped['jail_number'] = df_grouped['jail_prompt_id'].str.extract('(\d+)').astype(int)

    # Ordina il dataframe in base al numero estratto
    df_grouped = df_grouped.sort_values(by='jail_number')

    # Crea una lista ordinata per le categorie dell'asse X
    x_categories = df_grouped['jail_prompt_id'].unique().tolist()

    # Elimina la colonna temporanea (opzionale, se non serve più)
    df_grouped = df_grouped.drop(columns=['jail_number'])

    # Creiamo una lista di dati per ciascun 'model_name'
    series_data = []
    model_names = df_grouped['model_name'].unique()

    for model in model_names:
        model_data = df_grouped[df_grouped['model_name'] == model]
        series_data.append({
            'name': model,
            'data': model_data['consistency'].tolist()
        })

    # Definizione del grafico Highcharts
    chartDef = {
        'chart': {
            'type': 'line',  # Puoi cambiare il tipo di grafico, ad esempio 'streamgraph', 'line', ecc.
            'zoomType': 'x'
        },
        'title': {
            'text': 'Consistency Scores per ciascun Model e Jail Prompt'
        },
        'xAxis': {
            'categories': x_categories,  # Usato per le etichette dell'asse X
            'crosshair': True
        },
        'yAxis': {
            'title': {
                'text': 'Consistency Score'
            }
        },
        'legend': {
            'enabled': True
        },
        'series': series_data,  # I dati per le serie dei vari modelli
        'plotOptions': {
            'line': {
                'dataLabels': {
                    'enabled': False
                },
                'enableMouseTracking': True
            }
        }
    }

    # Mostriamo il grafico in Streamlit
    hg.streamlit_highcharts(chartDef, 750) 

with elements("chart_severity"):
  st.markdown("""### 5. Severity Score""")
  st.markdown("""**Descrizione**:  
  -Mostra come si distribuiscono i punteggi di gravità assegnati alle risposte dei modelli, indicando il livello di severità o permissività.  
  **Motivazione**:  
  La gravità della risposta è un indicatore del livello di moderazione applicato dal modello nelle sue risposte, in particolare per richieste eticamente discutibili.                       
  **Cosa Mostra**:  
  -Se i modelli tendono a rispondere in modo più permissivo o restrittivo.  
  -Le variazioni di severità nelle risposte. """)

  #TOGGLE BUTTON 
  typo = st.toggle("Severity distribution per model", True)

  if typo:
    # Supponiamo che 'df' sia il tuo dataframe
    df['severity'] = pd.to_numeric(df['severity'], errors='coerce')

    # Raggruppiamo i dati per model_name e calcoliamo la media di severity per ciascun modello
    aggregated_data = df.groupby('model_name')['severity'].mean().reset_index()

    # Creiamo i dati per la serie
    tile_data = [
        {
            'hc-a2': model,
            'name': model,
            'value': severity,
            'x': idx,  # Puoi scegliere una logica per assegnare valori x
            'y': 0,  # Posizionamento statico, puoi modificarlo per ordinarli
        }
        for idx, (model, severity) in enumerate(zip(aggregated_data['model_name'], aggregated_data['severity']))
    ]

    # Definiamo il grafico
    chartDef = {
        'chart': {
            'height': '70%',
            'type': 'tilemap'
        },
        'colorAxis': {
            'dataClasses': [
                {'color': '#FF2371', 'from': 4.5, 'name': 'Severity 5', 'to': 5},
                {'color': '#FF7987', 'from': 3.5, 'name': 'Severity 4', 'to': 4.5},
                {'color': '#FFC428', 'from': 2.5, 'name': 'Severity 3', 'to': 3.5},
                {'color': '#F9EDB3', 'from': 1.5, 'name': 'Severity 2', 'to': 2.5},
                {'color': '#D3F5D9', 'from': 0, 'name': 'Severity 1', 'to': 1.5}
            ]
        },
        'plotOptions': {
            'series': {
                'dataLabels': {
                    'color': '#000000',
                    'enabled': True,
                    'format': '{point.hc-a2}',
                    'style': {'textOutline': False}
                }
            }
        },
        'series': [{
            'data': tile_data,
            'name': 'Severity Scores'
        }],
        'subtitle': {
            'text': 'Source: Custom Data'
        },
        'title': {
            'text': 'Model Severity Scores'
        },
        'tooltip': {
            'headerFormat': '',
            'pointFormat': 'The severity score of <b>{point.name}</b> is <b>{point.value}</b>'
        },
        'xAxis': {'visible': False},
        'yAxis': {'visible': False}
    }

    # Visualizzazione del grafico in Streamlit
    hg.streamlit_highcharts(chartDef, 540)
  else:
    # per ciascun jail_prompt_id, calcoliamo la media di severity per ciascun model_name 

    # Supponiamo che 'df' sia il tuo dataframe
    df['severity'] = pd.to_numeric(df['severity'], errors='coerce')

    # Raggruppiamo i dati per jail_prompt_id e calcoliamo la media di severity per ciascun jail_prompt_id
    aggregated_data = df.groupby('jail_prompt_id')['severity'].mean().reset_index()

    # Creiamo i dati per la serie
    tile_data = [
        {
            'hc-a2': jail_prompt,  # Ogni 'jail_prompt_id'
            'name': jail_prompt,   # Nome associato al 'jail_prompt_id'
            'value': severity,     # Il valore medio della severity
            'x': idx,  # Puoi scegliere una logica per assegnare valori x
            'y': 0,     # Posizionamento statico
        }
        for idx, (jail_prompt, severity) in enumerate(zip(aggregated_data['jail_prompt_id'], aggregated_data['severity']))
    ]

    # Definiamo il grafico
    chartDef = {
        'chart': {
            'height': '70%',
            'type': 'tilemap'
        },
        'colorAxis': {
            'dataClasses': [
                {'color': '#FF2371', 'from': 4.5, 'name': 'Severity 5', 'to': 5},
                {'color': '#FF7987', 'from': 3.5, 'name': 'Severity 4', 'to': 4.5},
                {'color': '#FFC428', 'from': 2.5, 'name': 'Severity 3', 'to': 3.5},
                {'color': '#F9EDB3', 'from': 1.5, 'name': 'Severity 2', 'to': 2.5},
                {'color': '#D3F5D9', 'from': 0, 'name': 'Severity 1', 'to': 1.5}
            ]
        },
        'plotOptions': {
            'series': {
                'dataLabels': {
                    'color': '#000000',
                    'enabled': True,
                    'format': '{point.hc-a2}',
                    'style': {'textOutline': False}
                }
            }
        },
        'series': [{
            'data': tile_data,
            'name': 'Severity Scores'
        }],
        'subtitle': {
            'text': 'Source: Custom Data'
        },
        'title': {
            'text': 'Jail Prompt Severity Scores'
        },
        'tooltip': {
            'headerFormat': '',
            'pointFormat': 'The severity score of <b>{point.name}</b> is <b>{point.value}</b>'
        },
        'xAxis': {'visible': False},
        'yAxis': {'visible': False}
    }

    # Visualizzazione del grafico in Streamlit
    hg.streamlit_highcharts(chartDef, 540)


with elements("chart_disclaimer"):
    st.markdown("""### 6. Disclaimer""") 
    st.markdown("""**Descrizione**:  
              - Confronta la presenza di disclaimer nelle risposte (`True`/`False`) per ciascun modello.  
              - Ogni barra rappresenta il conteggio di risposte con o senza disclaimer per un modello specifico.                                      
              **Motivazione**:  
              I disclaimer sono un indicatore di responsabilità etica, mostrando come i modelli cercano di prevenire potenziali danni.                             
              **Cosa Mostra**:  
              - La frequenza con cui ciascun modello include disclaimer.  
              - La tendenza di ciascun modello a enfatizzare considerazioni etiche. """)
    
    # Filtriamo i dati per includere tutte le righe, indipendentemente dal valore di disclaimer
    df_disclaimer = df[['model_name', 'disclaimer']]

    # Dati per il grafico a barre (conteggio dei valori di disclaimer True e False per ogni modello)
    bar_data = df_disclaimer.groupby(['model_name', 'disclaimer']).size().unstack(fill_value=0)

    # Riorganizziamo i dati in modo che "True" e "False" siano separati in colonne
    categories = bar_data.index.tolist()
    true_values = bar_data[True].tolist()  # Conta i True per ciascun model_name
    false_values = bar_data[False].tolist()  # Conta i False per ciascun model_name

    # Configurazione del grafico
    chart_style = {
        "labels": {
            "items": [
                {
                    "html": "Disclaimer Distribution (True vs False)",
                    "style": {"color": "black", "left": "50px", "top": "18px"},
                }
            ]
        },
        "series": [
            {
                "data": true_values,
                "name": "Disclaimer True",
                "type": "column",
                "color": "#1f77b4",  # Colore per True
            },
            {
                "data": false_values,
                "name": "Disclaimer False",
                "type": "column",
                "color": "#ff7f0e",  # Colore per False
            },
        ],
        "title": {
            "text": "Disclaimer Distribution per Model",
            "align": "left",
        },
        "xAxis": {
            "categories": categories,
            "title": {"text": "Model Name"},
        },
        "yAxis": {
            "title": {"text": "Count of Disclaimer Values (True/False)"},
        },
    }

    # Visualizzazione del grafico con streamlit_highcharts
    hg.streamlit_highcharts(chart_style, height=540)
      


    
with elements("chart_distribution_jail"):
  st.markdown("""### 7. Distribution of Jailbreaking Success per Model""")
  st.markdown("""**Descrizione**:  
  -Mostra la percentuale di successo dei jailbreak per ciascun modello.                        
  **Motivazione**:  
  È utile per identificare quali modelli sono più vulnerabili al jailbreaking e quindi meno robusti.                  
  **Cosa Mostra**:  
  -Il livello di successo dei jailbreak su diversi modelli.  
  -Quali modelli richiedono maggiore attenzione per mitigare i prompt di jailbreak. """)
  # Calcoliamo la percentuale di successo del jailbreak per ciascun model_name
  success_percentage = (
      df.groupby("model_name")["jailbreak_success"]
      .apply(lambda x: (x == True).mean() * 100)  # Calcoliamo la percentuale di successo
      .reset_index()
      .rename(columns={"jailbreak_success": "success_percentage"})
  )

  # Dati per il grafico a barre (percentuale di successo per ciascun model_name)
  categories = success_percentage["model_name"].tolist()
  bar_values = success_percentage["success_percentage"].tolist()

  # Configurazione del grafico
  chart_style = {
      "labels": {
          "items": [
              {
                  "html": "Jailbreak Success Percentage per Model",
                  "style": {"color": "black", "left": "50px", "top": "18px"},
              }
          ]
      },
      "series": [
          {
              "data": bar_values,
              "name": "Jailbreak Success Percentage",
              "type": "column",
              "colorByPoint": True,
          }
      ],
      "title": {
          "text": "Jailbreak Success Percentage Analysis",
          "align": "left",
      },
      "xAxis": {
          "categories": categories,
          "title": {"text": "Model Name"},
      },
      "yAxis": {
          "title": {"text": "Success Percentage (%)"},
          "max": 100,  # Impostiamo il limite massimo dell'asse Y a 100%
      },
  }

  # Visualizzazione del grafico con streamlit_highcharts
  hg.streamlit_highcharts(chart_style, height=540)


with elements("chart_correlation"):
    st.markdown("""### 8. Correlation Matrix""")   
    st.markdown("""**Descrizione**:  
                -Una matrice che mostra le correlazioni tra le metriche numeriche (aderenza allo stile, consistenza e gravità).            
                **Motivazione**:  
                Le correlazioni aiutano a individuare relazioni significative tra le metriche. Ad esempio, un'alta correlazione tra "gravità" e "consistenza" potrebbe suggerire che risposte più consistenti tendono a essere più severe.                      
                **Cosa Mostra**:  
                -Relazioni positive o negative tra le metriche.  
                -Quali metriche sono più strettamente correlate. """)
    

    # Selezioniamo le colonne numeriche per il calcolo della correlazione
    correlation_columns = ['style_consistency', 'consistency', 'severity', 'jailbreak_success']
    df_corr = df[correlation_columns].copy()

    # Calcoliamo la matrice di correlazione
    correlation_matrix = df_corr.corr()

    # Impostiamo la dimensione della figura per il grafico
    plt.figure(figsize=(8, 6))

    # Creiamo la mappa di calore (heatmap)
    sns.heatmap(correlation_matrix, annot=True, cmap="crest", vmin=-1, vmax=1, cbar=True, square=True)

    # Titolo e etichette
    plt.title('Correlation Matrix Between Metrics', fontsize=14)
    plt.tight_layout()

    # Visualizza il grafico con Streamlit
    st.pyplot(plt)


with elements("chart_note"):
    
      st.markdown("""### 9. Comparative Boxplot of Metrics per Model""")  
      st.markdown("""**Descrizione**:  
    -Un grafico che mostra la distribuzione di tre metriche principali (aderenza allo stile, consistenza, gravità) per ciascun modello.                       
    **Motivazione**:  
    Un boxplot comparativo permette di confrontare i modelli in termini di performance su più dimensioni contemporaneamente.                 
    **Cosa Mostra**:  
    -La variabilità delle metriche per ogni modello.  
    -Se esistono differenze significative tra i modelli su una metrica specifica. """)
       
      # Raccogliamo le metriche in un formato lungo per seaborn
      df_long = df.melt(id_vars=["model_name"], value_vars=["style_consistency", "consistency", "severity"],
                        var_name="metric", value_name="score")

      # Creiamo il boxplot
      plt.figure(figsize=(12, 6))
      sns.boxplot(x="model_name", y="score", hue="metric", data=df_long, palette="Set2")

      # Aggiungiamo il titolo e le etichette
      plt.title("Comparative Boxplot of Metrics (style_consistency, consistency, severity)", fontsize=14)
      plt.xlabel("Model Name", fontsize=12)
      plt.ylabel("Score", fontsize=12)

      # Visualizza il grafico in Streamlit
      st.pyplot(plt)

with elements("jail_vs_nojail"):

    st.markdown("""### 10. Comparison of Metrics between Jailbreak and No Jailbreak""")

    df_nojail = load_json_nojail(nojail_results_folder)
    st.markdown(f"**Numero di record: {len(df_nojail)}**")
    st.dataframe(df_nojail, width=1000, height=300, hide_index=True)

    st.markdown("""**La sola richiesta evasa in modo consistente è la seguente:**""")
  
    ex = load(only_nojail_example)
    display_chat(ex, 'box3')
    st.divider()
    
    st.markdown("""**# Jailbreak Success vs Response (Non Jailbroken)**""")
    st.markdown("""Aggregare i valori di jailbreak_success per ciascun jail_prompt_id calcolando la media consente di ottenere un unico valore rappresentativo per ogni combinazione di model_name e req_id. Successivamente, puoi confrontare questo valore con i dati del dataframe df_nojail. """)

        ###SPIEGARE BENE CHE VIENE EFFETTUATA LA MEDIA DI JAILBREAK_SUCCESS PER CIASCUN JAILBREAK_PROMPT E POI VIENE FATTO IL CONFRONTO TRA JAIL_SUCCESS_MEDIO E RESPONSE PER OGNI MODEL E REQ_ID
    # 1. Aggrega df per calcolare la media di jailbreak_success per ogni model_name e req_id
    df_agg = df.groupby(['model_name', 'req_id']).agg(
        avg_jailbreak_success=('jailbreak_success', 'mean')  # Media su tutti i jail_prompt_id
    ).reset_index()

    # 2. Effettua il merge con df_nojail
    merged_df = pd.merge(df_agg, df_nojail, on=['model_name', 'req_id'], how='inner')

    # 3. Calcola la differenza tra la media di jailbreak_success e response
    merged_df['success_difference'] = merged_df['avg_jailbreak_success'] - merged_df['response'].astype(int)

    # 4. Crea la tabella pivot per la heatmap
    pivot_table = merged_df.pivot_table(
        index='model_name', columns='req_id', values='success_difference', aggfunc='mean'
    )

    # 5. Visualizza la heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, annot=True, cmap='coolwarm', cbar_kws={'label': 'Differenza (Media Jailbreak - Response)'})
    plt.title("Heatmap delle Differenze tra Media Jailbreak Success e Response")
    plt.ylabel("Model Name")
    plt.xlabel("Request ID")
    st.pyplot(plt)

    st.markdown("""**# Jailbreak Consistency vs NoJail Consistency**""")
    st.markdown(""" In risposte jailbroken, ci si aspetta una alta consistenza. In risposte non jailbroken, la consistenza dovrebbe essere bassa, in quanto il modello non sta cercando di evitare o manipolare la richiesta.                       """)
    st.markdown("""**N.B. La grandezza dei punti dipende dal valore di severity**""")
   # Aggrega df per calcolare la media di consistency per ogni model_name e req_id
    df_agg_consistency = df.groupby(['model_name', 'req_id']).agg(
        avg_consistency=('consistency', 'mean')  # Media su tutti i jail_prompt_id
    ).reset_index()

    # Merge con df_nojail
    merged_consistency = pd.merge(
        df_agg_consistency, 
        df_nojail[['model_name', 'req_id', 'consistency', 'severity']].rename(columns={'consistency': 'nojail_consistency'}), 
        on=['model_name', 'req_id']
    )

    # Genera una serie separata per ogni model_name
    series_data = []
    unique_models = merged_consistency['model_name'].unique()

    # Funzione per mappare la severity alla dimensione dei punti
    def map_severity_to_size(severity):
        #return 10 + severity * 5  # Scala la dimensione tra 10 e 35 (ad esempio)
        return severity 

    for model in unique_models:
        model_data = merged_consistency[merged_consistency['model_name'] == model]
        scatter_data = [
            {
                "x": row["avg_consistency"], 
                "y": row["nojail_consistency"], 
                "name": f"{row['model_name']} (req_id: {row['req_id']})",
                "marker": {
                    "radius": map_severity_to_size(row["severity"])  # Imposta la dimensione del punto
                }
            } 
            for _, row in model_data.iterrows()
        ]
        series_data.append({
            "name": model,
            "data": scatter_data
        })

    # Configurazione del grafico Highcharts
    scatter_chart = {
        "chart": {
            "type": "scatter",
            "zoomType": "xy"
        },
        "title": {
            "text": "Consistency Correlation (Jailbreak vs No Jailbreak)"
        },
        "xAxis": {
            "title": {
                "text": "Average Consistency (Jailbreak)"
            }
        },
        "yAxis": {
            "title": {
                "text": "Consistency (No Jailbreak)"
            }
        },
        "tooltip": {
            "headerFormat": "<b>{point.name}</b><br>",
            "pointFormat": "Jailbreak Consistency: {point.x}, No Jailbreak Consistency: {point.y}<br>Severity: {point.marker.radius}"
        },
        "series": series_data
    }

    # Visualizza il grafico in Streamlit
    hg.streamlit_highcharts(scatter_chart, height=550)




    st.markdown("""**# Confronto della Coerenza dello Stile (Style Consistency)**""")
    st.markdown("""Risposte jailbroken potrebbero mostrare più flessibilità nel seguire lo stile, o potrebbero esserci delle difficoltà nel mantenere uno stile coerente se il modello è distratto da tentativi di evasione.
Risposte non jailbroken potrebbero avere uno stile più neutro e coerente, a meno che non venga richiesto uno stile specifico dal prompt.""")
    
    # Uniamo i dati di df e df_nojail
    df_merged_style = pd.merge(
        df[['model_name', 'req_id', 'style_consistency']].rename(columns={'style_consistency': 'jailbreak_style_consistency'}),
        df_nojail[['model_name', 'req_id', 'style_consistency']].rename(columns={'style_consistency': 'nojail_style_consistency'}),
        on=['model_name', 'req_id']
    )

    # Creiamo un dataframe lungo per il violin plot
    melted_df = pd.melt(df_merged_style, id_vars=['model_name', 'req_id'], value_vars=['jailbreak_style_consistency', 'nojail_style_consistency'],
                        var_name='Scenario', value_name='style_consistency')

    # Creiamo il violin plot
    plt.figure(figsize=(12, 8))
    sns.violinplot(x='model_name', y='style_consistency', hue='Scenario', data=melted_df, split=True, inner="quart", palette="muted", fill = False, gap = .2)
    
    # Aggiungiamo il titolo e le etichette
    plt.title('Confronto della Style Consistency tra Jailbreak e NoJailbreak')
    plt.xlabel('Model Name')
    plt.ylabel('Style Consistency')

    # Mostriamo il grafico in Streamlit
    st.pyplot(plt)

    # interattivo
    # Aggrega df per calcolare la media di style_consistency per ogni model_name e req_id
    df_agg_style_consistency = df.groupby(['model_name', 'req_id']).agg(
        avg_style_consistency=('style_consistency', 'mean')  # Media su tutti i jail_prompt_id
    ).reset_index()

    # Merge con df_nojail
    merged_style_consistency = pd.merge(
        df_agg_style_consistency, 
        df_nojail[['model_name', 'req_id', 'style_consistency']].rename(columns={'style_consistency': 'nojail_style_consistency'}), 
        on=['model_name', 'req_id']
    )

    # Genera una serie separata per ogni model_name
    series_data = []
    unique_models = merged_style_consistency['model_name'].unique()

    for model in unique_models:
        model_data = merged_style_consistency[merged_style_consistency['model_name'] == model]
        scatter_data = [
            {
                "x": row["avg_style_consistency"], 
                "y": row["nojail_style_consistency"], 
                "name": f"{row['model_name']} (req_id: {row['req_id']})"
            } 
            for _, row in model_data.iterrows()
        ]
        series_data.append({
            "name": model,
            "data": scatter_data
        })

    # Configurazione del grafico Highcharts
    style_consistency_chart = {
        "chart": {
            "type": "scatter",
            "zoomType": "xy"
        },
        "title": {
            "text": "Style Consistency Comparison (Jailbreak vs No Jailbreak)"
        },
        "xAxis": {
            "title": {
                "text": "Average Style Consistency (Jailbreak)"
            }
        },
        "yAxis": {
            "title": {
                "text": "Style Consistency (No Jailbreak)"
            }
        },
        "tooltip": {
            "headerFormat": "<b>{point.name}</b><br>",
            "pointFormat": "Jailbreak Style Consistency: {point.x}, No Jailbreak Style Consistency: {point.y}"
        },
        "series": series_data
    }

    # Visualizza il grafico in Streamlit
    hg.streamlit_highcharts(style_consistency_chart, height=550)




    st.markdown("""**# Confronto dei Disclaimer**""")

   # Conteggio di True e False per Disclaimer in df
    df_disclaimer_counts = df['disclaimer'].value_counts()

    # Conteggio di True e False per Disclaimer in df_nojail
    df_nojail_disclaimer_counts = df_nojail['disclaimer'].value_counts()

    # Visualizzazione in un grafico a barre
    labels = ['True', 'False']
    df_disclaimer_percentage = df_disclaimer_counts / df.shape[0] * 100
    df_nojail_disclaimer_percentage = df_nojail_disclaimer_counts / df_nojail.shape[0] * 100

    fig, ax = plt.subplots(figsize=(8, 6))

    # Grafico a barre
    width = 0.35  # larghezza delle barre
    x = range(len(labels))
    ax.bar(x, df_disclaimer_percentage, width, label='Jailbreak', color='lightblue')
    ax.bar([p + width for p in x], df_nojail_disclaimer_percentage, width, label='No Jailbreak', color='salmon')

    ax.set_xticks([p + width / 2 for p in x])
    ax.set_xticklabels(labels)
    ax.set_ylabel('Percentage (%)')
    ax.set_title('Comparison of Disclaimer (True/False)')

    ax.legend()
    st.pyplot(fig)


    st.markdown("""**# Confronto della Severità della Risposta (Severity)**""")

    # Calcolare la severity media per ciascun model_name in df
    df_severity_mean = df.groupby('model_name')['severity'].mean()

    # Calcolare la severity media per ciascun model_name in df_nojail
    df_nojail_severity_mean = df_nojail.groupby('model_name')['severity'].mean()

    # Unire i due DataFrame in un unico per confronto
    severity_comparison = pd.DataFrame({
        'jail_severity': df_severity_mean,
        'nojail_severity': df_nojail_severity_mean
    }).fillna(0)

    severity_comparison.reset_index(inplace=True)

    # Creare una lista di colori distintivi per ciascun model_name
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    # Creare il grafico con streamlit_highcharts
    activity_charts = {
        'chart': {
            'type': 'column',
            'height': '60%'
        },
        'title': {
            'text': 'Average Severity Comparison by Model Name'
        },
        'xAxis': {
            'categories': severity_comparison['model_name'].tolist(),
            'title': {
                'text': 'Model Name'
            }
        },
        'yAxis': {
            'min': 0,
            'title': {
                'text': 'Average Severity',
                'align': 'high'
            },
            'labels': {
                'overflow': 'justify'
            }
        },
        'series': [
            {
                'name': 'Jailbreak',
                'data': severity_comparison['jail_severity'].tolist(),
                'color': colors[0],
            },
            {
                'name': 'No Jailbreak',
                'data': severity_comparison['nojail_severity'].tolist(),
                'color': colors[1],
            }
        ],
        'tooltip': {
            'shared': True,
            'valueSuffix': ' severity'
        }
    }

    # Visualizzare il grafico
    hg.streamlit_highcharts(activity_charts, 400)

    st.markdown("""### 11. Costruzione di Metriche Derivate""")
    st.markdown(""" Si possono anche creare alcune metriche derivate che confrontano in modo più diretto le risposte jailbroken con quelle non jailbroken:                      
- **Jailbreak Impact Score:** La differenza tra la severità e la consistenza delle risposte jailbroken vs non jailbroken.                               
- **Adaptability Score:** La differenza tra l'aderenza allo stile (style consistency) nelle risposte jailbroken e non jailbroken.""")
    
    st.markdown("""**0. Calcolo del Jailbreak Impact Score**""")
    st.markdown("""Il Jailbreak Impact Score può essere definito come la differenza tra la severità e la consistenza delle risposte jailbroken rispetto a quelle non jailbroken. Questo ti permetterà di vedere quanto il jailbreaking influisce sulla gravità e sulla coerenza delle risposte.                         
                La formula per calcolare il **Jailbreak Impact Score** è:                   """)
    st.markdown("""                    
$$\t{Jailbreak Impact Score} = (\t{Severity}_{\t{jailbroken}} - \t{Consistency}_{\t{jailbroken}}) - (\t{Severity}_{\t{non jailbroken}} - \t{Consistency}_{\t{non jailbroken}})$$
""")
    st.markdown("""**1. Cosa Misura il Jailbreak Impact Score?**""") 
    st.markdown("""Il Jailbreak Impact Score calcola la differenza tra l'impatto del jailbreaking e le caratteristiche delle risposte non jailbroken in base a due parametri chiave:

- Severity: Misura la gravità della risposta, dove un punteggio più alto indica una risposta più grave.                       
- Consistency: Misura quanto la risposta è aderente alla richiesta specifica, con punteggi più alti che indicano una risposta più consistente.                   
In sostanza, il Jailbreak Impact Score cerca di rispondere alla domanda: In che modo il jailbreaking influisce sulla gravità e sulla coerenza delle risposte?""")

    st.markdown("""**2. Interpretazione di un Jailbreak Impact Score Positivo o Negativo**""")
    st.markdown("""- Se il Jailbreak Impact Score è positivo significa che le risposte jailbroken hanno una maggiore differenza (positiva) tra severità e coerenza rispetto alle risposte non jailbroken.
In altre parole, il jailbreaking potrebbe aver reso le risposte più gravi o meno coerenti rispetto a quelle non jailbroken.
Un punteggio positivo suggerisce che il jailbreaking ha un impatto maggiore sulla severità e sulla coerenza delle risposte rispetto al modello che non è jailbroken.              
- Se il Jailbreak Impact Score è negativo significa che la differenza tra severità e coerenza nelle risposte jailbroken è inferiore rispetto alle risposte non jailbroken.
In altre parole, le risposte non jailbroken potrebbero essere più gravi o più coerenti, mentre le risposte jailbroken potrebbero risultare meno gravi o più coerenti.
Un punteggio negativo implica che il jailbreaking ha avuto un minore impatto sulla gravità e sulla coerenza delle risposte rispetto al comportamento non jailbroken.""")


    st.markdown("""**3. Calcolo dell'Adaptability Score**""")
    st.markdown("""L'Adaptability Score potrebbe essere calcolato come la differenza tra l'aderenza allo stile nelle risposte jailbroken e non jailbroken. Questo ti permetterà di capire come la capacità di adattarsi allo stile richiesto cambia tra le risposte jailbroken e non jailbroken.                                
                La formula per calcolare l'**Adaptability Score** è:                    """)     
    st.markdown("""                       
$$\t{Adaptability Score} = \t{Style Consistency}_{\t{jailbroken}} - \t{Style Consistency}_{\t{non jailbroken}}$$
""")

    st.markdown("""**4. Cosa Misura l'Adaptability Score?**""")
    st.markdown("""L'Adaptability Score calcola la differenza tra la coerenza stilistica (style consistency) nelle risposte jailbroken e non jailbroken.                   
    - Style Consistency: Misura quanto la risposta si adatti allo stile definito dal prompt o dalle aspettative. Un punteggio più alto indica che la risposta è più aderente allo stile richiesto.                       
    Quindi, l'Adaptability Score cerca di rispondere alla domanda: In che modo il jailbreaking influisce sulla capacità del modello di mantenere uno stile coerente nelle risposte?""")

    st.markdown("""**5. Interpretazione di un Adaptability Score Positivo o Negativo**""")
    st.markdown("""- Se l'Adaptability Score è positivo significa che il modello jailbroken ha una migliore coerenza stilistica rispetto al modello non jailbroken.
    In altre parole, le risposte jailbroken sono più aderenti allo stile richiesto rispetto alle risposte non jailbroken.
    Un punteggio positivo suggerisce che il jailbreaking ha migliorato l'adattabilità stilistica del modello.           """)
    st.markdown("""                
    - Se l'Adaptability Score è negativo significa che il modello non jailbroken ha una migliore coerenza stilistica rispetto al modello jailbroken.
    Le risposte non jailbroken sono più aderenti allo stile rispetto alle risposte jailbroken.
    Un punteggio negativo implica che il jailbreaking ha ridotto l'adattabilità stilistica del modello.""")





    # Calcolare la severità e la consistenza media per ciascun model_name e per ciascun tipo di risposta (jailbroken vs non jailbroken)
    df_jail = df[df['jailbreak_success'] == True]
    df_nojail = df_nojail

    # Severità media per le risposte jailbroken e non jailbroken
    df_jail_severity_mean = df_jail.groupby('model_name')['severity'].mean()
    df_nojail_severity_mean = df_nojail.groupby('model_name')['severity'].mean()

    # Consistenza media per le risposte jailbroken e non jailbroken
    df_jail_consistency_mean = df_jail.groupby('model_name')['consistency'].mean()
    df_nojail_consistency_mean = df_nojail.groupby('model_name')['consistency'].mean()

    # Style Consistency per le risposte jailbroken e non jailbroken
    df_jail_style_consistency_mean = df_jail.groupby('model_name')['style_consistency'].mean()
    df_nojail_style_consistency_mean = df_nojail.groupby('model_name')['style_consistency'].mean()

    # Calcolare i Jailbreak Impact Score e Adaptability Score
    jailbreak_impact_score = (df_jail_severity_mean - df_jail_consistency_mean) - (df_nojail_severity_mean - df_nojail_consistency_mean)
    adaptability_score = df_jail_style_consistency_mean - df_nojail_style_consistency_mean

    # Creare un DataFrame per visualizzare i risultati
    scores_df = pd.DataFrame({
        'model_name': df_jail_severity_mean.index,
        'Jailbreak Impact Score': jailbreak_impact_score,
        'Adaptability Score': adaptability_score
    })

    # Visualizzazione dei risultati con streamlit_highcharts
    activity_charts = {
        'chart': {
            'type': 'column',
            'height': '60%'
        },
        'title': {
            'text': 'Jailbreak Impact and Adaptability Scores by Model'
        },
        'xAxis': {
            'categories': scores_df['model_name'].tolist(),
            'title': {
                'text': 'Model Name'
            }
        },
        'yAxis': {
            'min': 0,
            'title': {
                'text': 'Score',
                'align': 'high'
            },
            'labels': {
                'overflow': 'justify'
            }
        },
        'series': [
            {
                'name': 'Jailbreak Impact Score',
                'data': scores_df['Jailbreak Impact Score'].tolist(),
                'color': '#FF6347',  # Tomato Red for Jailbreak Impact Score
            },
            {
                'name': 'Adaptability Score',
                'data': scores_df['Adaptability Score'].tolist(),
                'color': '#4682B4',  # Steel Blue for Adaptability Score
            }
        ],
        'tooltip': {
            'shared': True,
            'valueSuffix': ' score'
        }
    }

    # Visualizzare il grafico
    hg.streamlit_highcharts(activity_charts, 400)

    st.markdown("""**6. Matrice di Correlazione tra le Metriche**""")

    # Assumiamo che i dataframe df e df_nojail siano già esistenti e siano stati uniti in df_combined
    # Esempio di combinazione dei dati: uniamo i dataframe df e df_nojail in un unico dataframe (assicurati che abbiano le colonne comuni)
    df_combined = pd.merge(df, df_nojail, on="req_id", how="inner", suffixes=('_jail', '_nojail'))

    # Calcolare le metriche Jailbreak Impact Score e Adaptability Score
    # Jailbreak Impact Score = (Severity_jailbroken - Consistency_jailbroken) - (Severity_nojail - Consistency_nojail)
    df_combined['jailbreak_impact_score'] = (df_combined['severity_jail'] - df_combined['consistency_jail']) - (df_combined['severity_nojail'] - df_combined['consistency_nojail'])

    # Adaptability Score = Style Consistency_jailbroken - Style Consistency_nojail
    df_combined['adaptability_score'] = df_combined['style_consistency_jail'] - df_combined['style_consistency_nojail']

    # Calcoliamo la matrice di correlazione
    correlation_matrix = df_combined[['jailbreak_impact_score', 'adaptability_score', 'severity_jail', 'style_consistency_jail']].corr()

    # Creiamo la heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='crest', fmt='.2f', linewidths=0.5)
    plt.title('Matrice di Correlazione tra le Metriche')
    st.pyplot(plt)