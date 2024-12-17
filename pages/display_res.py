import streamlit as st
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_elements import elements, mui, nivo, dashboard
import streamlit_highcharts as hg




st.subheader("Results")

st.markdown("**Results of the experiments will be displayed here.** \n")
st.markdown("""Questi grafici sono progettati per fornire un'analisi completa e dettagliata delle risposte dei modelli LLM. I grafici evidenziano:  
1. **Performance Generale**: Successo del jailbreaking e presenza di disclaimer.  
2. **Qualità delle Risposte**: Aderenza, consistenza e gravità.  
3. **Confronti e Relazioni**: Differenze tra modelli e correlazioni tra metriche.  

Questa combinazione di visualizzazioni permette di ottenere insight approfonditi sulle prestazioni dei modelli e guidare le decisioni per ulteriori miglioramenti. """)

results_folder = '/home/site/wwwroot/responses/analysis'
#results_folder = 'results/analysis'


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

df = load_json_data(results_folder)
st.markdown(f"**Numero di record: {len(df)}**")
st.dataframe(df, width=1000, height=500)


with elements("activity_charts"): 
    st.markdown("""**0. Activity Monitor**
- Questo grafico mostra tutte innanzitutto la percentuali di modelli analizzati, in riferimento al totale disponibile sul tool.
- Successivamente, mostra la percentuale di prompt e di richieste evase per ciascun modello.  
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
                            'y': 100}],
                'name': 'Jail_Prompts'},
              { 'data': [ { 'color': 'blue',
                            'innerRadius': '38%',
                            'radius': '62%',
                            'y': 100}],
                'name': 'Requests'}],
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


    st.markdown("""**1. Successo del Jailbreaking**  
    **Descrizione**:  
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
            #'y': int(success_counts[success_counts['jailbreak_success'] == True]['count']),
            'y': int(success_counts[success_counts['jailbreak_success'] == True]['count'].iloc[0]),
            'drilldown': 'success_details'
        },
        {
            'name': 'Failure',
            #'y': int(success_counts[success_counts['jailbreak_success'] == False]['count']),
            'y': int(success_counts[success_counts['jailbreak_success'] == False]['count'].iloc[0]),
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

with elements("chart_jailbreak"):
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
                'minSize': '20%',
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
    hg.streamlit_highcharts(chartDef, 640)


with elements("chart_style"):
    
    # Grafico 2: Distribuzione Aderenza allo Stile
    st.markdown("""**2. Distribuzione Aderenza allo Stile**  
    **Descrizione**:  
    -Un grafico che rappresenta la distribuzione dei punteggi assegnati all'aderenza allo stile richiesto dai prompt.  
    -Utilizza un istogramma arricchito con la densità (KDE) per visualizzare la forma della distribuzione.                      
    **Motivazione**:  
    L'aderenza allo stile è una metrica importante per valutare se il modello segue le istruzioni stilistiche fornite nei prompt di jailbreak. Una distribuzione ben definita può indicare coerenza nelle risposte.                
    **Cosa Mostra**:  
    -La frequenza dei punteggi su una scala da 1 a 5.  
    -La tendenza del modello a rispettare o meno lo stile richiesto.
    """)

     # Creazione di intervalli per la distribuzione
    df["consistency_range"] = pd.cut(
        df["style_consistency"], bins=[0, 2, 4, 5], labels=["1-2", "3-4", "5"]
    )

    # Dati per il grafico a barre (media di style_consistency per modello)
    bar_data = df.groupby("model_name")["style_consistency"].mean().reset_index()
    categories = bar_data["model_name"].tolist()
    bar_values = bar_data["style_consistency"].tolist()

    # Dati per il grafico a torta (distribuzione degli intervalli)
    pie_data = (
        df["consistency_range"]
        .value_counts()
        .sort_index()
        .reset_index()
        .rename(columns={"index": "range", "consistency_range": "count"})
    )
    pie_values = [{"name": row["range"], "y": row["count"]} for _, row in pie_data.iterrows()]

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
            'categories': df_grouped['jail_prompt_id'].unique().tolist(),  # Usato per le etichette dell'asse X
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
    hg.streamlit_highcharts(chartDef, 550)          

# consistency 

with elements("chart_consistency"):
    st.markdown("""**3. Distribuzione Consistenza (Istogramma con KDE)**  
**Descrizione**:  
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

    # Dati per il grafico a barre (media di style_consistency per modello)
    bar_data = df.groupby("model_name")["consistency"].mean().reset_index()
    categories = bar_data["model_name"].tolist()
    bar_values = bar_data["consistency"].tolist()

    # Dati per il grafico a torta (distribuzione degli intervalli)
    pie_data = (
        df["consistency_range"]
        .value_counts()
        .sort_index()
        .reset_index()
        .rename(columns={"index": "range", "consistency_range": "count"})
    )
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
            'categories': df_grouped['jail_prompt_id'].unique().tolist(),  # Usato per le etichette dell'asse X
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
    hg.streamlit_highcharts(chartDef, 550) 

with elements("chart_severity"):
  st.markdown("""**4. Distribuzione Gravità della Risposta**  
  **Descrizione**:  
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
            'height': '80%',
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
    hg.streamlit_highcharts(chartDef, 640)
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
            'height': '60%',
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
    hg.streamlit_highcharts(chartDef, 640)


with elements("chart_disclaimer"):
    st.markdown("""**5. Presenza di Disclaimer per Modello**  
              **Descrizione**:  
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
  st.markdown("""**6. Distribuzione del Successo del Jailbreaking per Modello**  
  **Descrizione**:  
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
    st.markdown("""**7. Matrice di Correlazione tra le Metriche**  
                **Descrizione**:  
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
    
      st.markdown("""**8. Boxplot Comparativo delle Metriche per Modello**  
    **Descrizione**:  
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