import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from scipy.stats import dirichlet
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Required by Render

def create_dirichlet_plot(alpha, title=""):
    samples = dirichlet.rvs(alpha, size=1000)
    df = pd.DataFrame(samples, columns=["X1", "X2", "X3"])
    fig = px.scatter_ternary(
        df, a="X1", b="X2", c="X3",
        color_discrete_sequence=["blue"],
        opacity=0.6,
        hover_data={"X1": ":.3f", "X2": ":.3f", "X3": ":.3f"},
        title=title
    )
    fig.update_traces(marker=dict(size=5))
    return fig, df

app.layout = dbc.Container([
    html.H2("Dirichlet Distribution Visualizer"),
    html.Label("Alpha values (α1, α2, α3):"),
    dbc.Row([
        dbc.Col(dcc.Slider(0.1, 10, 0.1, value=2, id='alpha1'), width=4),
        dbc.Col(dcc.Slider(0.1, 10, 0.1, value=5, id='alpha2'), width=4),
        dbc.Col(dcc.Slider(0.1, 10, 0.1, value=3, id='alpha3'), width=4),
    ]),
    dcc.Graph(id='dirichlet-plot'),
    html.Pre(id="stats"),
    html.A("⬇ Download CSV", id="csv-link", href="", download="samples.csv", style={"marginRight": "20px"}),
    html.A("⬇ Download Plot (HTML)", id="html-link", href="", download="plot.html")
], fluid=True)

@app.callback(
    Output('dirichlet-plot', 'figure'),
    Output('csv-link', 'href'),
    Output('html-link', 'href'),
    Output('stats', 'children'),
    Input('alpha1', 'value'),
    Input('alpha2', 'value'),
    Input('alpha3', 'value'),
)
def update_plot(a1, a2, a3):
    alpha = [a1, a2, a3]
    fig, df = create_dirichlet_plot(alpha, title=f"α = {alpha}")
    df.to_csv("samples.csv", index=False)
    fig.write_html("plot.html")

    csv_href = "data:text/csv;charset=utf-8," + df.to_csv(index=False)
    html_href = "data:text/html;charset=utf-8," + open("plot.html", "r").read()

    stats = df.describe().loc[["mean", "std"]].round(3).to_string()
    return fig, csv_href, html_href, stats

if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8080)
