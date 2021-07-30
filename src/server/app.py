import time
import RPi.GPIO as GPIO                                                                  
from flask import Flask, render_template, request                                       

app = Flask(__name__)

@app.route('/get_toggled_status') 
def get_toggled_status():
  current_status = request.args.get('status')
  print(current_status)
  return 'Toggled' if current_status == 'Untoggled' else 'Untoggled'

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
    print("\n-------")
    print(state)
    print(light)
    set_red_light(light, state)
        
            
    template_data = {                                                           
        'title' : state,                                                        
    }   
    return render_template('index.html', **template_data)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)