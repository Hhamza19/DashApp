import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.express as px

df_dotation = pd.read_pickle(r"data/Dotations.pkl")
df_billetrie = pd.read_pickle(r"data/Billetteries.pkl")
df = df_dotation
df_dot_trim = df.groupby(['Trimestre'])['Montant Dotations'].sum().reset_index(name='Dotation')
df_dot_trim['Dotation'] = df_dot_trim['Dotation'].apply(lambda e: (e / 1000.0)).round(1)

fig8 = px.line_polar(df_dot_trim ,r='Dotation', theta='Trimestre', line_close=True,markers=True,text='Dotation',
                     title="Répartition des dotations par trimestre (K€)")
fig8.update_traces(textposition='top center',fill='toself')
#print()
# fig.show()
#Repartition des dotations par Trimestre
