import pandas as pd

# Criando um dataset fictício
data = {
    "Time": ["Time A", "Time A", "Time A", "Time B", "Time B", "Time B"],
    "Adversário": ["Time B", "Time C", "Time D", "Time A", "Time C", "Time D"],
    "Posse de Bola (%)": [60, 55, 70, 40, 45, 30],
    "Chutes a Gol": [10, 8, 12, 5, 7, 3],
    "Resultado": ["Vitória", "Derrota", "Vitória", "Derrota", "Empate", "Derrota"]
}

# Convertendo o dicionário em um DataFrame do pandas
df = pd.DataFrame(data)

# Visualizando o dataset
print(df)


# Contando o número de vitórias e derrotas para cada time
vitórias = df[df['Resultado'] == 'Vitória'].groupby('Time').size()
derrotas = df[df['Resultado'] == 'Derrota'].groupby('Time').size()

# Calculando a média de posse de bola e chutes a gol para cada time
media_posse = df.groupby('Time')['Posse de Bola (%)'].mean()
media_chutes = df.groupby('Time')['Chutes a Gol'].mean()

# Exibindo os resultados
print("Vitórias por Time:\n", vitórias)
print("Derrotas por Time:\n", derrotas)
print("Média de Posse de Bola por Time:\n", media_posse)
print("Média de Chutes a Gol por Time:\n", media_chutes)


import dash
from dash import dcc, html
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__)

# Layout da aplicação
app.layout = html.Div([
    html.H1("Análise de Jogos de Futebol"),
    
    html.Div([
        dcc.Dropdown(
            id='select-time',
            options=[{'label': time, 'value': time} for time in df['Time'].unique()],
            value='Time A',
            clearable=False
        )
    ], style={'width': '50%', 'margin': '20px auto'}),
    
    html.Div(id='output-metrics'),

    dcc.Graph(id='graph-posse-chutes')
])

# Callback para atualizar as métricas e o gráfico
@app.callback(
    [Output('output-metrics', 'children'),
     Output('graph-posse-chutes', 'figure')],
    [Input('select-time', 'value')]
)
def update_metrics(time):
    # Filtrando dados pelo time selecionado
    time_data = df[df['Time'] == time]
    
    # Calculando métricas
    vitórias = time_data[time_data['Resultado'] == 'Vitória'].shape[0]
    derrotas = time_data[time_data['Resultado'] == 'Derrota'].shape[0]
    media_posse = time_data['Posse de Bola (%)'].mean()
    media_chutes = time_data['Chutes a Gol'].mean()
    
    # Criando os elementos HTML para exibir as métricas
    metrics = [
        html.P(f"Vitórias: {vitórias}"),
        html.P(f"Derrotas: {derrotas}"),
        html.P(f"Média de Posse de Bola: {media_posse:.2f}%"),
        html.P(f"Média de Chutes a Gol: {media_chutes:.2f}")
    ]
    
    # Criando um gráfico de barras para posse de bola e chutes a gol
    fig = px.bar(time_data, x='Adversário', y=['Posse de Bola (%)', 'Chutes a Gol'],
                 barmode='group', title=f"Desempenho do {time} por Adversário")
    
    return metrics, fig

if __name__ == '__main__':
    app.run_server(debug=True)
