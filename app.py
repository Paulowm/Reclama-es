import streamlit as st
import plotly.express as px 

#--------------------------
import pandas as pd

HAPVIDA=pd.read_csv('RECLAMEAQUI_HAPVIDA.csv', sep=',')
IBYTE=pd.read_csv('RECLAMEAQUI_IBYTE.csv', sep=',')
NAGEM=pd.read_csv('RECLAMEAQUI_NAGEM.csv', sep=',')

HAPVIDA['Empresa'] = 'Hapvida'
IBYTE['Empresa'] = 'Ibyte'
NAGEM['Empresa'] = 'Nagem'

# unindo os dataframes
df = pd.concat([HAPVIDA, IBYTE, NAGEM])

# converte a coluna 'TEMPO' para datetime
df['TEMPO'] = pd.to_datetime(df['TEMPO'])

# cria uma coluna de estados 'UF'
df['UF'] = df['LOCAL'].str.extract(r'([A-Z]{2})')

empresas = ['Hapvida', 'Ibyte', 'Nagem']
ufs = df['UF'].unique()
status = df['STATUS'].unique()
total_reclamacoes=df['ID'].count()
#--------------------------


st.title("Reclame Aqui - HAPVIDA IBYTE NAGEM")

empresas_select = st.sidebar.selectbox('Selecione a Empresa', empresas)
uf_select = st.sidebar.selectbox('Selecione o estado', ufs)
status_select = st.sidebar.selectbox('Selecione o status', status)
qtd_palavras_select = st.sidebar.slider(
    'Selecione a quantidade de palavras na descrição',
    min_value=0,
    max_value=20,
    value=(0, 20))
st.metric(label="Total Reclamações", value=total_reclamacoes)
#--------------------------

import matplotlib.pyplot as plt
import seaborn as sns

serie_temporal = df.groupby([df['TEMPO'], 'Empresa']).size().reset_index(name='reclamacoes')
print(serie_temporal)

plt.figure(figsize=(15, 8))
sns.lineplot(data=serie_temporal, x='TEMPO', y='reclamacoes', hue='Empresa')
plt.xticks(rotation=45)
plt.title('Histograma de Reclamações por Empresa e Data')
plt.xlabel('Data')
plt.ylabel('Reclamações')
plt.show()
#--------------------------


df_time = df.groupby(['Empresa', 'TEMPO']).size().reset_index(name='reclamacoes')
fig = px.line(df_time, x='TEMPO', y='reclamacoes', color='Empresa', title='Reclamações por Empresa')
st.plotly_chart(fig)

df_uf = df.groupby(['UF', 'STATUS']).size().reset_index(name='reclamacoes')
fig = px.bar(df_uf, x='UF', y='reclamacoes', color='STATUS', title='Reclamações por estado e status')
st.plotly_chart(fig)

fig = px.histogram(df, x='Empresa', title='Distribuição do número de palavras na descrição')
st.plotly_chart(fig)
