import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.express as px

df_dotation = pd.read_pickle(r"data/Dotations.pkl")


# Répartition des Doatations par Type de deplacement (Mission/Formation)
df_dot_for_mis = df_dotation.groupby(['Objet'])['Montant Dotations'].sum().reset_index(name='Dotation')
df_dot_for_mis['Dotation'] = df_dot_for_mis['Dotation'].apply(lambda e: (e / 1000.0)).round(3)
# Remplacer les valeur Null par 0
df_dot_for_mis.fillna(0.0, inplace=True)
# Pie chart Doatations par type (Formation/mission)
fig3 = px.pie(df_dot_for_mis,values='Dotation',names='Objet',color='Objet',color_discrete_map={'Mission':'#7a7a7a','Formation':'#ed9715'},
              title='Répartition des dotations (Mis./Form.)')
# fig3.show()
# print()

# Répartition des Dotations par BCP/BPR
df_dotation['Affectation'] = np.where(df_dotation['Affectation']!='BCP','BPR','BCP')
df_dot_bcp_bpr = df_dotation.groupby(['Affectation'])['Montant Dotations'].sum().reset_index(name='Dotation')
fig4 = px.pie(df_dot_bcp_bpr,values='Dotation',names='Affectation',color='Affectation',color_discrete_map={'BCP':'#7a7a7a','BPR':'#ed9715'},
              title='Répartition des dotations (BPR/BCP)')
# fig4.show()
# print()
