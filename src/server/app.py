import RPi.GPIO as GPIO                                                                  
from flask import Flask, render_template, request, Response                                      
import requests
import json
import gzip
from io import BytesIO
import time
import os

app = Flask(__name__)

def set_light(light, state):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    if light == 'red':
        GPIO.setup(18,GPIO.OUT)
        if state == 'on':
            GPIO.output(18,GPIO.HIGH)
        elif state == 'off':
            GPIO.output(18,GPIO.LOW)
    if light == 'white':
        GPIO.setup(17,GPIO.OUT)
        if state == 'on':
            GPIO.output(17,GPIO.HIGH)
        elif state == 'off':
            GPIO.output(17,GPIO.LOW)

@app.route("/")                                                          
def update_light():
    state = request.args.get('state')
    light = request.args.get('light')

    set_light(light, state)
        
    return render_template('index.html')

@app.route('/flicker')
def flicker_lights():
    print("Flicker Lights")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17,GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(18,GPIO.OUT, initial=GPIO.LOW)
    
    t_end = time.time() + 40
    while time.time() < t_end:
        GPIO.output(18,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(17,GPIO.HIGH)
        GPIO.output(18,GPIO.LOW)
        time.sleep(1)
        GPIO.output(17,GPIO.LOW)

@app.route('/fight_song_player')
def fight_song_player():
    print("Song Queried")
    path_to_file = "../../assets/FightSong.wav"

    def generate():
        with open(path_to_file, "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    print("Song sent")
    return Response(generate(), mimetype="audio/x-wav")


@app.route('/fight_song')
def fight_song():
    return render_template('fight_song.html')
# @app.route("/wolfpack")
# def wolfpack():
#     return render_template('wolfpack.html')

@app.route('/wolfpack')
def get_data():
    sports = {
        # 'hockey': ['mens-college-hockey', 'womens-college-hockey'], 
        # 'basketball': ['mens-college-basketball', 'womens-college-basketball'], 
        # 'soccer': ['mens-college-soccer', 'womens-college-soccer'], 
        'football': ['college-football']
        }
    for sport in sports:
        print(sport)
        game_data = {}
        for league in sports[sport]:
            print(league)
            game_data[league] = []
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
                
            events = data['sports'][0]['leagues'][0]['events']
            for event in events:
                competitors = event['competitors']
                if 'wolfpack' in str(competitors[0]['displayName']).lower() or 'wolfpack' in str(competitors[1]['displayName']).lower():
                    game_data[league].append(event)
                    
    #print(data)
    current_games = []
    past_games = []
    next_games = []
    game_data_stats = {}
    for league in game_data.keys():
        for event in game_data[league]:
            if event['status'] == 'pre':
                next_games.append(event)
            elif event['status'] == 'post':
                past_games.append(event)
            elif event['status'] == 'current':
                current_games.append(event)
                
    if len(next_games) > 0:
        game_data_stats['next_game'] = {}
        game_data_stats['next_game']['date'] = next_games[0]['date'].split("T")[0]
        game_data_stats['next_game']['time'] = next_games[0]['summary']
        game_data_stats['next_game']['location'] = next_games[0]['location']
        game_data_stats['next_game']['comp1'] = next_games[0]['competitors'][0]['displayName']
        game_data_stats['next_game']['comp2'] = next_games[0]['competitors'][1]['displayName']
        
    if len(past_games) > 0:
        game_data_stats['past_game'] = {}
        if past_games[0]['competitors'][0]['displayName'] == 'NC State Wolfpack' and past_games[0]['competitors'][0]['winner'] == 'true':
            set_light("red", "on")
        elif past_games[0]['competitors'][1]['displayName'] == 'NC State Wolfpack' and past_games[0]['competitors'][1]['winner'] == 'true':
            set_light("red", "on")
        game_data_stats['past_game']['date'] = past_games[0]['date'].split("T")[0]
        game_data_stats['past_game']['time'] = past_games[0]['summary']
        game_data_stats['past_game']['location'] = past_games[0]['location']
        game_data_stats['past_game']['comp1'] = past_games[0]['competitors'][0]['displayName']
        game_data_stats['past_game']['comp1_score'] = past_games[0]['competitors'][0]['score']
        game_data_stats['past_game']['comp2'] = past_games[0]['competitors'][1]['displayName']
        game_data_stats['past_game']['comp2_score'] = past_games[0]['competitors'][1]['score']
    
    template_data = {
        "date" : game_data_stats['next_game']['date'],
        "location" : game_data_stats['next_game']['location'],
        "time" : game_data_stats['next_game']['time'],
        "comp1" : game_data_stats['next_game']['comp1'],
        "comp2" : game_data_stats['next_game']['comp2']
    }
    print(game_data_stats['next_game'])

    return  render_template("wolfpack.html", **template_data)

if __name__ == "__main__":
   app.run(debug=True)