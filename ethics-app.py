import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv("ethics.csv")
df.sort_values('Panel', inplace=True)

dfa = pd.read_csv("ethics.csv")
dfa.sort_values('Approved-M', inplace=True)

dfb = pd.read_csv("ethics.csv")
dfb.sort_values(['Year', 'Panel'], inplace=True)

dfc = pd.read_csv('ethics-totals.csv')

available_indicators = dfc['Indicator'].unique()

app = dash.Dash(__name__, prevent_initial_callbacks=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=["UG", "PGT", "PGR", "Staff", "Psychology", "Biomed",
               "Healthcare & Food", "Applied Comm. Sci.", "Social", "Natural"],
        customdata=["Undegraduate,", "Postgraduate Taught,", "Postgraduate Research,", "Staff,",
                    "Psychology Sub-Panel,", "Biomedical Sciences Sub-Panel,", "Healthcare & Food Sub-Panel,", "Applied Community Sciences Sub-Panel,",
                    "Social Sub-Panel,", "Natural Sub-Panel,"],
        hovertemplate='%{customdata} number of applications: %{value}<extra></extra>',
        color="lightslategrey"
    ),
    link=dict(
        source=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
                1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3],
        target=[4, 5, 6, 7, 8, 9, 4, 5, 6, 7, 8,
                9, 4, 5, 6, 7, 8, 9, 4, 5, 6, 7, 8, 9],
        value=[329, 409, 431, 71, 931, 603, 146, 78, 182, 82, 121,
               184, 60, 19, 16, 7, 56, 44, 34, 37, 48, 9, 36, 32],
        hovertemplate='Applications of Type %{source.customdata}<br />' +
        'assigned to %{target.customdata} totalling: %{value}<extra></extra>',
        color=[
            '#5ae6ca', '#d8dff1', '#f1d8df', '#ffb347', '#a0b1dd', '#1e2c52',
            '#5ae6ca', '#d8dff1', '#f1d8df', '#ffb347', '#a0b1dd', '#1e2c52',
            '#5ae6ca', '#d8dff1', '#f1d8df', '#ffb347', '#a0b1dd', '#1e2c52',
            '#5ae6ca', '#d8dff1', '#f1d8df', '#ffb347', '#a0b1dd', '#1e2c52']
    ))])


fig.update_layout(title_text="Flow of application types. Hover over nodes and links for more information",
                  font_size=8)

fig2 = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=["UG sign-off", "PGT sign-off", "Panel-assessed", "Psychology",
               "Biomed", "Healthcare & Food", "Applied Comm. Sci.", "Social", "Natural"],
        customdata=["Undegraduate sign-off,", "Postgraduate Taught sign-off,", "Panel-assessed,",
                    "Psychology Sub-Panel,", "Biomedical Sciences Sub-Panel,", "Healthcare & Food Sub-Panel,", "Applied Community Sciences Sub-Panel,",
                    "Social Sub-Panel,", "Natural Sub-Panel,"],
        hovertemplate='%{customdata} number of applications: %{value}<extra></extra>',
        color="grey"
    ),
    link=dict(
        source=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
        target=[3, 4, 5, 6, 7, 8, 3, 4, 5, 6, 7, 8, 3, 4, 5, 6, 7, 8],
        value=[0, 239, 323, 67, 902, 590, 3, 59, 113,
               62, 104, 153, 564, 230, 240, 33, 137, 135],
        hovertemplate='Approval Type %{source.customdata}<br />' +
        'assigned to %{target.customdata} totalling: %{value}<extra></extra>',
        color=[
            '#5ae6ca', '#d8dff1', '#f1d8df', '#ffb347', '#a0b1dd', '#1e2c52',
            '#5ae6ca', '#d8dff1', '#f1d8df', '#ffb347', '#a0b1dd', '#1e2c52',
            '#5ae6ca', '#d8dff1', '#f1d8df', '#ffb347', '#a0b1dd', '#1e2c52']
    ))])


fig2.update_layout(title_text="Flow of approval types. Hover over nodes and links for more information",
                   font_size=8)

fig3 = px.histogram(df, y="Panel",
                    color="Approval Type-P",
                    color_discrete_sequence=[
                        '#5ae6ca', '#d8dff1', '#f1d8df', '#ffb347', '#a0b1dd', '#1e2c52'],
                    barmode="stack",
                    labels={"Panel": "", "count": "",
                            "Approval Type-P": "Approved via"},
                    template="simple_white"
                    )

