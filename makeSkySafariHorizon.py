#!/usr/bin/env python3
import csv
import sys
from PIL import Image,ImageDraw

# Constants
#    macOS size is 4096 x 2048
# WIDTH = 4096
# HEIGHT = 2048
#    iOS size is 2048 x 1024
WIDTH = 2048
HEIGHT = 1024
COLOR = (50, 200, 50, 200)

horizon = []
BOT = HEIGHT - 1

def sort_key(row):
    return row[0]

def AzToX(az):
    return int(az*WIDTH/360)

# Note: Sky Safari supports horizons below 0 in its horizon panorama support, I believe.
# However, this program expects the altitude to be between 0 and 90.
def AltToY(alt):
    #    return int(2048-(alt*1024/90+1024))
    HALF = HEIGHT/2
    # return int(WIDTH-(alt*1024/90+1024))
    return int(HEIGHT-(alt*HALF/90+HALF))

def drawPoly(i):
    x1 = AzToX(horizon[i][0])
    y1 = AltToY(horizon[i][1])
    x2 = AzToX(horizon[i+1][0])
    y2 = AltToY(horizon[i+1][1])

    draw.polygon([(x1,y1),(x2,y2),(x2,BOT),(x1,BOT)], fill=COLOR, outline=COLOR, width=1)

###############################
# Main program

# Read the CSV file that describes the horizon

with open('horizon.csv') as csvfile:
    horizon_reader = csv.reader(csvfile)
    for row in horizon_reader:
        row[0] = float(row[0])
        row[1] = float(row[1])
        horizon.append(row)

# Sort the horizon list by azimuth
horizon.sort(key = sort_key)

# Create a new 32 bit image with transparency
img = Image.new(mode='RGBA', size=(WIDTH,HEIGHT), color=(0,0,0,0))
draw = ImageDraw.Draw(img)

k = 0
for row in horizon[:-1]:
    drawPoly(k)
    k = k + 1

# OK, handle the last poly, that wraps around the right/left edge of the screen:

# 1 means left side of the poly, i.e. right most point, just to the left of x=360
Az1 = horizon[-1][0]
Alt1 = horizon[-1][1]
# 2 means right side of the poly, i.e. left most point, just to right of x=0
Az2 = horizon[0][0]
Alt2 = horizon[0][1]

x_diff = Az2+360 - Az1
if x_diff == 0:
    portion = 1
else:
    portion = (360 - Az1)/x_diff

y_diff = Alt2 - Alt1
y_wrap = Alt1 + portion*y_diff

# Convert from degrees to pixel measurements
x1 = AzToX(Az1)
y1 = AltToY(Alt1)
x2 = AzToX(Az2)
y2 = AltToY(Alt2)
y_wrap = AltToY(y_wrap)

draw.polygon([(x1,y1), ((WIDTH-1),y_wrap), ((WIDTH-1),BOT), (x1,BOT)], fill=COLOR, outline=COLOR, width=1)
draw.polygon([(x2,y2), (   0,y_wrap), (   0,BOT), (x2,BOT)], fill=COLOR, outline=COLOR, width=1)

img.save('image.png', 'PNG')
