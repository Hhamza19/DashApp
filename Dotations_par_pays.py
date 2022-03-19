import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.express as px


df_dotation = pd.read_pickle(r"data/Dotations.pkl")

# Repartitions des Dotations par Pays
df_mt_pays = df_dotation.groupby(['Pays 1'])['MT_Dotation_Final'].sum().reset_index(name='Montant Dotation')
df_mt_pays.sort_values(by=['Montant Dotation'],inplace=True)
df_mt_pays['Montant Dotation'] = df_mt_pays['Montant Dotation'].apply(lambda x:x/1000).round(3)
# fig = px.bar(df_mt_pays, x='Montant Dotation', y='Pays 1',labels={'Pays 1':'Pays'}, title='Dotations par pays',orientation='h')
# fig.update_traces(marker_color='rgb(204, 137, 4)')
# fig.show()
# print()