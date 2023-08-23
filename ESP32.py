import machine # Import the machine module
import time
import network
from umail import SMTP
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# Replace with your network credentials
SSID = "your_SSID"
PASSWORD = "your_PASSWORD"

# Email configuration
EMAIL_HOST = "smtp.gmail.com"  #server address
EMAIL_PORT = 465  #server port
EMAIL_USER = "....@gmail.com"
EMAIL_PASSWORD = "your_email_password"
EMAIL_FROM = "......@gmail.com"
EMAIL_TO = "......@gmail.com"
EMAIL_SUBJECT = "Motion Detected!"

# Motion detection settings
MOTION_PIN = 23 # GPIO pin number
motion_detected = False

# display configuration
OLED_WIDTH = 120
OLED_HEIGHT = 60
i2c = I2C(scl=Pin(4), sda=Pin(5), freq=100000)  # Adjust pin numbers as needed
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    while not sta_if.isconnected():
        pass

def send_email():
    smtp = SMTP(EMAIL_HOST, EMAIL_PORT, ssl=True)
    smtp.login(EMAIL_USER, EMAIL_PASSWORD)
    
    msg = f"From: {EMAIL_FROM}\nTo: {EMAIL_TO}\nSubject: {EMAIL_SUBJECT}\n\nIntruder alert!" # Email body
    smtp.sendmail(EMAIL_FROM, EMAIL_TO, msg)
    
    smtp.quit()

def setup():
    connect_wifi()
    
    motion_pin = machine.Pin(MOTION_PIN, machine.Pin.IN)
    
    oled.fill(0)  # Clear the display
    oled.text("Waiting for", 0, 0)
    oled.text("authorization...", 0, 16)
    oled.show()

def display_welcome():
    oled.fill(0)
    oled.text("WELCOME", 20, 20)
    oled.show()

def loop():
    global motion_detected
    
    motion_value = motion_pin.value()
    
    if motion_value == 1 and not motion_detected:
        print("Motion detected!")
        send_email()
        motion_detected = True
        display_welcome()
    elif motion_value == 0:
        motion_detected = False
    
    time.sleep(1)

setup()
while True:
    loop()
