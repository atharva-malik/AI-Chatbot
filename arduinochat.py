# 1,0,1: Blue, 0,1,1: Green, 0,0.5,0.5: Cyan. 

try:
    from pyfirmata import Arduino, util
except:
    import pip
    pip.main(['install', 'pyfirmata'])
    from pyfirmata import Arduino, util
import time, os

board = Arduino('COM3')

iterator = util.Iterator(board)
iterator.start()

gD11 = board.get_pin('d:11:p')
bD10 = board.get_pin('d:10:p')
rD9 = board.get_pin('d:9:p')
PowerD8 = board.get_pin('d:8:o')

time.sleep(1)
PowerD8.write(1)
def changeColour(r, g, b):
    rD9.write(r)
    gD11.write(g)
    bD10.write(b)

def changeColourSmooth(initialColours, finalColours):
    changeR = finalColours[0] - initialColours[0]
    changeG = finalColours[1] - initialColours[1]
    changeB = finalColours[2] - initialColours[2]
    for i in range(100):
        changeColour(initialColours[0] + changeR * i / 100, initialColours[1] + changeG * i / 100, initialColours[2] + changeB * i / 100)
        time.sleep(0.03)

def changeColourSmoothFast(initialColours, finalColours):
    changeR = finalColours[0] - initialColours[0]
    changeG = finalColours[1] - initialColours[1]
    changeB = finalColours[2] - initialColours[2]
    for i in range(100):
        changeColour(initialColours[0] + changeR * i / 100, initialColours[1] + changeG * i / 100, initialColours[2] + changeB * i / 100)
        time.sleep(0.001)

def backgroundPulse():
    changeColourSmooth([0, 1, 1], [1, 0, 1])
    changeColourSmooth([1, 0, 1], [0, 1, 1])

def listening():
    changeColour(0, 0.5, 0.5)

def talking():
    changeColourSmoothFast([1, 1, 1], [1, 0, 1])
    changeColourSmoothFast([1, 0, 1], [1, 1, 1])


"""
while True:
    bD11.write(float(input("D11P: ")))
    rD10.write(float(input("D10P: ")))
    gD9.write(float(input("D9P: ")))
    PowerD8.write(1)
    time.sleep(3)

time.sleep(1)

while True:
    os.system('cls')
    print(PotA5.read())
    if ButD7.read() == 1:
        LitD13.write(1)
    else:
        LitD13.write(0)
    time.sleep(0.5)
"""