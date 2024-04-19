# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import Dash, html, dcc


# initializing the app
app =dash.Dash()

# set app layout

app.layout = html.Div(html.H1('Moonrise over Hamburg, Shanghai, Bali 🌙'))   # creates header for website

if __name__ == '__main__':
     app.run_server()  # runs a local server for the website to run on