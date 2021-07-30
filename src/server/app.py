import time
import RPi.GPIO as GPIO                                                                  
from flask import Flask, render_template, request                                       

app = Flask(__name__)

def set_red_light(light, state):
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

    set_red_light(light, state)
        
    return render_template('index.html')

@app.route("/alarm")
def alarm():
    return render_template('alarm.html')

@app.route("/wolfpack")
def wolfpack():
    return render_template('wolfpack.html')

if __name__ == "__main__":
   app.run(debug=True)