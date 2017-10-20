#Carlos Gonzalez
#cggonzal
#Section C

from tkinter import *
import random

highScore = []
def init(data):
    data.rows = 8
    data.cols = 16
    data.margin = 5
    data.direction = (0, -1)
    loadSnakeBoard(data)
    placeFood(data)
    placePoison(data)
    data.gameOver = False
    data.paused = False
    data.debugMode = False
    data.score = 1
    data.scoreHeight = 80
    data.scoreReturned = False
    data.timerDelay = 100
    data.snakeMove = 0
    data.snakeMove20 = False
    data.wallExists = False

def loadSnakeBoard(data):
    data.board = []
    for row in range(data.rows): data.board += [[0]*data.cols]
    headRow = (len(data.board)) // 2
    headCol = len(data.board[0]) // 2
    data.board[headRow][headCol] = 1
    data.headRow = headRow
    data.headCol = headCol

def mousePressed(event, data):
    if data.paused and event:
        placeWall(event,data)


def keyPressed(event, data):
    if (event.char == "r"): init(data); return
    elif (event.char == "p"): data.paused = not data.paused; return
    elif (event.char == "d"):
        data.debugMode = not data.debugMode
    if (data.gameOver or data.paused): return
    if (event.keysym == "Left"):    data.direction = (0, -1)
    elif (event.keysym == "Right"): data.direction = (0,  1)
    elif (event.keysym == "Up"):    data.direction = (-1, 0)
    elif (event.keysym == "Down"):  data.direction = ( 1, 0)
    takeStep(data)

def timerFired(data):
    if (data.paused): return
    if (data.gameOver):
        if data.snakeMove20 == True and data.scoreReturned == False:
            data.score += 1
        return
    elif data.score == 4:
        data.timerDelay = 35
    takeStep(data)

def placePoison(data):
    row = random.randint(0, data.rows - 1)
    col = random.randint(0, data.cols - 1)
    while data.board[row][col] != 0 and data.board[row][col] != -1:
        row = random.randint(0, data.rows - 1)
        col = random.randint(0, data.cols - 1)
    data.board[row][col] = -2

def takeStep(data):
    if data.wallExists: data.snakeMove += 1
    if data.snakeMove >= 20: data.snakeMove20 = True
    (drow, dcol) = data.direction
    (headRow, headCol) = (data.headRow, data.headCol)
    (newHeadRow, newHeadCol) = (headRow + drow, headCol + dcol)

    if ((newHeadRow < 0) or (newHeadRow >= data.rows) or
        (newHeadCol < 0) or (newHeadCol >= data.cols) or
        data.board[newHeadRow][newHeadCol] > 0):
        data.gameOver = True
    elif data.board[newHeadRow][newHeadCol] == -1:
        # eat food
        data.board[newHeadRow][newHeadCol]= data.board[headRow][headCol] + 1
        (data.headRow, data.headCol) = (newHeadRow, newHeadCol)
        data.score += 1
        placeFood(data)

    elif data.board[newHeadRow][newHeadCol] == -2:
        data.gameOver = True
        data.board[newHeadRow][newHeadCol] = data.board[headRow][headCol] + 1
        (data.headRow, data.headCol) = (newHeadRow, newHeadCol)
        removeTail(data)

    elif data.board[newHeadRow][newHeadCol] == -7:
        data.score -= 1
        if data.score < 1:
            data.gameOver = True
            removeTail(data)

        else:
            data.board[newHeadRow][newHeadCol] = data.board[headRow][headCol] - 1
            (data.headRow, data.headCol) = (newHeadRow, newHeadCol)

    else:
        # didn't eat, so remove old tail (slither forward)
        data.board[newHeadRow][newHeadCol] = data.board[headRow][headCol] + 1
        (data.headRow, data.headCol) = (newHeadRow, newHeadCol)
        removeTail(data)

def placeFood(data):
    row = random.randint(0, data.rows - 1)
    col = random.randint(0, data.cols - 1)
    while data.board[row][col] != 0:
        row = random.randint(0, data.rows - 1)
        col = random.randint(0, data.cols - 1)
    data.board[row][col] = -1

def removeTail(data):
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] > 0:
                data.board[row][col] -= 1

def placeWall(event,data):
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin - data.scoreHeight
    cellWidth = gridWidth / data.cols
    cellHeight = gridHeight / data.rows

    for row in range(data.rows):
        for col in range(data.cols):
            x0 = data.margin + gridWidth * col / data.cols
            x1 = data.margin + gridWidth * (col+1) / data.cols
            y0 = (data.margin + gridHeight * row / data.rows)
            y1 = data.margin + gridHeight * (row+1) / data.rows
            if event.x > x0 and event.x < x1 and event.y > y0 and event.y < y1 and data.board[row][col] != -7:
                data.board[row][col] = -7
                data.wallExists = True
            elif event.x > x0 and event.x < x1 and event.y > y0 and event.y < y1 and data.board[row][col] == -7:
                data.board[row][col] = 0
                data.wallExists = False
                data.snakeMove = 0

def drawBoard(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            drawSnakeCell(canvas, data, row, col)

def getHighScore(data):
    global highScore
    if data.scoreReturned: return
    if len(highScore) < 3:
        highScore.append(data.score) # high scores when less than 3 plays
        highScore.sort()
        data.scoreReturned = True
    elif data.score > highScore[0]: # high scores when greater than 3 plays
        if data.score > highScore[0] and data.score < highScore[1]:
            highScore.insert(0,data.score)
            data.scoreReturned = True

        elif data.score > highScore[1] and data.score < highScore[2]:
            highScore.insert(1,data.score)
            data.scoreReturned = True

        elif data.score > highScore[2]:
            highScore.append(data.score)
            data.scoreReturned = True

    return
def drawSnakeCell(canvas, data, row,col):
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin - data.scoreHeight
    cellWidth = gridWidth / data.cols
    cellHeight = gridHeight / data.rows
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = (data.margin + gridHeight * row / data.rows)
    y1 = data.margin + gridHeight * (row+1) / data.rows

    canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
    if data.board[row][col] > 0:
        # draw snake body
        canvas.create_oval(x0, y0, x1, y1, fill="blue")
    elif data.board[row][col] == -1:
        # draw food
        canvas.create_oval(x0, y0, x1, y1, fill="green")

    elif data.board[row][col] == -2:
        canvas.create_oval(x0, y0, x1, y1, fill="red")

    elif data.board[row][col] == -7:
        canvas.create_rectangle(x0, y0, x1, y1, fill="brown")


    if (data.debugMode):
        canvas.create_text(x0 + cellWidth/2, y0 + cellHeight/2,
                           text=str(data.board[row][col]),
                           font=("Helvatica", 14, "bold"))

def redrawAll(canvas, data):
    global highScore
    drawBoard(canvas, data)

    canvas.create_text(data.width/2, data.height - 3*data.scoreHeight/4, text = "Your score is: " + str(data.score))
    if (data.gameOver):
        getHighScore(data)
    if data.gameOver:
        highScore.sort()
        scores = highScore[len(highScore)-3:]
        if len(highScore) == 2: scores = highScore
        canvas.create_text(data.width/2, data.height - data.scoreHeight/2,text = "Your High scores were: " + str(scores))
        canvas.create_text(data.width/2, data.height/2, text="Game Over!",
                           font=("Helvetica", 32, "bold"))



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
    data.timerDelay = 100 # milliseconds
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

run(600, 600)
