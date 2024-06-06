
import csv
import sys
from PIL import Image,ImageDraw

# Constants
BOT = 2047
COLOR = (50, 200, 50, 200)

horizon = []

def sort_key(row):
    return row[0]

def AzToX(az):
    return int(az*4096/360)

# Note: Sky Safari supports horizons below 0 in its horizon panorama support, I believe.
# However, this program expects the altitude to be between 0 and 90.
def AltToY(alt):
    return int(2048-(alt*1024/90+1024))

def drawPoly(i):
    print( i, horizon[i][0],horizon[i][1],horizon[i+1][0],horizon[i+1][1])
    x1 = AzToX(horizon[i][0])
    y1 = AltToY(horizon[i][1])
    x2 = AzToX(horizon[i+1][0])
    y2 = AltToY(horizon[i+1][1])

    # draw.polygon([(horizon[i][0],horizon[i][1]),(horizon[i+1][0],horizon[i+1][1]),(horizon[i+1][0],BOT),(horizon[i][0],BOT)], fill=COLOR, outline=(50,50,255), width=10)
    draw.polygon([(x1,y1),(x2,y2),(x2,BOT),(x1,BOT)], fill=COLOR, outline=COLOR, width=1)

# Main program
# Read the CSV file that describes the horizon

with open('horizon.csv') as csvfile:
    horizon_reader = csv.reader(csvfile)
    for row in horizon_reader:
        #print(row)
        row[0] = float(row[0])
        row[1] = float(row[1])
        horizon.append(row)

horizon.sort(key = sort_key)
#print(horizon)

# Graphics stuff
#img = image.open('image.png')
#rbga = img.convert('RGBA')

img = Image.new(mode='RGBA', size=(4096,2048), color=(0,0,0,0))

draw = ImageDraw.Draw(img)
# draw.polygon([(546,443),(887,321),(887,2047),(546,2047)], fill=COLOR, outline=COLOR, width=1)
drawPoly(0)

k = 0
for row in horizon[:-1]:
    #print(k, row[0])
    drawPoly(k)
    k = k + 1

# OK, handle the last poly, that wraps around the right/left edge of the screen:

# 1 means left side of the poly, i.e. right most point, just to the left of x=360
Az1 = horizon[-1][0]
Alt1 = horizon[-1][1]
# 2 means right side of the poly, i.e. left most point, just to right of x=0
Az2 = horizon[0][0]
Alt2 = horizon[0][1]

diff = Az2+360 - Az1
portion = (360 - Az1)/diff
print("portion is", portion)

diff2 = Alt2 - Alt1
#y_wrap = Alt1 + portion*(Alt2 - Alt1)
y_wrap = Alt1 + portion*diff2
print("diff2 is", diff2)
print("y_wrap is", y_wrap)

x1 = AzToX(Az1)
y1 = AltToY(Alt1)
x2 = AzToX(Az2)
y2 = AltToY(Alt2)

draw.polygon([(x1,y1), (4095,y_wrap), (4095,BOT), (x1,BOT)], fill=COLOR, outline=COLOR, width=1)
draw.polygon([(x2,y2), (   0,y_wrap), (   0,BOT), (x2,BOT)], fill=COLOR, outline=COLOR, width=1)

img.save('image.png', 'PNG')
