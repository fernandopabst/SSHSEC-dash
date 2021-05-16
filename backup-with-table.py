import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_dangerously_set_inner_html

df = pd.read_csv("ethics.csv")

# Creating an ID column name gives us more interactive capabilities
df['id'] = df['ID']
df.set_index('id', inplace=True, drop=False)


app = dash.Dash(__name__, prevent_initial_callbacks=True,external_stylesheets=[dbc.themes.BOOTSTRAP])

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = ["UG","PGT","PGR","Staff","Psychology","Biomed","Healthcare & Food","Applied Comm. Sci.","Social","Natural"],
      customdata = ["Undegraduate,", "Postgraduate Taught,", "Postgraduate Research,", "Staff,",
                    "Psychology Sub-Panel,", "Biomedical Sciences Sub-Panel,","Healthcare & Food Sub-Panel,","Applied Community Sciences Sub-Panel,",
                    "Social Sub-Panel,","Natural Sub-Panel,"],
      hovertemplate='%{customdata} number of applications: %{value}<extra></extra>',
      color = "lightslategrey"
    ),
    link = dict(
      source = [0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3],
      target = [4,5,6,7,8,9,4,5,6,7,8,9,4,5,6,7,8,9,4,5,6,7,8,9],
      value = [329,409,431,71,931,603,146,78,182,82,121,184,60,19,16,7,56,44,34,37,48,9,36,32],
      hovertemplate='Applications of Type %{source.customdata}<br />'+
        'assigned to %{target.customdata} totalling: %{value}<extra></extra>',
      color = [
'#d8f1ea','#d8dff1','#f1d8df','#f1ead8','#a0b1dd','#1e2c52',
'#d8f1ea','#d8dff1','#f1d8df','#f1ead8','#a0b1dd','#1e2c52',
'#d8f1ea','#d8dff1','#f1d8df','#f1ead8','#a0b1dd','#1e2c52',
'#d8f1ea','#d8dff1','#f1d8df','#f1ead8','#a0b1dd','#1e2c52']
  ))])


fig.update_layout(title_text="Flow of application types. Hover over nodes and links for more information",
                  font_size=8)

fig2 = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = ["UG sign-off","PGT sign-off","Panel-assessed","Psychology","Biomed","Healthcare & Food","Applied Comm. Sci.","Social","Natural"],
      customdata = ["Undegraduate sign-off,", "Postgraduate Taught sign-off,", "Panel-assessed,",
                    "Psychology Sub-Panel,", "Biomedical Sciences Sub-Panel,","Healthcare & Food Sub-Panel,","Applied Community Sciences Sub-Panel,",
                    "Social Sub-Panel,","Natural Sub-Panel,"],
      hovertemplate='%{customdata} number of applications: %{value}<extra></extra>',
      color = "grey"
    ),
    link = dict(
      source = [0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2,2],
      target = [3,4,5,6,7,8,3,4,5,6,7,8,3,4,5,6,7,8],
      value = [0,239,323,67,902,590,3,59,113,62,104,153,564,230,240,33,137,135],
      hovertemplate='Approval Type %{source.customdata}<br />'+
        'assigned to %{target.customdata} totalling: %{value}<extra></extra>',
      color = [
'#d8f1ea','#d8dff1','#f1d8df','#f1ead8','#a0b1dd','#1e2c52',
'#d8f1ea','#d8dff1','#f1d8df','#f1ead8','#a0b1dd','#1e2c52',
'#d8f1ea','#d8dff1','#f1d8df','#f1ead8','#a0b1dd','#1e2c52',
'#d8f1ea','#d8dff1','#f1d8df','#f1ead8','#a0b1dd','#1e2c52']
  ))])


fig2.update_layout(title_text="Flow of approval types. Hover over nodes and links for more information",
                  font_size=8)

CMU_LOGO = "https://campaigns.cardiffmet.ac.uk/vod/img/nav/touch/logo.png"

app.layout = html.Div([
       dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=CMU_LOGO, height="40px")),
                    dbc.Col(dbc.NavbarBrand("Cardiff School of Sport and Health Sciences - Ethics", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://www.cardiffmet.ac.uk/sportandhealthsciences/Pages/default.aspx",
        ),
    ],
    color="dark",
    dark=True,
    sticky="top"
),

    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "hideable": True}
            if i == "id"
            else {"name": i, "id": i}
            for i in df.columns
        ],
        data=df.to_dict('records'),
        filter_action="native",    
        sort_action="native",       
        sort_mode="single",        
        row_deletable=False,      
        selected_columns=[],       
        selected_rows=[],          
        page_action="native",     
        page_current=0,            
        page_size=3,              
        style_cell={              
            'width': 'auto'
        },
        style_data={ 
            'whiteSpace': 'normal',
            'height': 'auto'
        }
    ),

    html.Br(),
    html.Br(),
    html.Div(id='bar-container'),
    html.Div([
        dbc.Row([
            dbc.Col(
        dbc.Card(
    [
        dbc.CardHeader("From when records began to May 2021 - Type to Panel"),
        dbc.CardBody(
            [
    dcc.Graph(figure=fig),
            ]
        ),
        dbc.CardFooter("Undergraduate applications are frequently re-routed for self-certification via supervisor sign-off"),
    ],
    style={"width": "35rem","align":"center"}
),width="auto"), dbc.Col(
 dbc.Card(
    [
        dbc.CardHeader("From when records began to May 2021 - Approval Requirement to Panel"),
        dbc.CardBody(
            [
    dcc.Graph(figure=fig2),
            ]
        ),
        dbc.CardFooter("Considering self-certified applications versus panel-assess applications, the flow takes on a different shape"),
    ],
    style={"width": "35rem","align":"center"}
), width="auto")],justify="center")
],style={'textAlign': 'center'})

])


@app.callback(
    Output(component_id='bar-container', component_property='children'),
    [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_row_ids'),
     Input(component_id='datatable-interactivity', component_property='selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_indices'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_row_ids'),
     Input(component_id='datatable-interactivity', component_property='active_cell'),
     Input(component_id='datatable-interactivity', component_property='selected_cells')]
)
def update_bar(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
               order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):
    dff = pd.DataFrame(all_rows_data)

    colors = ['#7FDBFF' if i in slctd_row_indices else '#0074D9'
              for i in range(len(dff))]

    if "Supervisor" in dff:
        return [
            dcc.Graph(id='bar-chart',
                      figure=px.bar(
                          data_frame=dff,
                          x='Supervisor',
                          labels={"count": "Total applications"},hover_data={"Project Title"},color="Type"
                      )
                      )
        ]

@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]

if __name__ == '__main__':
    app.run_server(debug=True)