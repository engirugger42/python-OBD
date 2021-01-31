import sys
#sys.path.insert(0, "/usr/local/lib/python3.8/dist-packages")
import obd
from graphics import *
import tkinter
obd.logger.setLevel(obd.logging.DEBUG) # enables all debug information

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

win = GraphWin("Simple Ass OBD2 Panel", WINDOW_WIDTH, WINDOW_HEIGHT)

connection = obd.OBD(fast=False, timeout=30) # auto-connects to USB or RF port
speedCmd = obd.commands.SPEED # select an OBD command (sensor)
rpmCmd = obd.commands.RPM
fuelCmd = obd.commands.FUEL_LEVEL

def button1(event):
    x, y = event.x, event.y
    print(x,y)

def processClick(clickpoint):
        if clickPoint is None:  # so we can substitute checkMouse() for getMouse()
            text.setText("")
        elif inside(clickPoint, left):
            text.setText("left")
        elif inside(clickPoint, right):
            text.setText("right")
        elif inside(clickPoint, quit):
            win.close()
        else:
            text.setText("")
    
def controlButtons():
    left = Rectangle(Point(675, 50), Point(775, 150))  # points are ordered lower left, upper right
    right = Rectangle(Point(675, 160), Point(775, 260))
    quit = Rectangle(Point(675, 270), Point(775, 370))

    nextText = Text(Point(725, 100), "Next")
    nextText.draw(win)
    prevText = Text(Point(725, 210), "Previous")
    prevText.draw(win)
    text = Text(Point(725, 320), "Exit")
    text.draw(win)

    left.draw(win)
    right.draw(win)
    quit.draw(win)

    return left, right, quit

def dash1Displays():
    speed = Rectangle(Point(75, 50), Point(225, 150))  # points are ordered lower left, upper right
    rpm = Rectangle(Point(250, 50), Point(400, 150))
    fuelLevel = Rectangle(Point(425, 50), Point(575, 150))

    speedText = "Speed"
    rpmText = "RPM"
    fuelText = "Fuel %"
    speedLabel = Text(Point(75+((150-len(speedText))/2), 60), speedText)
    speedLabel.draw(win)
    rpmLabel = Text(Point(250+((150-len(rpmText))/2), 60), rpmText)
    rpmLabel.draw(win)
    fuelLabel = Text(Point(425+((150-len(fuelText))/2), 60), fuelText)
    fuelLabel.draw(win)

    speed.draw(win)
    rpm.draw(win)
    fuelLevel.draw(win)
    
    return speed, rpm, fuelLevel

def inside(point, rectangle):
    """ Is point inside rectangle? """

    ll = rectangle.getP1()  # assume p1 is ll (lower left)
    ur = rectangle.getP2()  # assume p2 is ur (upper right)

    return ll.getX() < point.getX() < ur.getX() and ll.getY() < point.getY() < ur.getY()
    
def readDash1Values():
    #speed, rpm, fuel = dash1Displays()
    
    rpmResponse = connection.query(rpmCmd) # send the command, and parse the response    
    speedResponse = connection.query(speedCmd) # send the command, and parse the response   
    fuelResponse = connection.query(fuelCmd) # send the command, and parse the response

    speedResponseLabel.setText(speedResponse.value.to("mph"))
    
    rpmResponseLabel.setText(rpmResponse.value.to("rpm"))
    
    #fuelResponseText = "%.2f" % round(fuelResponse.value,2)
    fuelResponseLabel.setText(fuelResponse.value.to("percent"))
    
    #speed.draw(win)
    #rpm.draw(win)
    #fuelLevel.draw(win)
       
    return rpmResponse, speedResponse, fuelResponse

#win.bind('<Button-1>>', button1)
left, right, quit = controlButtons()
speed, rpm, fuelLevel = dash1Displays()

centerPoint = Point(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
text = Text(centerPoint, "")
text.draw(win)
speedResponseLabel = Text(Point(75+73, 100), "0.0")
speedResponseLabel.draw(win)    
rpmResponseLabel = Text(Point(250+73, 100), "0000")
rpmResponseLabel.draw(win)
fuelResponseLabel = Text(Point(425+73, 100), "0.0%")
fuelResponseLabel.draw(win)

while True:
    clickPoint = win.getMouse()
    processClick(clickPoint)
    rpmResponse, speedResponse, fuelResponse = readDash1Values()
