
from tkinter import *
import random
import copy

class Background(object):
    def __init__(self):
        self.grass = PhotoImage(file="grass.gif")

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
        self.setStartPoint(data)

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
            elif collisionType(data,data.x1,data.y1-10)=="hole":
                data.y1-=10
                data.gameOverP1=True
        if event.keysym=="Down":
            if isLegal(data,data.x1,data.y1+10):
                data.y1+=10
            elif collisionType(data,data.x1,data.y1+10)=="tent": 
                data.y1+=10
            elif collisionType(data,data.x1,data.y1+10)=="hole":
                data.y1+=10
                data.gameOverP1=True
        if event.keysym=="Left":
            if isLegal(data,data.x1-10,data.y1):
                data.x1-=10
            elif collisionType(data,data.x1-10,data.y1)=="tent":
                data.x1-=10
            elif collisionType(data,data.x1-10,data.y1)=="hole":
                data.x1-=10
                data.gameOverP1=True
        if event.keysym=="Right":
            if isLegal(data,data.x1+10,data.y1):
                data.x1+=10
            elif collisionType(data,data.x1+10,data.y1)=="tent":
                data.x1+=10
            elif collisionType(data,data.x1+10,data.y1)=="hole":
                data.x1+=10
                data.gameOverP1=True 
        if event.keysym=="period":
            Bomb().placeBomb(1,data.x1,data.y1,data)

class Player2(object):
    def __init__(self,data):     
        self.setStartPoint(data)

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
            elif collisionType(data,data.x2,data.y2-10)=="hole":
                data.y2-=10
                data.gameOverP2=True
        if event.keysym=="f":
            if isLegal(data,data.x2,data.y2+10):
                data.y2+=10
            elif collisionType(data,data.x2,data.y2+10)=="tent": 
                data.y2+=10
            elif collisionType(data,data.x2,data.y2+10)=="hole":
                data.y2+=10
                data.gameOverP2=True
        if event.keysym=="d":
            if isLegal(data,data.x2-10,data.y2):
                data.x2-=10
            elif collisionType(data,data.x2-10,data.y2)=="tent":
                data.x2-=10
            elif collisionType(data,data.x2-10,data.y2)=="hole":
                data.x2-=10
                data.gameOverP2=True
        if event.keysym=="g":
            if isLegal(data,data.x2+10,data.y2):
                data.x2+=10
            elif collisionType(data,data.x2+10,data.y2)=="tent": 
                data.x2+=10
            elif collisionType(data,data.x2+10,data.y2)=="hole":
                data.x2+=10
                data.gameOverP2=True
        if event.keysym=="z":
            Bomb().placeBomb(2,data.x2,data.y2,data)

