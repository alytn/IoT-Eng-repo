from flask import Flask
from gpiozero import LED
from time import sleep

app = Flask(__name__)
led = LED(17)

@app.route('/led/on')
def led_on():
    led.on()
    return "LED is ON"

@app.route('/led/off')
def led_off():
    led.off()
    return "LED is OFF"

@app.route('/led/blink')
def led_blink():
    led.blink(on_time=0.5, off_time=0.5)
    return "LED is BLINKING"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
