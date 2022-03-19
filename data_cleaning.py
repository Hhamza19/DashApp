import pandas as pd
import numpy as np
import os

# pwd = os.getcwd()  # present working directory
df_billetterie = pd.read_excel(r"data/CanevasDotations+Billeterie Benjelloun.xlsx", sheet_name="Billetterie", header=9)
df_dotations = pd.read_excel(r"data/CanevasDotations+Billeterie Benjelloun.xlsx",sheet_name="Dotations en devise",header=10)

df = df_billetterie
# df = df_dotations
df.loc[~df['Nom & Prénom'].isnull(),'Nom & Prénom'] = 'Nom&Prenom'

df['Nom & Prénom'].fillna(0.0,inplace=True)
df = df.loc[np.where(df['Nom & Prénom'] != 0.0)]
# df['Restitution/Complément'].fillna(0.0,inplace=True) # pour la dataframe df_dotations
# df['Montant Dotations'].fillna(0.0,inplace=True) # pour la dataframe df_dotations
df['Affectation'] = np.where((df['Banque']!='BCP')&(df['Banque']!='BDC'),'BPRs',df['Banque'])
# df['MT_Dotation_Final'] = df['Montant Dotations'] + df['Restitution/Complément'] # pour la dataframe df_dotations
df['BPR'] = np.where(df['Affectation'] == 'BCP',df['DG/Pôle'],df['Affectation'])
for pole in set(df['DG/Pôle']):
    df.loc[df['DG/Pôle'] == pole,'Nombre de déplacements'] = len(df.loc[df['DG/Pôle']==pole])
df['Trimestre'] = np.where(df['mois'].isin([1,2,3]),'T1',
                           np.where(df['mois'].isin([4,5,6]),'T2',
                                    np.where(df['mois'].isin([7,8,9]),'T3','T4')))

df.to_pickle(r"data/Billetteries.pkl")
df.to_excel(r"data/Billetteries.xlsx",index=False)
# df.to_pickle(r"data/Dotations.pkl")
# df.to_excel(r"data/Dotations.xlsx",index=False)
print()
