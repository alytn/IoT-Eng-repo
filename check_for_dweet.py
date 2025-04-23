import requests
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import logging

# Configuration
THING_NAME = "7a2c4b0c"  # Your unique dweet "thing" name
LED_GPIO_PIN = 17
DWEET_URL = f"https://dweet.io/get/latest/dweet/for/{THING_NAME}"

# Logging setup (optional)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DweetLED")

# Set up GPIO pin using PiGPIOFactory (best for remote/advanced control)
from gpiozero import Device
Device.pin_factory = PiGPIOFactory()

# Initialize LED
led = LED(LED_GPIO_PIN)
last_state = None

def get_led_state():
    try:
        response = requests.get(DWEET_URL)
        response.raise_for_status()
        data = response.json()

        content = data['with'][0]['content']
        return content.get('state')
    except Exception as e:
        logger.warning(f"Error fetching dweet: {e}")
        return None

def set_led(state):
    global last_state
    if state == last_state:
        return  # no change
    if state == "on":
        led.on()
        logger.info("LED turned ON")
    elif state == "off":
        led.off()
        logger.info("LED turned OFF")
    elif state == "blink":
        led.blink()
        logger.info("LED set to BLINK")
    else:
        led.off()
        logger.info("Unknown state received; turning LED OFF")

    last_state = state

# Main loop
logger.info("Listening for dweets. Press Ctrl+C to stop.")
try:
    while True:
        state = get_led_state()
        if state:
            set_led(state)
        sleep(2)
except KeyboardInterrupt:
    logger.info("Exiting... Turning LED off.")
    led.off()
