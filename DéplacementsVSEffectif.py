import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.express as px


df_billetterie = pd.read_pickle(r"data/Billetteries.pkl")

# Deplacement vs Effectif pour chaque entité
df_BCP = df_billetterie.loc[df_billetterie['Banque']=='BCP']
df_effectif = pd.read_excel(r"data/CanevasDotations+Billeterie Benjelloun.xlsx", sheet_name="Effectif")
df_BCP = pd.merge(df_BCP, df_effectif,left_on='DG/Pôle',right_on='Code',how='left')
df_depVSeff = df_BCP.groupby(['DG/Pôle', 'Nombre de déplacements', 'Effectif'], dropna=False).size().reset_index(name="count")
df_depVSeff = df_depVSeff.loc[df_depVSeff['Effectif'].notnull()]
df_depVSeff['Déplacements vs Effectif'] = (df_depVSeff['Nombre de déplacements'] / df_depVSeff['Effectif']).round(2)
df_depVSeff.drop('count',axis='columns',inplace=True)
df_depVSeff = df_depVSeff[df_depVSeff['DG/Pôle']!='PRESIDENCE DG']
df_depVSeff.sort_values(by='Déplacements vs Effectif',ascending=False,inplace=True)
fig1 = px.line(df_depVSeff, x='DG/Pôle', y='Déplacements vs Effectif',markers=True,labels={'DG/Pôle':'','Déplacements vs Effectif':''},text='Déplacements vs Effectif',title="Nb déplacements vs Effectif par entité")
fig1.update_traces(textposition="top center")
# print()

