from flask import Flask
import RPi.GPIO as GPIO
from time import sleep

app = Flask(__name__)
servo23 = 23 #Servo Motor 1
servo22 = 22 #Servo Motor 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo23, GPIO.OUT)
GPIO.setup(servo22, GPIO.OUT)

servo1 = GPIO.PWM(servo23, 50)
servo2 = GPIO.PWM(servo22, 50)
servo1.start(7.5)
servo2.start(7.5)

@app.route('/surprise')
def surprise():
    servo1.ChangeDutyCycle(12.5) #180 degrees
    servo2.ChangeDutyCycle(12.5) #180 degrees
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0) #servo reset
    servo2.ChangeDutyCycle(0)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(2.5) #0 degrees reset
    servo2.ChangeDutyCycle(2.5) #0 degrees reset
    return "Gambling!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)