import pandas as pd
import requests
import dash
import string
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from pprint import pprint

base_url = 'https://api.coronatab.app'
country_url = f'{base_url}/places?typeId=country'
data = requests.get(country_url).json()

app = dash.Dash(external_stylesheets=[dbc.themes.LUMEN])

app.layout = html.Div([
  html.H1('COVID-19 Live Dashboard'),
  dcc.Input(id='input', value='', type='text'),
  html.Div(id='output-graph')
], className='container')

@app.callback(Output(component_id='output-graph', component_property='children'),
              [Input(component_id='input', component_property='value')])
def update_graph(country_name):
  if country_name == '':
    return
  
  for country in data['data']:
    # if country_name in [country['alpha2code'], country['alpha3code'], country['name']]:
    if country_name in country['alpha2code'] or country_name in country['alpha3code'] or country_name in country['name']:
      latest_data = country['latestData']
      return [
        dcc.Graph(
          id='country-graph',
          animate=True,
          figure={
            'data': [{
              'x': ['Deaths', 'Cases', 'Recovered'],
              'y': [latest_data['deaths'], latest_data['cases'], latest_data['recovered']],
              'type': 'bar',
              'name': country_name
            }],
            'layout': {
              'title': country_name
            }
          }
        ),
        html.P(f"Last updated on {latest_data['date']} for {country['name']}")
      ]
  
if __name__ == "__main__":
  app.run_server(debug=True)