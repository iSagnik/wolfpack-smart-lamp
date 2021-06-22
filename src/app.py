from flask import Flask
import pandas as pd
import requests
import json
import gzip
from io import BytesIO
import csv
import time

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<a href = '/get-data'>Get Data</a>"

@app.route('/get-data')
def get_data():
    sport = 'hockey'
    league = 'mens-college-hockey'
    URL = f"https://site.web.api.espn.com/apis/v2/scoreboard/header?sport={sport}&league={league}&region=us&contentorigin=espn&tz=America/New_York"
    headers = {
        'Connection' : 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': '*/*',
    }
    try:
        response = requests.get(URL, headers = headers)
        content = gzip.GzipFile(fileobj=BytesIO(response.content)).read().decode('utf-8')
        data = json.loads(content)
    except:
        content = response.content.decode()
        data = json.loads(content)
    #print(data)

    events = data['sports'][0]['leagues'][0]['events']
    print(events)
    data_string = json.dumps(data, indent=4)
    html_string = f"<p>{data_string}</p><hr><a href = '/'>Home</a>"
    return  html_string

if __name__ == "__main__":
    app.run(debug=True)