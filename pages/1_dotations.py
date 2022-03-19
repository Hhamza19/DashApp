import dash
import pandas as pd
dash.register_page(__name__,path="/dotations",name='Frais de dotations')
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc

df_dotation = pd.read_pickle(r"data/Dotations.pkl")
entite = ['BI','PMPM', 'Projet ABI', 'INSP. GEN', 'PRESIDENCE DG', 'CABINET & COMM', 'PDCH', 'DGBD', 'DGBCP', 'PFSP', 'PRG']

layout = [
    dbc.Row(
        dbc.Col(html.H2('Frais liés aux déplacements à l’étranger'),width=12,className='text-center text-primary m-4')
    ),
    dbc.Row([
       dbc.Col(
           html.Div(html.H4("Dotations en devise")), width=12,className='text-center'
       )
    ],justify='start'),
    dbc.Row([
        dbc.Col(html.Div([html.Span([dbc.Label("Entité (DG/Pôle)")],className="fw-bold"),
                dcc.Dropdown(id='selct_entite_dot',
                         options=[{'label': e, 'value': e} for e in entite],
                         multi=False,
                         value='BI'
                ),
        ],),width={'size':3}
        )
    ],className="g-0 m-4"),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='graph_dot_mis_for',figure={}),width={'size':5}
        ),
        dbc.Col(
            dcc.Graph(id='graph_dot_trim',figure={}),width={'size':5}
        )
    ],justify='between'),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='graph_dot_cr',figure={}),width={'size':6}
        ),
        dbc.Col(
            dcc.Graph(id='graph_dot_pays',figure={}),width={'size':5}
        )
    ],justify='between'),
]


@callback(
    Output(component_id='graph_dot_mis_for',component_property='figure'),
    Output(component_id='graph_dot_trim',component_property='figure'),
    Output(component_id='graph_dot_cr',component_property='figure'),
    Output(component_id='graph_dot_pays',component_property='figure'),
    Input(component_id='selct_entite_dot',component_property='value')
)
def updategraph(entite) :
    # Dotations
    dff_dot = df_dotation.copy()
    dff_dot = dff_dot[dff_dot['DG/Pôle'] == entite]

    df_dot_mis_for = dff_dot.groupby(['Objet'])['MT_Dotation_Final'].sum().reset_index(name='Dotation')
    df_dot_mis_for['Dotation'] = df_dot_mis_for['Dotation'].apply(lambda e: (e / 1000.0)).round(1)
    fig1 = px.pie(df_dot_mis_for, values='Dotation', names='Objet',color='Objet',color_discrete_map={'Mission':'#7a7a7a','Formation':'#ed9715'},
                  title='Répartition des dotations (Mis./Form.)')
    fig1.update_traces(textinfo='value', textfont_size=10)

    df_dot_trim = dff_dot.groupby(['Trimestre'])['MT_Dotation_Final'].sum().reset_index(name='Dotation')
    df_dot_trim['Dotation'] = df_dot_trim['Dotation'].apply(lambda e: (e / 1000)).round(1)
    fig2 = px.bar(df_dot_trim, x='Trimestre', y='Dotation', text='Dotation',title='Répartition par trimestre (K€)')
    fig2.update_traces(textposition="outside")
    fig2.update_traces(marker_color='rgb(204, 137, 4)')

    df_dot_cr = dff_dot.groupby(['Entité'])['MT_Dotation_Final'].sum().reset_index(name='Dotation')
    fig3 = px.pie(df_dot_cr, values='Dotation', names='Entité',color_discrete_sequence=px.colors.sequential.RdBu ,title="Répartition par centre de responsabilité")

    df_dot_pays = dff_dot.groupby(['Pays 1'])['MT_Dotation_Final'].sum().reset_index(name='Dotation')
    df_dot_pays['Dotation'] = df_dot_pays['Dotation'].apply(lambda e: (e / 1000)).round(1)
    df_dot_pays.sort_values(by=['Dotation'], inplace=True)
    fig4 = px.bar(df_dot_pays, y='Pays 1', x='Dotation', text='Dotation', title='Répartition par pays (K€)',
                  labels={'Pays 1': '', 'Dotation': ''})
    fig4.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False,marker_color='rgb(204, 137, 4)')

    return fig1,fig2,fig3,fig4
