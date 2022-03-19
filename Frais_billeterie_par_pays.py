import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.express as px

df_billetterie = pd.read_pickle(r"data/Billetteries.pkl")

# Regroupement des frais de billeterie par Pays
df_mt_pays = df_billetterie.groupby(['Pays 1'])['Montant Billet'].sum().reset_index(name='Montant Billeterie')
df_mt_pays.sort_values(by=['Montant Billeterie'],inplace=True)
df_mt_pays['Montant Billeterie'] = df_mt_pays['Montant Billeterie'].apply(lambda x:x/1000).round(3)
fig = px.bar(df_mt_pays, x='Montant Billeterie', y='Pays 1',labels={'Pays 1':'Pays'}, title='Frais de billetrie par pays',orientation='h')
# fig.update_traces(marker_color='rgb(204, 137, 4)')
# fig.show()
# print()