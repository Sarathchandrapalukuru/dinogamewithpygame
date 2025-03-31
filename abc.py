import RPi.GPIO as GPIO
import time
import pyautogui  # Alternative to keyboard module

# Define the GPIO pin for the touch sensor
TOUCH_SENSOR_PIN = 4  # Change this if using a different pin

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def touch_callback(channel):
    print("Touch detected! Simulating Space key press...")
    pyautogui.press('space')

# Detect touch event
GPIO.add_event_detect(TOUCH_SENSOR_PIN, GPIO.RISING, callback=touch_callback, bouncetime=200)

try:
    print("Waiting for touch input...")
    while True:
        time.sleep(0.1)  # Reduce CPU usage
except KeyboardInterrupt:
    print("Exiting... Cleaning up GPIO")
    GPIO.cleanup()
