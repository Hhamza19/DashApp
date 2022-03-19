import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.express as px

df_billetterie = pd.read_pickle(r"data/Billetteries.pkl")

# Type de deplacement (Mission/Formation)
df_mission = df_billetterie.loc[df_billetterie['Objet'] == 'Mission']
df_formation = df_billetterie.loc[df_billetterie['Objet'] == 'Formation']

#Nombre de déplacements par type (Mission/Formation)
df_miss_for = df_billetterie.groupby(['Objet'])['Nom & Prénom'].count().reset_index(name='Nombre de déplacements')
df_miss_for.rename(columns={'Objet':'Type de déplacement'},inplace=True)
fig2 = px.pie(df_miss_for, values='Nombre de déplacements', names='Type de déplacement',color='Type de déplacement',color_discrete_map={'Mission':'#7a7a7a','Formation':'#ed9715'},
              title="Répartition des déplacements à l’étranger")
# print()