import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
dash.register_page(__name__, path="/",name='Frais globaux')
from Repartition_des_deplacements import df_miss_for,fig2
from DéplacementsVSEffectif import df_depVSeff,fig1
from Dotations_par_pays import df_mt_pays
from Reparition_des_dotations import df_dot_for_mis,df_dot_bcp_bpr,fig3,fig4
from Dotations_par_entité import df_dot_entite,fig5
from Frais_billeterie_par_entite import df_etr_mar,fig7
from Repartition_par_trimetre import df_dot_trim,fig8

df_dotation = pd.read_pickle(r"data/Dotations.pkl")
df_billetterie = pd.read_pickle(r"data/Billetteries.pkl")

layout = [
    dbc.Row(
        dbc.Col(html.H2("Analyse des frais liés aux déplacements à l’étranger"),className='text-center text-primary m-4',width=12)
    ),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H5("Nombre de déplacements", className="card-title text-center"),
                            html.P(len(df_billetterie),className="text-center fs-5 text"),
                        ]
                    ),
                ],
                style={"width": "18rem", "background-color": "#f8f9fa", "height": "6rem"},
            ),width={'size':3}
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H5("Dotations en devise (K€)", className="card-title text-center"),
                            html.P(round(df_dot_entite['MT_Dotation'].sum(),0), className="text-center fs-5 text"),
                        ]
                    ),
                ],
                style={"width": "18rem", "background-color": "#f8f9fa", "height": "6rem"},
            ), width={'size': 3}
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H5("Frais de billetterie (KDH)", className="card-title text-center"),
                            html.P(round(df_etr_mar['Total'].sum(),0), className="text-center fs-5 text"),
                        ]
                    ),
                ],
                style={"width": "18rem", "background-color": "#f8f9fa", "height": "6rem"},
            ), width={'size': 3}
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H5("Budget global (KDH)", className="card-title text-center"),
                            html.P(round(df_dot_entite['MT_Dotation'].sum()*10+df_etr_mar['Total'].sum(),0), className="text-center fs-5 text"),
                        ]
                    ),
                ],
                style={"width": "18rem", "background-color": "#f8f9fa", "height": "6rem"},
            ), width={'size': 3}
        )
    ],justify="between"),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='graph_rep_dep',figure=fig2)
        ,width={'size':5}),
        dbc.Col(
            dcc.Graph(id='graph_depVSeff',figure=fig1)
        ,width={'size':5})
    ],className="g-0",justify="between"),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='graph_rep_dot_bcp_bpr',figure=fig4)
        ,width={'size':5}),
        dbc.Col(
            dcc.Graph(id='graph_dot_entite',figure=fig5)
        ,width={'size':5,'order':'first'})
    ],className="g-0",justify="between"),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='slct_pays',
                         options=[
                             {"label": e, "value": e} for e in df_dotation['Pays 1'].unique()
                         ],
                         multi=True,
                         value=df_dotation['Pays 1'].unique()[20:]
                         ),
            dcc.Graph(id='graph_dot_pays_0', figure={})
        ], width={'size': 5}),
        dbc.Col(
            dcc.Graph(id='graph_rep_dot_miss_for',figure=fig3)
        ,width={'size':5}),
    ],justify='between'),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='graph_frais_bill', figure=fig7), width={'size': 6}
        ),
        dbc.Col(
            dcc.Graph(id='graph_dot_trim', figure=fig8), width={'size':6}
        )
    ], className="g-0", justify="between")
]

@callback(
    Output(component_id='graph_dot_pays_0',component_property='figure'),
    Input(component_id='slct_pays',component_property='value')
)
def update_graph(pays_slctd) :
    dff_dot = df_dotation.copy()
    df_mt_pays = dff_dot.groupby(['Pays 1'])['MT_Dotation_Final'].sum().reset_index(name='Montant Dotation')
    df_mt_pays.sort_values(by=['Montant Dotation'], inplace=True)
    df_mt_pays['Montant Dotation'] = df_mt_pays['Montant Dotation'].apply(lambda x: x / 1000).round(3)
    dff = df_mt_pays.copy()
    # dff = dff[np.isin(dff['Pays 1'], pays_slctd)]
    dff = dff[dff['Pays 1'].isin(pays_slctd)]

    fig = px.bar(dff, x='Montant Dotation', y='Pays 1', labels={'Pays 1': '','Montant Dotation':''},
                 title='Dotations par pays',orientation='h')
    fig.update_traces(marker_color='rgb(204, 137, 4)')

    return fig