import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import requests
import io

# Fetch and process CSV data
csv_url = 'https://gist.githubusercontent.com/fullstacc/98d5f1a17165b3f9f4790845671efdc6/raw/697d5f8aa08aca22f423f8efe8993630e062145e/mlb-2023.csv'
csv_data = requests.get(csv_url).content
data = pd.read_csv(io.StringIO(csv_data.decode('utf-8')))

win_counts = {}
for _, row in data.iterrows():
    winner = row['team1'] if row['score1'] > row['score2'] else row['team2']
    win_counts[winner] = win_counts.get(winner, 0) + 1

top_teams = sorted(win_counts.items(), key=lambda x: x[1], reverse=True)[:10]

# Create the Dash app
app = dash.Dash(__name__)

# Layout for the app
app.layout = html.Div([
    html.H1("Top 10 MLB Teams by Wins, April 18 2023", style={
            'textAlign': 'center', 'fontFamily': 'Roboto, sans-serif'}),
    dcc.Graph(
        id='mlb-bar-chart',
        figure={
            'data': [
                go.Bar(
                    x=[team for team, _ in top_teams],
                    y=[wins for _, wins in top_teams],
                    marker={'color': 'steelblue'}
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Teams'},
                yaxis={'title': 'Number of Wins'},
                font={'family': 'Roboto, sans-serif'},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
