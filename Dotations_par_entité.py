import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.express as px

df_dotation = pd.read_pickle(r"data/Dotations.pkl")
# df = df_dotation.loc[~df_dotation['Nom & Prénom'].isnull()]
# df['Nom & Prénom'] = 'Nom&Prenom'
# df.to_pickle(r"data/Dotations.pkl")

# Dotations par Entité
df_dot_entite = df_dotation.groupby(['BPR'])['Montant Dotations'].sum().reset_index(name='MT_Dotation')
df_dot_entite['MT_Dotation'] = df_dot_entite['MT_Dotation'].apply(lambda e: (e / 1000.0)).round(3)


# # Outer join de df_mt_dot_formation et df_mt_dot_mission
# df_dot_for_mis = pd.merge(df_mt_dot_formation, df_mt_dot_mission, on='BPR', how='outer')

# Remplacer les valeur Null par 0
df_dot_entite.fillna(0.0, inplace=True)

# Graphe Doatations par Entité
df_dot_entite = df_dot_entite.sort_values(by=['MT_Dotation'], ascending=True)
df_dot_entite = df_dot_entite[np.isin(df_dot_entite['BPR'],['PBDC','CHAABI BANK','DGRG'],invert=True)]
fig5 = px.bar(df_dot_entite, x='MT_Dotation', y='BPR',labels={'MT_Dotation':'','BPR':''}, orientation='h',text_auto=True,title='Répartition des dotations en devise par entité (K€)')
fig5.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig5.update_traces(marker_color='rgb(204, 137, 4)')
# fig5.show()
# print()