import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash_extensions import Lottie       # pip install dash-extensions
import plotly.express as px
import pandas as pd
from dash.dependencies import Output, Input
from cc_stats import DataAnalysis

def my_dashboard():

    #Load clean data
    gas_data = DataAnalysis().consumption_data()
    only_glp_data = gas_data[gas_data['Tipo_combustible'] == 17]


    # Lottie by Emil - https://github.com/thedirtyfew/dash-extensions
    url_kms = "https://assets9.lottiefiles.com/private_files/lf30_mtifqxx7.json"
    url_lt_per_km = "https://assets10.lottiefiles.com/private_files/lf30_px09jhc8.json"
    url_total = "https://assets7.lottiefiles.com/temp/lf20_EqtckR.json"
    url_dto = "https://assets1.lottiefiles.com/private_files/lf30_ptwvrbdt.json"
    url_lts_glp = "https://assets1.lottiefiles.com/packages/lf20_zqojwy4n.json"
    url_lts_g95 = "https://assets4.lottiefiles.com/packages/lf20_pqxofxw9.json"
    url_header = "https://assets8.lottiefiles.com/private_files/lf30_nhg4au0e.json"
    options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))


    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])


    app.layout = dbc.Container([
        # First row
        dbc.Row([
            dbc.Col([
                dbc.Card([dbc.CardHeader(Lottie(options=options, width="15%", height="15%", url=url_header)),
                    dbc.CardBody([
                        html.H1(
                        children="Análisis consumo combustible", className="header-title"),
                        html.P(
                        children="Dacia Sandero Stepway 2021,"
                        " desde su primer repostaje",
                        className="header-description",)
                    ], style={'textAlign':'center'})
                ]),

            ], width=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.DatePickerRange(
                                id="date-range",
                                min_date_allowed=gas_data.Fecha.min().date(),
                                max_date_allowed=gas_data.Fecha.max().date(),
                                start_date=gas_data.Fecha.min().date(),
                                display_format='DD-MMM-YY',
                                end_date=gas_data.Fecha.max().date(),
                                className=""
                            )
                    ])
                ]),
            ], width=4),
        ],className='mb-2 mt-2'),
        # Second row
        dbc.Row([
            dbc.Col([
                dbc.Card([dbc.CardHeader(Lottie(options=options, width="35%", height="35%", url=url_kms)),
                    dbc.CardBody([
                        html.H6('Kilometros recorridos'),
                        html.H2(id='kms_rec', children="000")
                    ], style={'textAlign':'center'})
                ]),
            ], width=2),
            dbc.Col([
                dbc.Card([dbc.CardHeader(Lottie(options=options, width="35%", height="35%", url=url_lt_per_km)),
                    dbc.CardBody([
                        html.H6('Media consumo\n Lts x 100km'),
                        html.H2(id='lt_x_km', children="000")
                    ], style={'textAlign':'center'})
                ]),
            ], width=2),
            dbc.Col([
                dbc.Card([dbc.CardHeader(Lottie(options=options, width="35%", height="35%", url=url_total)),
                    dbc.CardBody([
                        html.H6('Gasto total'),
                        html.H2(id='total', children="000")
                    ], style={'textAlign':'center'})
                ]),
            ], width=2),
            dbc.Col([
                dbc.Card([dbc.CardHeader(Lottie(options=options, width="35%", height="35%", url=url_dto)),
                    dbc.CardBody([
                        html.H6('Gasto con descuentos'),
                        html.H2(id='dto', children="000")
                    ], style={'textAlign':'center'})
                ]),
            ], width=2),
            dbc.Col([
                dbc.Card([dbc.CardHeader(Lottie(options=options, width="65%", height="65%", url=url_lts_glp)),
                    dbc.CardBody([
                        html.H6('Media valor litro GLP'),
                        html.H2(id='GLP', children="000")
                    ], style={'textAlign':'center'})
                ]),
            ], width=2),
            dbc.Col([
                dbc.Card([dbc.CardHeader(Lottie(options=options, width="35%", height="35%", url=url_lts_g95)),
                    dbc.CardBody([
                        html.H6('Media valor litro Gasolina 95'),
                        html.H2(id='g95', children="000")
                    ], style={'textAlign':'center'})
                ]),
            ], width=2),
        ],className='mb-2'),
        #   third row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='lt_line_chart', figure={}),
                    ])
                ]),
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='days_bar_chart', figure={}),
                    ])
                ]),
            ], width=6),
        ],className='mb-2'),

        # fourth row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='total_line_chart', figure={}),
                    ])
                ]),
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='totals_sunburst-chart', figure={}),
                    ])
                ]),
            ], width=6),
            # dbc.Col([
            #     dbc.Card([
            #         dbc.CardBody([
            #             dcc.Graph(id='line-chart', figure={}),
            #         ])
            #     ]),
            # ], width=4),
        ],className='mb-2'),
    ], fluid=True)

    # Update the six small cards
    @app.callback(
        Output("kms_rec", "children"),
        Output("lt_x_km", "children"),
        Output("total", "children"),
        Output("dto", "children"),
        Output("GLP", "children"),
        Output("g95", "children"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        )

    def update_small_cards(start_date, end_date):
        df_c = gas_data.copy()
        # Replace 0 in lt_x_km with mean for mean purposes
        df_c['lt_x_km'] = df_c['lt_x_km'].replace(0,df_c['lt_x_km'].mean())
        df_c = df_c[(df_c['Fecha']>=start_date) & (df_c['Fecha']<=end_date)]

        total_km = f"{df_c.loc[df_c['Tipo_combustible'] == 17, 'Kms_btw_rec'].sum()} kms"
        avg_lt_x_km = f"{round(df_c.loc[df_c['Tipo_combustible'] == 17,'lt_x_km'].mean(), 2)}"
        total_payment = f"{round(df_c['Total'].sum(), 2)} €"
        total_pay_dto = f"{round(df_c['Total_dtos'].sum(), 2)} €"
        avg_lt_glp = f"{round(df_c.loc[df_c['Tipo_combustible'] == 17, 'Precio_lt'].mean(), 2)} €"

        avg_g95 = round(df_c.loc[df_c['Tipo_combustible'] == 1, 'Precio_lt'].mean(), 2)
        if avg_g95 > 0:
            avg_lt_g95 = f"{avg_g95} €"
        else:
             avg_lt_g95 = "Sin repostar"

       # avg_lt_g95 = f"{round(avg_lt_g95, 2)} €"

        return total_km, avg_lt_x_km, total_payment, total_pay_dto, avg_lt_glp, avg_lt_g95

    @app.callback(
        Output("lt_line_chart", "figure"),
        Output("days_bar_chart", "figure"),
        Output("total_line_chart", "figure"),
        Output("totals_sunburst-chart", "figure"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        )
    def update_charts(start_date, end_date):
        df_c = gas_data.copy()
        df_c = df_c[(df_c['Fecha']>=start_date) & (df_c['Fecha']<=end_date)]
        only_glp = df_c.loc[df_c['Tipo_combustible'] == 17]

        # --------------- line liters chart ---------------------------
        fig_line_lt = px.line(only_glp, x="Fecha", y="Precio_lt", hover_data=['Est._servicio'],
                  color_discrete_sequence=px.colors.qualitative.Vivid,
                  template = "plotly_dark",
                  labels={
                         "Precio_lt": "€",
                         "Fecha": "Fecha repostaje",
                         "value": "Total €"
                     },
                    title="Valor litro GLP")
        fig_line_lt.update_layout(
                       title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                       font=dict(color='#8a8d93'))

        # --------------- days bar chart ---------------------------

        df_days  = pd.DataFrame(df_c['Día'].value_counts())
        df_days = df_days.reset_index()
        df_days.columns = ['Día', 'cant']

        fig_days_bar = px.bar(df_days, x='cant', y='Día', color='Día',
                              color_discrete_sequence=px.colors.qualitative.Vivid,
                              template = "plotly_dark",
                              labels={"cant": "Nº de veces repostaje por día",
                                      "Día": "Día de la semana"},
                                orientation='h', title="Veces repostaje por días")
        fig_days_bar.update_yaxes(tickangle=45)
        fig_days_bar.update_layout(
                       title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                       font=dict(color='#8a8d93'))
        #fig_days_bar.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
        #ig_days_bar.update_layout(margin=dict(l=20, r=20, t=30, b=20))


        # --------------- Total line chart --------------------------------------------
        fig_total_line = px.line(df_c, x="Fecha", y=["Total_dtos", "Total"], hover_data=['Litros'],
                  color_discrete_sequence=px.colors.qualitative.D3,
                  template = "plotly_dark",
                  labels={
                         "variable": "",
                         "Fecha": "Fecha repostaje",
                         "value": "Total €"
                     },
                    title="Total cuenta con y sin descuentos")
        fig_total_line.update_layout(
                       title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                       font=dict(color='#8a8d93'))

        # ------------------- Sunburst chart ------------------------------------------


        fig_sunburst = px.sunburst(df_c,
                      path=["Combustible", "Est._servicio", "Precio_lt"],
                      color_discrete_sequence=px.colors.qualitative.D3,
                      values='Total_dtos',
                      title="Gasto combustible",
                      #width=450, height=450,
                                   template = "plotly_dark")
        fig_sunburst.update_layout(margin=dict(l=20, r=20, t=30, b=20))
        fig_sunburst.update_layout(title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                       font=dict(color='#8a8d93'))

        return fig_line_lt, fig_days_bar, fig_total_line, fig_sunburst


    app.run(debug=True, use_reloader=False)
    #return app.run_server(debug=False, port=8001)