fig3.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
},
    xaxis_title_text='Total number of applications',
    annotations=[
    go.layout.Annotation(
        text='Click on legend once to remove from graph,<br>or double-click to focus on legend',
        align='center',
        showarrow=False,
        xref='paper',
        yref='paper',
        y=1.15,
        x=1,
        bordercolor='gray',
        borderwidth=0.5
    )
])


labels = ["Cardiff Met", "Perrotis College, Greece",
          "Singapore (DIC)", "Singapore (EASB)", "Sri Lank (ICBT)"]

fig4 = make_subplots(rows=1, cols=6, specs=[[{'type': 'domain'}, {'type': 'domain'}, {
                     'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])
fig4.add_trace(go.Pie(labels=labels, values=[1145, 0, 0, 0, 0], marker=dict(colors=['#5ae6ca', '#d8dff1', '#f1d8df', '#ffb347', '#a0b1dd', '#1e2c52']), name="Social"),
               1, 1)
fig4.add_trace(go.Pie(labels=labels, values=[882, 0, 0, 0, 0], marker=dict(colors=['#5ae6ca', '#d8dff1', '#f1d8df', '#ffb347', '#a0b1dd', '#1e2c52']),  name="Natural"),
               1, 2)
fig4.add_trace(go.Pie(labels=labels, values=[418, 0, 0, 13, 141], marker=dict(colors=['#5ae6ca', '#d8dff1', '#f1d8df', '#ffb347', '#a0b1dd', '#1e2c52']),  name="Psych"),
               1, 3)
fig4.add_trace(go.Pie(labels=labels, values=[544, 0, 19, 0, 61], marker=dict(colors=['#5ae6ca', '#d8dff1', '#f1d8df', '#ffb347', '#a0b1dd', '#1e2c52']),  name="BMS"),
               1, 4)
fig4.add_trace(go.Pie(labels=labels, values=[679, 35, 0, 0, 0], marker=dict(colors=['#5ae6ca', '#d8dff1', '#f1d8df', '#ffb347', '#a0b1dd', '#1e2c52']),  name="HCF"),
               1, 5)
fig4.add_trace(go.Pie(labels=labels, values=[170, 0, 19, 0, 0], marker=dict(colors=['#5ae6ca', '#d8dff1', '#f1d8df', '#ffb347', '#a0b1dd', '#1e2c52']),  name="ACS"),
               1, 6)

fig4.update_traces(textposition='inside', hole=.35,
                   hoverinfo="label+percent+name")

fig4.update_layout(
    {
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    },
    title_text="Institution",
    annotations=[dict(text='Social', x=0, y=0.8, font_size=12, showarrow=False),
                 dict(text='Natural', x=(1/6), y=0.8,
                      font_size=12, showarrow=False),
                 dict(text='Psych', x=(1/6)*2.1, y=0.8,
                      font_size=12, showarrow=False),
                 dict(text='BMS', x=(1/6)*3.1, y=0.8,
                      font_size=12, showarrow=False),
                 dict(text='HCF', x=(1/6)*4.2, y=0.8,
                      font_size=12, showarrow=False),
                 dict(text='ACS', x=0.9, y=0.8, font_size=12, showarrow=False)
                 ])

fig5 = px.line(dfa, x="Approved-M", y="Totals", facet_col="Panel-F", hover_name="Approved-M", range_y=[1, 1500], labels={"Totals": "", "Approved-M": "", "Panel-F": ""},
               template="ggplot2"
               )
fig5.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig5.add_annotation(row=1, col=6, x="2020-09", y=758, text="Term", arrowhead=1)
fig5.add_annotation(text='Drag and drop an area to select and zoom into it. Once zoomed, hold down <b>Shift</b> and user your mouse cursor to span through time',
                    align='center',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    y=1.15,
                    x=1,
                    bordercolor='gray',
                    borderwidth=0.5)
fig5.update_traces(line_color='#5ae6ca')

fig6 = px.histogram(dfb, x="Panel", facet_col="AY", facet_col_spacing=0.1, color="Type", template="none",
                    color_discrete_sequence=[
                        '#5ae6ca', '#d8dff1', '#f1d8df', '#ffb347', '#a0b1dd', '#1e2c52'],
                    barmode="stack",
                    labels={"Panel": "", "count": "",
                            "AY": "Academic Year"}
                    )
fig6.update_layout(
    hoverlabel=dict(
        bgcolor="beige",
        font_size=12,
        font_family="Rockwell"
    ),
    hovermode="x unified",
    yaxis_title="",
    margin=dict(b=160)
)
fig6.update_xaxes(tickfont=dict(family='Rockwell', color='gray', size=10))

CMU_LOGO = "https://campaigns.cardiffmet.ac.uk/vod/img/nav/touch/logo.png"

app.layout = html.Div(style={'backgroundColor': 'beige'}, children=[
    dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=CMU_LOGO, height="40px")),
                        dbc.Col(dbc.NavbarBrand(
                            "Cardiff School of Sport and Health Sciences - Ethics 2018 to 2021", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="https://teamsites.cardiffmet.ac.uk/units/ca/cari/SitePages/Ethics.aspx",
            ),
        ],
        color="dark",
        dark=True,
        sticky="top"),
    html.Div([dbc.Row([
        dbc.Card(
            dbc.CardBody(["Welcome to the ", html.Strong(
                "Years in Data"), " for the ethics framework at the CSSHS. Scroll down to explore the different types of data visualisation available, spanning from 2018 to the current year."]),
            className="mb-3", color="info", inverse=True)], justify="center"
    )
    ]),
    html.Div([
        dbc.Row([
             dbc.Card(
                dbc.CardBody(
                    [
                        html.H3("Applications through time",
                                className="card-title"),
                        html.P(
                            [
                                "Since being implemented in 2018, the CSSHS Ethic Framework system has approved a total of ",html.Strong("3,853 applications"),". The School of Sport and Health Sciences Ethics Committee (SSHSEC) delegates first responsibility for assessing applications to 6 sub-panels",
                            ],
                            className="card-text",
                        ),
                        html.P(
                            dcc.Graph(id="graph",
                                      figure=fig3, config={
                                          'displayModeBar': False
                                      })
                        ),
                        html.P(
                            [
                                "A peak in incoming applications during the year can be observed throughout the panels, although the degree to which this happens varies greatly",
                            ],
                            className="card-text"),
                        dcc.Graph(id="graph2",
                                  figure=fig5, config={
                                      'displayModeBar': False
                                  }),
                        html.P(
                            [
                                "When viewed side-by-side, there is a slight deceleration in the volume of submissions for the 2020/21 Academic Year, and that trend is likely to be maintained when the full dataset for 2020/21 is available",
                            ],
                            className="card-text"),
                        dcc.Graph(id="graph3",
                                  figure=fig6, config={
                                      'displayModeBar': False
                                  })
                    ]
                ),
                 className="w-75 mb-3", color="secondary", outline=True
                )
             ], justify="center")]),
        html.Div([
        dbc.Row([
             dbc.Card(
                dbc.CardBody(
                    [html.H3("Adding context and manipulating the data",
                                className="card-title"),
                        html.P(
                            [
                                "To understand the particularities and submission profiles of each panel and add context and meaning to the figures, ",html.Strong("select two indicators from the dropdown menus below"),". Once selected, 3 figures will be produced: on the left-hand side you will be able to see a comparison for all available panels in relation to the chosen categories, which can be filtered with the Academic Year slider underneath. And by hovering over specific data points, the two figures on the right-hand side will update to show data on the hovered panel for all Academic Years, so that changes are made visible",
                            ],
                            className="card-text",
                        ),
    html.Div([
        html.Div([
            html.H4("Select your X axis"),
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i}
                         for i in available_indicators],
                value='Select your X axis'
            )
        ],
            style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.H4("Select your Y axis"),
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i}
                         for i in available_indicators],
                value='Select your Y axis'
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})],
        style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),
    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            config={
                'displayModeBar': False
            },
            hoverData={'points': [{'customdata': 'Social'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series', config={
            'displayModeBar': False
        }),
        dcc.Graph(id='y-time-series', config={
            'displayModeBar': False
        }),
    ], style={'display': 'inline-block', 'width': '49%'}),
    html.Div([
        dcc.Slider(
        id='crossfilter-AY--slider',
        min=dfc['AY'].min(),
        max=dfc['AY'].max(),
        value=dfc['AY'].max(),
        marks={str(AY): str(AY) for AY in dfc['AY'].unique()},
        step=None
    ),html.P(),
    dbc.Toast(
    [html.P("Please note only applications that have been approved are shown above", className="mb-0")],
    header="Approvals",
)], style={'width': '49%', 'padding': '0px 20px 20px 20px'})]),
                 className="w-75 mb-3", color="warning", outline=True
                )
             ], justify="center")]), 
    html.Div([
        dbc.Row([
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H4("TNE Partners", className="card-title"),
                        html.P(
                            [
                                "CSSHS is partnered with a number of institutions in delivering transnational education. Since 2018, there have been 283 ethics applications from students in TNE",
                            ],
                            className="card-text",
                        ),
                        html.P(
                            dcc.Graph(id="graph1",
                                      figure=fig4, config={
                                          'displayModeBar': False
                                      })
                        ),
                        dbc.Toast(
                            [html.P("As well as the 4 franchises shown above, Cardiff Met is also partnered with City Unity College Greece in Athens. They are in the trial period of a devolved ethics framework and do not send their submissions to our panels", className="mb-0")],
                            header="CUC Athens",
                        )
                    ]
                ),
                className="w-90 mb-4", color="primary", outline=True
            )
        ], justify="center")]),
        html.Div([dbc.Row([
        dbc.Card(
            dbc.CardBody(["Finally, see the two Sankey diagrams below to observe how the flow between types of application and target panel compare with the transformed flow when considering the type of approval sought"]),
            className="mb-3", color="info", inverse=True)], justify="center"
    )
    ]),
    html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Type in relation to Panel"),
                        dbc.CardBody(
                            [
                                dcc.Graph(figure=fig, config={
                                    'displayModeBar': False
                                }),
                            ]
                        ),
                        dbc.CardFooter(
                            "Undergraduate applications are frequently re-routed for self-certification via supervisor sign-off"),
                    ],
                    style={"width": "30rem", "align": "center"}
                ), width="auto"), dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Approval Requirement in relation to Panel"),
                        dbc.CardBody(
                            [
                                dcc.Graph(figure=fig2, config={
                                    'displayModeBar': False
                                }),
                            ]
                        ),
                        dbc.CardFooter(
                            "Considering self-certified applications versus panel-assessed applications, the flow takes on a different shape"),
                    ],
                    style={"width": "30rem", "align": "center"}
                ), width="auto")], justify="center")
    ], style={'textAlign': 'center'}),html.Div(dbc.Row())
])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-AY--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 AY_value):
    dff = dfc[dfc['AY'] == AY_value]

    fig7 = px.scatter(x=dff[dff['Indicator'] == xaxis_column_name]['Value'],
                      y=dff[dff['Indicator'] == yaxis_column_name]['Value'],
                      hover_name=dff[dff['Indicator'] == yaxis_column_name]['Panel'], size=dff[dff['Indicator']
                                                                                               == yaxis_column_name]['Value'], template='ggplot2'
                      )

    fig7.update_traces(
        customdata=dff[dff['Indicator'] == yaxis_column_name]['Panel'])

    fig7.update_xaxes(title=xaxis_column_name, type='linear', showspikes=True)

    fig7.update_yaxes(title=yaxis_column_name, type='linear', showspikes=True)

    fig7.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0})
    fig7.update_layout(
        hoverlabel=dict(
            bgcolor="beige",
            font_size=12,
            font_family="Rockwell"
        ),
        hovermode="x unified",
        margin=dict(b=160)
    )

    return fig7


def create_time_series(dff, title):

    fig7 = px.scatter(dff, x='AY', y='Value',
                      labels={"Value": "",
                              "AY": "Academic Years"}, template='ggplot2')

    fig7.update_traces(mode='lines+markers')

    fig7.update_xaxes(showgrid=False, type='category')

    fig7.update_yaxes(type='linear')

    fig7.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                        xref='paper', yref='paper', showarrow=False, align='left',
                        bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    fig7.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig7


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name):
    country_name = hoverData['points'][0]['customdata']
    dff = dfc[dfc['Panel'] == country_name]
    dff = dff[dff['Indicator'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name):
    dff = dfc[dfc['Panel'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator'] == yaxis_column_name]
    return create_time_series(dff, yaxis_column_name)


if __name__ == '__main__':
    app.run_server(debug=False)
