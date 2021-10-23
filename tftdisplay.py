import busio
import digitalio
from board import SCK, MOSI, MISO, CE0, D25, D24
from PIL import Image, ImageDraw, ImageFont
from time import sleep

from adafruit_rgb_display import color565
import adafruit_rgb_display.ili9341 as ili9341

# the value to display
temp = 25.1
humi = 75.2

# First define some constants to allow easy resizing of shapes.
BORDER = 10
FONTSIZE = 130
FONTSIZEsmall = 60
FONTSIZEsmaller = 40

# color definition
darkgrey = (92, 75, 81)
lightblue = (140, 190, 178)
cream = (242, 235, 191)
sunset = (243, 181, 98)
blood = (240, 96, 96)
white = (255, 255, 255)
black = (0,0,0)

# Configuration for CS and DC pins:
CS_PIN = CE0
DC_PIN = D24
RST_PIN = D25

# Setup SPI bus using hardware SPI:
spi = busio.SPI(clock=SCK, MOSI=MOSI, MISO=MISO)

# Create the ILI9341 display:
disp = ili9341.ILI9341(spi,
                          rotation=0,
                          cs=digitalio.DigitalInOut(CS_PIN),
                          rst=digitalio.DigitalInOut(RST_PIN),
                          dc=digitalio.DigitalInOut(DC_PIN))

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height


def update(humi, temp):
    image = Image.new("RGB", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a green filled box as the background
    draw.rectangle((0, 0, width, height), fill=white)

    # # Draw a smaller inner purple rectangle
    # draw.rectangle(
    #     (BORDER, BORDER, width - BORDER - 1, height - BORDER - 1), fill=darkgrey
    # )

    # disp.image(image)
    # Load a TTF Font
    font = ImageFont.truetype("/home/pi/gitrepo/LabMonitoring/BebasNeue-Regular.ttf", FONTSIZE)
    fontSmall = ImageFont.truetype("/home/pi/gitrepo/LabMonitoring/BebasNeue-Regular.ttf", FONTSIZEsmall)
    fontSmaller = ImageFont.truetype("/home/pi/gitrepo/LabMonitoring/BebasNeue-Regular.ttf", FONTSIZEsmaller)

    # Draw temprature value
    temptext = str(int(temp))
    (temp_width, temp_height) = font.getsize(temptext)
    draw.text(
        (163-temp_width,15),
        temptext,
        font=font,
        fill=black,
    )

    #draw degree sign
    degree = "."
    (degree_width, degree_height) = fontSmall.getsize(degree)
    draw.text(
        (170-degree_width, -15),
        degree,
        font=fontSmall,
        fill=black,
    )

    #draw celcius sign
    signC = "C"
    (signC_width, signC_height) = fontSmall.getsize(signC)
    draw.text(
        (170, 30),
        signC,
        font=fontSmall,
        fill=black,
    )

    #draw dot sign
    dot = "."
    (dot_width, dot_height) = fontSmall.getsize(dot)
    draw.text(
        (170-dot_width,27+signC_height),
        dot,
        font=fontSmall,
        fill=black,
    )

    #draw decimal places
    decimalTemp = str(int(temp*10%10))
    (decimalTemp_width, decimalTemp_height) = fontSmall.getsize(decimalTemp)
    draw.text(
        (170,27+signC_height),
        decimalTemp,
        font=fontSmall,
        fill=black,
    )

    # Draw humidity value
    humitext = str(int(humi))
    (humi_width, humi_height) = font.getsize(humitext)
    draw.text(
        (163-humi_width,15+temp_height+20),
        humitext,
        font=font,
        fill=black,
    )

    #draw percent sign
    signP = "%"
    (signP_width, signP_height) = fontSmall.getsize(signP)
    draw.text(
        (165, 35+temp_height+20),
        signP,
        font=fontSmaller,
        fill=black,
    )

    #draw decimal places
    decimalHumi = str(int(humi*10%10))
    (decimalHumi_width, decimalHumi_height) = fontSmall.getsize(decimalHumi)
    draw.text(
        (170,22+temp_height+20+signP_height),
        decimalHumi,
        font=fontSmall,
        fill=black,
    )

    #draw dot sign
    dot = "."
    (dot_width, dot_height) = fontSmall.getsize(dot)
    draw.text(
        (170-dot_width,22+temp_height+20+signP_height),
        dot,
        font=fontSmall,
        fill=black,
    )
    # sleep(5)
    # Display image.
    disp.image(image)
