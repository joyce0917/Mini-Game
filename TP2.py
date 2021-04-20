
from tkinter import *
import random

class Background(object):
    def __init__(self):
        self.grass = PhotoImage(file="grass.gif")
        self.label= Label(image=self.grass)
        self.label.photo=self.grass
        self.label.pack()
    def draw(self,canvas):
        canvas.create_image(0,0,anchor=NW,image=self.grass)

class Cell(object):
    def __init__(self,data):
        self.width=data.width
        self.height=data.height
        self.rows=data.rows
        self.cols=data.cols
        
    def getCell(self,x,y,data):
        size=self.width/self.cols
        row=int(y//size)
        col=int(x//size)
        return (row,col)

    def getCellBounds(self,row,col):
        # aka "modelToView"s
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        x0 =self.width * col / self.cols
        x1 =self.width * (col+1) / self.cols
        y0 =self.height * row / self.rows
        y1 =self.height * (row+1) / self.rows
        return (x0, y0, x1, y1)


class Obstacle(Cell):
    def __init__(self,data):
        super().__init__(data)
        self.typeImage=[]
        self.setType()
        self.place(data)
        for image in self.typeImage:
            self.label= Label(image=image[1])
            self.label.photo=image[1]
            self.label.pack()

    def setType(self):
        L=["house","house","ant","ant","hole","flower","flower","rock","tent"]
        for pic in L:
            image = "%s.gif" % (pic)
            self.typeImage.append((pic,PhotoImage(file=image)))
    
    def place(self,data):
        if data.start==True:
            for row in range (self.rows):
                for i in range(5):
                    col=random.choice([num for num in range (self.cols)])
                    obs=random.choice(self.typeImage)
                    if self.getCell(data.x1,data.y1,data)!=(row,col) and self.getCell(data.x2,data.y2,data)!=(row,col):
                        data.board[row][col]=obs[1]
                        data.typeBoard[row][col]=obs[0]
            data.start=False

    def drawCell(self,canvas,row,col,data):
        point=(self.getCellBounds(row,col)[0],self.getCellBounds(row,col)[1])
        image=data.board[row][col]
        canvas.create_image(point,anchor=NW,image=image)

    def draw(self,canvas,data):
        # draw grid of cells
        for row in range(self.rows):
            for col in range(self.cols):
                if data.board[row][col]!=None:
                    self.drawCell(canvas,row,col,data)

class Player1(object):
    def __init__(self,data):
        pass

    def setStartPoint(self,data):
        if data.start==True:
            row=random.randint(0,data.rows-1)
            col=random.randint(0,data.cols-1)
            if data.board[row][col]==None:
                p=Cell(data).getCellBounds(row,col)
                data.x1=(p[0]+p[2])//2
                data.y1=(p[1]+p[3])//2
            else:
                self.setStartPoint(data)

    def draw(self,canvas,data):
        canvas.create_oval(data.x1-5,data.y1-5,data.x1+5,data.y1+5,fill="red")

    def keyPressed(self,event, data):
        if event.keysym=="Up":
            if isLegal(data,data.x1,data.y1-10):
                data.y1-=10
            elif collisionType(data,data.x1,data.y1-10)=="tent":
                data.y1-=10
        if event.keysym=="Down":
            if isLegal(data,data.x1,data.y1+10):
                data.y1+=10
            elif collisionType(data,data.x1,data.y1+10)=="tent":
                data.y1+=10
        if event.keysym=="Left":
            if isLegal(data,data.x1-10,data.y1):
                data.x1-=10
            elif collisionType(data,data.x1-10,data.y1)=="tent":
                data.x1-=10
        if event.keysym=="Right":
            if isLegal(data,data.x1+10,data.y1):
                data.x1+=10
            elif collisionType(data,data.x1+10,data.y1)=="tent":
                data.x1+=10
        if event.keysym=="period":
            Bomb().placeBomb(data.x1,data.y1,data)

class Player2(object):
    def __init__(self,data):
        pass

    def setStartPoint(self,data):
        if data.start==True:
            row=random.randint(0,data.rows-1)
            col=random.randint(0,data.cols-1)
            if data.board[row][col]==None:
                p=Cell(data).getCellBounds(row,col)
                data.x2=(p[0]+p[2])//2
                data.y2=(p[1]+p[3])//2
            else:
                self.setStartPoint(data)

    def draw(self,canvas,data):
        canvas.create_oval(data.x2-5,data.y2-5,data.x2+5,data.y2+5,fill="Blue")

    def keyPressed(self,event,data):
        if event.keysym=="r":
            if isLegal(data,data.x2,data.y2-10):
                data.y2-=10
            elif collisionType(data,data.x2,data.y2-10)=="tent":
                data.y2-=10
        if event.keysym=="f":
            if isLegal(data,data.x2,data.y2+10):
                data.y2+=10
            elif collisionType(data,data.x2,data.y2+10)=="tent":
                data.y2+=10
        if event.keysym=="d":
            if isLegal(data,data.x2-10,data.y2):
                data.x2-=10
            elif collisionType(data,data.x2-10,data.y2)=="tent":
                data.x2-=10
        if event.keysym=="g":
            if isLegal(data,data.x2+10,data.y2):
                data.x2+=10
            elif collisionType(data,data.x2+10,data.y2)=="tent":
                data.x2+=10
        if event.keysym=="z":
            Bomb().placeBomb(data.x2,data.y2,data)

class Bomb(object):
    def __init__(self):
        self.imageBomb=[PhotoImage(file="bomb1.gif"),PhotoImage(file="bomb2.gif")]
        for image in self.imageBomb:
            self.label= Label(image=image)
            self.label.photo=image
            self.label.pack()
        self.imageBubble=PhotoImage(file="bubble.gif")
        self.label= Label(image=self.imageBubble)
        self.label.photo=self.imageBubble
        self.label.pack()

    def placeBomb(self,x,y,data):
        (row,col)=Cell(data).getCell(x,y,data)
        p=Cell(data).getCellBounds(row,col)
        x=(p[0]+p[2])//2
        y=(p[1]+p[3])//2
        data.bomb.append((x,y))
        data.time.append(0)

    def draw(self,canvas,data):
        if len(data.bomb)>0:
            for i in range (len(data.bomb)):
                j=data.time[i]%2
                canvas.create_image(data.bomb[i],image=self.imageBomb[j])

    def timerFired(self,data):
        for i in range (len(data.time)):
            data.time[i]+=1 
        for j in range (len(data.time)):
            if data.time[j]==7:
                data.time[j]=-1
        k=0
        while -1 in data.time:
            data.time.remove(-1)
            data.bomb.pop(k)
            k+=1

    # def drawBubble(self,)

def init(data):
    data.rows=10
    data.cols=10
    data.start=True
    data.board=[[None]*data.cols for i in range (data.rows)]
    data.typeBoard=[[None]*data.cols for i in range (data.rows)]
    data.bomb=[]
    data.time=[]
    Player1(data).setStartPoint(data)
    Player2(data).setStartPoint(data)


def isLegal(data,x,y):
    if x<0 or x>data.width or y<0 or y>data.height:
        return False
    (row,col)=Cell(data).getCell(x,y,data)
    if data.board[row][col]!=None:
        return False
    return True

def collisionType(data,x,y):
    if x<0 or x>data.width or y<0 or y>data.height:
        return None
    (row,col)=Cell(data).getCell(x,y,data)
    if data.typeBoard[row][col]!=None:
        return data.typeBoard[row][col]
    return None

####################################
# controllers
####################################

def mousePressed(event, data):
    pass


def keyPressed(event, data):
    Player1(data).keyPressed(event,data)
    Player2(data).keyPressed(event,data)

def timerFired(data):
    Bomb().timerFired(data)

####################################
# draw functions
####################################

def redrawAll(canvas, data):
    Background().draw(canvas)
    Player1(data).draw(canvas,data)
    Player2(data).draw(canvas,data)
    Obstacle(data).draw(canvas,data)
    Bomb().draw(canvas,data)


####################################
# use the run function as-is
####################################

def run(width=700, height=700):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
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
    data.timerDelay = 500 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
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

run()