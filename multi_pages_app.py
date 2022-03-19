import dash
import dash_labs as dl
import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State

app = dash.Dash(
    __name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# for x in dash.page_registry.values():
#     print(x)

pages = list(dash.page_registry.values())

sidebar = dbc.Card([
    dbc.CardBody([
        html.H4("Type de frais", className="text-center fs-5 text"),
        html.Hr(),
        dbc.Nav(
            # dbc.ListGroup(
            #     [
            #         dbc.ListGroupItem(page["name"], href=page["path"])
            #         for page in dash.page_registry.values()
            #         if page["module"] != "pages.not_found_404"
            #     ]
            # ),
            # [
            #     dbc.NavLink(pages[1]["name"], href=pages[1]["path"], active="exact", className='text-center'),
            #     dbc.NavLink(pages[0]["name"], href=pages[0]["path"], active="exact", className='text-center'),
            # ],
            [
                dbc.NavLink(page["name"], href=page["path"], active="exact",className='text-center fs-6 text')
                for page in dash.page_registry.values() if page["module"] != "pages.not_found_404"
            ],
            vertical=True,
            pills=True,
        ),
    ])
],style=SIDEBAR_STYLE,)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(sidebar, width=1),
        dbc.Col(dl.plugins.page_container, width=10)
    ], justify='between')
],fluid=True,)


if __name__ == "__main__" :
    app.run_server(debug=True)