class Bomb(object):
    def __init__(self):
        self.imageBomb=[PhotoImage(file="bomb1.gif"),PhotoImage(file="bomb2.gif")]
        self.imageBubble=PhotoImage(file="bubble.gif")
        self.pop=False

    def placeBomb(self,player,x,y,data):
        (row,col)=Cell(data).getCell(x,y,data)
        p=Cell(data).getCellBounds(row,col)
        x=(p[0]+p[2])//2
        y=(p[1]+p[3])//2
        data.bombList.append((x,y))
        data.time.append(0)
        data.bombPlayer.append(player)


    def draw(self,canvas,data):
        if len(data.bombList)>0:
            for i in range (len(data.bombList)):
                j=data.time[i]%2
                canvas.create_image(data.bombList[i],image=self.imageBomb[j])
        if self.pop==True:
            self.drawBubble(canvas,data)
            self.pop=False
            self.delete(data)

    def timerFired(self,data,canvas):
        for i in range (len(data.time)):
            data.time[i]+=1 
        for j in range (len(data.time)):
            if data.time[j]==15:
                data.time[j]=-1
                self.pop=True
                data.bombListCopy=copy.copy(data.bombList)
                data.bombPlayerCopy=copy.copy(data.bombList)
                # self.drawBubble(canvas,data)
                # self.delete(data)
                self.gameOver(data.bombPlayer[j],data)
        k=0
        while -1 in data.time:
            data.time.remove(-1)
            data.bombList.pop(k)
            data.bombPlayer.pop(k)
            k+=1


    def drawBubble(self,canvas,data):
        size=data.strengthP1 if data.bombPlayerCopy[0]==1 else data.strengthP2
        place=data.bombListCopy[0]
        gap=data.width/data.rows
        for i in range (-size,size+1):
            if place[0]+i*gap<data.width and place[0]+i*gap>0:
                canvas.create_image((place[0]+i*gap,place[1]),image=self.imageBubble)
            if place[1]+i*gap<data.height and place[0]+i*gap>0:
                canvas.create_image((place[0],place[1]+i*gap),image=self.imageBubble)

    def delete(self,data):
        size=data.strengthP1 if data.bombPlayerCopy[0]==1 else data.strengthP2
        place=Cell(data).getCell(data.bombListCopy[0][0],data.bombListCopy[0][1],data)
        for i in range (-size,size+1):
            if place[0]+i<data.rows and place[0]+i>=0:
                row=place[0]+i
                col=place[1]
                if data.typeBoard[row][col]!="rock":
                    data.typeBoard[row][col]=None
                    data.board[row][col]=None
            if place[1]+i<data.cols and place[1]+i>=0:
                row=place[0]
                col=place[1]+i
                if data.typeBoard[row][col]!="rock":
                    data.typeBoard[row][col]=None
                    data.board[row][col]=None

    def gameOver(self,player,data):
        (row1,col1)=Cell(data).getCell(data.x1,data.y1,data)
        (row2,col2)=Cell(data).getCell(data.x2,data.y2,data)
        size=data.strengthP1 if data.bombPlayerCopy[0]==1 else data.strengthP2
        place=Cell(data).getCell(data.bombListCopy[0][0],data.bombListCopy[0][1],data)
        for i in range (-size,size+1):
            if place[0]+i<data.rows and place[0]+i>=0:
                row=place[0]+i
                col=place[1]
                if (row1,col1)==(row,col):
                    data.gameOverP1=True
                if (row2,col2)==(row,col):
                    data.gameOverP2=True
            if place[1]+i<data.cols and place[1]+i>=0:
                row=place[0]
                col=place[1]+i
                if (row1,col1)==(row,col):
                    data.gameOverP1=True
                if (row2,col2)==(row,col):
                    data.gameOverP2=True 


def init(data):
    data.rows=10
    data.cols=10
    data.start=True
    data.board=[[None]*data.cols for i in range (data.rows)]
    data.typeBoard=[[None]*data.cols for i in range (data.rows)]
    data.bombList=[]
    data.bombListCopy=[]
    data.time=[]
    data.bombPlayer=[]
    data.bombPlayerCopy=[]
    data.strengthP2=1
    data.strengthP1=1
    data.gameOverP1=False
    data.gameOverP2=False
    data.background=Background()
    data.player1=Player1(data)
    data.player2=Player2(data)
    data.obstacle=Obstacle(data)
    data.bomb=Bomb()



def isLegal(data,x,y):
    if x<0 or x>data.width or y<0 or y>data.height:
        return False
    (row,col)=Cell(data).getCell(x,y,data)
    if data.board[row][col]!=None:
        return False
    # L=[]
    # for i in data.bombList:
    #     L.append(Cell(data).getCell(i[0],i[1],data))
    # if (row,col) in L:
    #     return False
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
    data.player1.keyPressed(event,data)
    data.player2.keyPressed(event,data)

def timerFired(data,canvas):
    if data.gameOverP1==False and data.gameOverP2==False:
        data.bomb.timerFired(data,canvas)

####################################
# draw functions
####################################

def redrawAll(canvas, data):
    if data.gameOverP1==False and data.gameOverP2==False:
        data.background.draw(canvas)
        data.player1.draw(canvas,data)
        data.player2.draw(canvas,data)
        data.obstacle.draw(canvas,data)
        data.bomb.draw(canvas,data)
    if data.gameOverP1==True:
        canvas.create_text(data.width/2,data.height/2,text="P2 Win",font="Heltivia 40",fill="red")
    if data.gameOverP2==True:
        canvas.create_text(data.width/2,data.height/2,text="P1 Win",font="Heltivia 40",fill="red")


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
        timerFired(data,canvas)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init

    root = Tk()
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas

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