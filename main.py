from tkinter import *
import cv2
from PoseDetection import PoseDetector
from PIL import ImageTk, Image

####################################
# customize these functions
####################################

def set_frame(data, initial=False):
    if(initial):
        data.cap = cv2.VideoCapture(0)

    _, data.img = data.cap.read()
    data.img = cv2.flip(data.img, 1)
    data.rgb = cv2.cvtColor(data.img, cv2.COLOR_BGR2RGB)
    data.imtk = ImageTk.PhotoImage(image=Image.fromarray(data.rgb))

    if(initial):
        data.pose = PoseDetector()
        data.lm = data.pose.findPts(data.rgb)
    else:
        data.lm = data.pose.findPts(data.rgb)

def init(data):
    # load data.xyz as appropriate
    data.w = 1280
    data.h = 720

    set_frame(data, initial=True)

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    set_frame(data, initial=False)

def redrawAll(canvas, data):
    # draw in canvas
    canvas.create_image(0, 0, anchor=NW, image=data.imtk)

    for pt in data.lm:
        canvas.create_oval(pt[0] - 25, pt[1] - 25, pt[0] + 25, pt[1] + 25, fill = '#11a0ed', width = 0)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 0 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1280, 720)
