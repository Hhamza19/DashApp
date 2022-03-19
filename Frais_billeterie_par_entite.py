import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.express as px

df_billetterie = pd.read_pickle(r"data/Billetteries.pkl")
# df = df_billetterie.loc[~df_billetterie['Nom & Prénom'].isnull()]
# df['Nom & Prénom'] = 'Nom&Prenom'
# Type de deplacement (Maroc/Etranger)
df_maroc = df_billetterie.loc[df_billetterie['Type voyage'] == 'Maroc']
df_etranger = df_billetterie.loc[df_billetterie['Type voyage'] == 'Etranger']
# Frais de billeterie par Entité
df_mt_maroc = df_maroc.groupby(['BPR'])['Montant Billet'].sum().reset_index(name='MT Maroc')
df_mt_etranger = df_etranger.groupby(['BPR'])['Montant Billet'].sum().reset_index(name='MT Etranger')
df_mt_maroc['MT Maroc'] = df_mt_maroc['MT Maroc'].apply(lambda e: (e / 1000.0)).round(3)
df_mt_etranger['MT Etranger'] = df_mt_etranger['MT Etranger'].apply(lambda e: (e / 1000.0)).round(1)

# Outer join de df_mt_etranger et df_mt_maroc
df_etr_mar = pd.merge(df_mt_etranger, df_mt_maroc, on='BPR', how='outer')

# Remplacer les valeur Null par 0
df_etr_mar['MT Etranger'].fillna(0.0, inplace=True)
df_etr_mar['MT Maroc'].fillna(0.0, inplace=True)

df_etr_mar['Total'] = df_etr_mar['MT Maroc'] + df_etr_mar['MT Etranger']
df_etr_mar = df_etr_mar.sort_values(by=['Total'], ascending=True)
df_etr_mar = df_etr_mar[np.isin(df_etr_mar['BPR'],['PBDC','CHAABI BANK','DGRG'],invert=True)]
# print(df['MT Maroc'].isnull())
# # Visualisation
# title = "Montant billeterie par DG/Pôle en KDH  (2019)"
fig7 = px.bar(df_etr_mar,x='Total',y='BPR',orientation='h',labels={'BPR':'','Total':''},text_auto=True,
              title="Répartition des frais de billetterie par entité (KDh)")
fig7.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig7.update_traces(marker_color='rgb(204, 137, 4)')
# fig2.show()
# print()