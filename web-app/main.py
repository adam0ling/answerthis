import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_gif_component as gif
import json
from dash.dependencies import Input, Output, State

from email_send import send_email
from wirte_tweets import writeTweet

import requests
import numpy as np
import os

# external stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP]

# launch app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True


class DashCallbackVariables:
    """Class to store information useful to callbacks"""

    def __init__(self):
        self.n_clicks = {1: 0}

    def update_n_clicks(self, nclicks, bt_num):
        self.n_clicks[bt_num] = nclicks


callbacks_vars = DashCallbackVariables()

colors = {
    'background': '#FFFFFF',
    'text': '#383c4a',
    'styledBackground': '#30333d'
}

style_cell={
    'font-size': 14,
    'color': colors['text'],
    'backgroundColor': colors['background'],
    'whiteSpace':'normal'
}

app.layout = html.Div([
    html.Div([], style={'padding':30}),
    html.H1(
            children='May the rng gods amuse you',
            style={
                'textAlign': 'center',
                'color': colors['text']
                }
    ),
    html.Div(
        children='Ask me whatever you want to know:', style={
                'textAlign': 'center',
                'color': colors['text']
                }
    ),
    html.Div([], style={'padding':15}),
    dbc.Row([
        dbc.Col('', width=3),
        dbc.Col([
            dbc.Input(
                    id='question',
                    type='text',
                    placeholder='ask me already...',
                    style=style_cell
                ),
            html.Div([],style={
                'textAlign': 'center',
                'color': colors['text'],
                'padding':10}),
            dbc.Button('Le go', id='button', color='primary'),
        ]),
        dbc.Col('', width=3)                                        
    ],style={
                'textAlign': 'center',
                'color': colors['text'],
                'padding':10}),
    html.Div([],style={
                'textAlign': 'center',
                'color': colors['text'],
                'padding':10}),
    html.Div(
        [
        dbc.Modal(
            [
                dbc.ModalHeader(id='question_modal'),
                dbc.ModalBody(children=[
                    html.Div(
                        'Cyber monkeys are trying to find the typewriter...', 
                        id='answer_1'),
                    html.Div(children=[
                        gif.GifPlayer(
                            gif='../assets/monkey.gif',
                            still='../assets/monkey_still.png',
                            autoplay=True
                        ),], style={
                                    'textAlign': 'center',
                                    'color': colors['text'],
                                    'padding':10}, id='tweet-it')                    
                                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", color='light', className="ml-auto")
                ),
            ],
            id="modal",
        ),
        ], style={
                'textAlign': 'center',
                'color': colors['text'],
                'padding':10},
    )
], style={'backgroundColor': colors['background']})


# callbacks
@app.callback(
    [Output('answer_1', 'children'),
    Output('tweet-it', 'children'),
    Output('question_modal', 'children')],
    [Input('button', 'n_clicks')],
    [State('question', 'value')])
def update_output(n_clicks, value):
    if n_clicks:
        # It was triggered by a click on the button 1
        url = 'http://0.0.0.0/generator?text='+value  # change to actual api ip
        callbacks_vars.update_n_clicks(n_clicks, 1)
        seed = np.random.randint(1,9999999999)
        length = 400
        answer = requests.get(url, timeout=60)
        
        # email sending
        message = answer.json()[0]
        message = message.replace(':', '>>>')
        send_email(message)

        # twitter module
        tweet_it = html.Div([
                            dbc.Input(
                                id='at',
                                type='text',
                                placeholder='@placeholder',
                                style=style_cell
                            ),
                            dbc.FormText("answerthis does not take any responsibility for your tweets. Please act responsibly."),
                            html.Div([],style={
                                    'textAlign': 'center',
                                    'color': colors['text'],
                                    'padding':10}),
                    dbc.Button('Tweet it!', id='tweet_btn', color='primary', className='mr-1'),
                    html.A(dbc.Button('Read the Tweets', id='other_tweets', color='link', className='mr-1'), href='https://twitter.com/answerthisbot', target="_blank"),
                            ],style={
                                    'textAlign': 'center',
                                    'color': colors['text'],
                                    'padding':10})

        return dcc.Markdown(answer.json()[0], id='answer_modal'), html.Div([tweet_it]), value

@app.callback(
    Output('modal','is_open'),
    [Input('button', 'n_clicks'), Input('close','n_clicks')],
    [State('modal', 'is_open')]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    [Output('tweet_btn', 'color'),
    Output('tweet-link', 'children')],
    [Input('tweet_btn', 'n_clicks'),
    Input('question_modal', 'children'),
    Input('answer_modal', 'children'),
    Input('at', 'value')]
)
def tweet(n_clicks, question, answer, at):
    if n_clicks:
        if at[:1] !='@':
            at = '@'
        answer = answer[answer.find('Answer:')+7:]
        a = writeTweet(question, answer, at)
        # linkT = 'https://twitter.com/answerthisbot/status/'+str(a)
        col = 'success'
        return col
    else:
        col = 'primary'
        return col
            
        

if __name__ == '__main__':
    app.server(host='0.0.0.0', port=8080, debug=True)
