import dash
dash.register_page(__name__,path="/billeteries",name='Frais de billeteries')
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np # pip install numpy
import pandas as pd

df_billetteries = pd.read_pickle(r"data/Billetteries.pkl")


entite = ['BI','PMPM', 'Projet ABI', 'INSP. GEN', 'PRESIDENCE DG', 'CABINET & COMM', 'PDCH', 'DGBD', 'DGBCP', 'PFSP', 'PRG']

np.random.seed(2020)

layout = html.Div(
    [
        dcc.Graph(id="histograms-graph"),
        html.P("Mean:"),
        dcc.Slider(
            id="histograms-mean", min=-3, max=3, value=0, marks={-3: "-3", 3: "3"}
        ),
        html.P("Standard Deviation:"),
        dcc.Slider(id="histograms-std", min=1, max=3, value=1, marks={1: "1", 3: "3"}),
    ]
)

layout = [
        dbc.Row([
           dbc.Col(
               html.Div(html.H4("Frais de billetteries")), width=12,className='m-4 text-center'
           )
        ],justify='start'),
        dbc.Row([
            dbc.Col(html.Div([html.Span([dbc.Label("Entité (DG/Pôle)")], className="fw-bold"),
                          dcc.Dropdown(id='selct_entite_bill',
                                       options=[{'label': e, 'value': e} for e in entite],
                                       multi=False,
                                       value='BI'
                                       ),
                          ], ), width={'size': 3}
                )
    ], className="g-0 m-4"),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='graph_bill_trim',figure={}),width=5
        ),
        dbc.Col(
            dcc.Graph(id='graph_bill_dep',figure={}),width=5
        )
    ],justify='between')
]


@callback(
    Output(component_id='graph_bill_trim', component_property='figure'),
    Output(component_id='graph_bill_dep', component_property='figure'),
    Input(component_id='selct_entite_bill',component_property='value')
)
def updateGraph(entite) :
    # Billeteries
    dff_bill = df_billetteries.copy()
    dff_bill = dff_bill[dff_bill['DG/Pôle'] == entite]

    # Billetrie par trimestre
    df_bill_trim = dff_bill.groupby(['Trimestre'])['Montant Billet'].sum().reset_index(name='Montant Billet')
    df_bill_trim['Montant Billet'] = df_bill_trim['Montant Billet'].apply(lambda e: (e / 1000)).round(1)
    fig1 = px.bar(df_bill_trim, x='Trimestre', y='Montant Billet', text='Montant Billet', title='Répartition par trimestre (KDh)')
    fig1.update_traces(marker_color='rgb(204, 137, 4)')

    # Nombre de déplacement par type (Miss./Form.)
    df_bill_dep = dff_bill.groupby(['Objet'])['Nom & Prénom'].count().reset_index(name='Nombre deplacement')
    fig2 = px.pie(df_bill_dep,values='Nombre deplacement',names='Objet',color='Objet',color_discrete_map={'Mission':'#7a7a7a','Formation':'#ed9715'},
                  title="Répartition des déplacements à l’étranger")
    fig2.update_traces(textinfo='value',textfont_size=10)

    return fig1,fig2
