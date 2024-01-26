import streamlit as st
import plotly.express as px 

#--------------------------
import pandas as pd

hapvida=pd.read_csv('RECLAMEAQUI_HAPVIDA.csv', sep=',')
ibyte=pd.read_csv('RECLAMEAQUI_IBYTE.csv', sep=',')
nagem=pd.read_csv('RECLAMEAQUI_NAGEM.csv', sep=',')

hapvida['empresa'] = 'Hapvida'
ibyte['empresa'] = 'Ibyte'
nagem['empresa'] = 'Nagem'

# unindo os dataframes
df = pd.concat([hapvida, ibyte, nagem])

# converte a coluna 'TEMPO' para datetime
df['TEMPO'] = pd.to_datetime(df['TEMPO'])

# cria uma coluna de estados 'UF'
df['UF'] = df['LOCAL'].str.extract(r'([A-Z]{2})')

empresas = ['Hapvida', 'Ibyte', 'Nagem']
ufs = df['UF'].unique()
status = df['STATUS'].unique()
total_reclamacoes=df['ID'].count()
#--------------------------


st.title("Reclamações")

empresas_select = st.sidebar.selectbox('Selecione a empresa', empresas)
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

serie_temporal = df.groupby([df['TEMPO'], 'empresa']).size().reset_index(name='reclamacoes')
print(serie_temporal)

plt.figure(figsize=(15, 8))
sns.lineplot(data=serie_temporal, x='TEMPO', y='reclamacoes', hue='empresa')
plt.xticks(rotation=45)
plt.title('Histograma de Reclamações por Empresa e Data')
plt.xlabel('Data')
plt.ylabel('Reclamações')
plt.show()
#--------------------------


df_time = df.groupby(['empresa', 'TEMPO']).size().reset_index(name='reclamacoes')
fig = px.line(df_time, x='TEMPO', y='reclamacoes', color='empresa', title='Reclamações por empresa')
st.plotly_chart(fig)

df_uf = df.groupby(['UF', 'STATUS']).size().reset_index(name='reclamacoes')
fig = px.bar(df_uf, x='UF', y='reclamacoes', color='STATUS', title='Reclamações por estado e status')
st.plotly_chart(fig)

fig = px.histogram(df, x='empresa', title='Distribuição do número de palavras na descrição')
st.plotly_chart(fig)
