# First we need to import the libraries
from time import sleep
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from rpi_TM1638 import TMBoards
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

# We create a variable for the server and the topic
mqtt_server = "test.mosquitto.org"
mqtt_topic = "project2_group2"

# These are the pins on Raspberry Pi we are using for the LED&KEY
STB = 14
CLK = 15
DIO = 18

TM = TMBoards(DIO, CLK, STB, 0)


# This function connects the client to the mqtt topic
# And prints out a message if the connection was successful
def on_connect(client, userdata, flags, rc):
    client.subscribe("project2_group2")
    print("Connected with result code " + str(rc))

# This function defines parameters of the image
# on the OLED screen
def on_message(client, userdata, msg):

    # Define the reset pin
    oled_reset = digitalio.DigitalInOut(board.D4)

    # These numbers vary depending on the size of the OLED screen
    WIDTH = 128
    HEIGHT = 64
    BORDER = 1
    spi = board.SPI()
    oled_cs = digitalio.DigitalInOut(board.D5)
    oled_dc = digitalio.DigitalInOut(board.D6)
    oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, oled_dc, oled_reset, oled_cs)

    # Clear display
    oled.fill(0)
    oled.show()

    # Make sure to create image with mode '1' for 1-bit color
    image = Image.new("1", (oled.width, oled.height))

    # Get drawing object to draw on image
    draw = ImageDraw.Draw(image)

    # Draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    # Draw a smaller inner rectangle
    draw.rectangle((BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1), outline=0, fill=0, )

    # Load default font
    font = ImageFont.load_default()

    # Variable for text = emojis
    text = str(msg.payload)[2:-1]
    (font_width, font_height) = font.getsize(text)
    draw.text((oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2), text, font=font,
              fill=255, )
    # Display image
    if text != " ":
        draw.text((oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2), text, font=font,
                  fill=255, )

        # Display image
        oled.image(image)
        oled.show()


def main():
    # When we run this program the user is connected to the server
    # And can publish to the topic "project2_group2"
    # Anyone who is subscribing to the topic can see the emojis
    # that are sent from this Raspberry Pi
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.subscribe(mqtt_topic)
    client.connect("test.mosquitto.org", 1883, 60)
    client.loop_start()

    # This is the loop for the LED&KEY board
    # Each of them stands for one emoji
    # The last button exits the program
    while True:
        for i in range(8):
            TM.leds[i] = True if TM.switches[i] else False

        if TM.switches[0]:
            client.publish(mqtt_topic, ":-)")
            sleep(0.08)
        if TM.switches[1]:
            client.publish(mqtt_topic, ":-(")
            sleep(0.08)
        if TM.switches[2]:
            client.publish(mqtt_topic, "OK")
            sleep(0.08)
        if TM.switches[3]:
            client.publish(mqtt_topic, "xD")
            sleep(0.08)
        if TM.switches[4]:
            client.publish(mqtt_topic, "(>_<)")
            sleep(0.08)
        if TM.switches[5]:
            client.publish(mqtt_topic, "(-_-)")
            sleep(0.08)
        if TM.switches[6]:
            client.publish(mqtt_topic, "(*_*)")
            sleep(0.08)
        if TM.switches[7]:
            client.publish(mqtt_topic, "Send your emoji")
            sleep(0.08)
            client.unsubscribe(mqtt_topic)
            return


main()
