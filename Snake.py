from tkinter import *
import random
import time

def main():
    root = Tk()
    Snake ()
    root.resizable(False, False)
    root.wm_attributes("-topmost", 1)
    root.mainloop()

class Snake (Frame):
    def __init__(self):
        super().__init__()
        self.master.title("Snake")
        self.board = Board()

class konst:
    WIDTH = 600
    HEIGHT = 600
    DELAY = 100
    DOT_SIZE = 20
    MAX_RAND_POS = 29

class Board(Canvas):
    def __init__(self):
        super().__init__(width = konst.WIDTH, height = konst.HEIGHT, background = "black", highlightthickness = 0)
        self.startGame()
        self.pack()

    def startGame(self):
        self.inGame = True
        self.dots = 3
        self.score = 0

        self.moveX = konst.DOT_SIZE
        self.moveY = 0

        self.foodX = 100
        self.foodY = 190

        self.loadImages()
        self.createObjects()

        self.locateFood()

        self.bind_all("<Key>", self.onKeyPressed)

        self.after(konst.DELAY, self.onTimer)        

    def loadImages(self):
        self.food = PhotoImage (file = "food.png")
        self.snake = PhotoImage (file = "snake.png")
    
    def createObjects(self):
        self.create_text(30,10, text = "Score: {0}".format(self.score), tag = "score", fill="white")
        
        self.create_image(self.foodX, self.foodY, image = self.food, anchor = NW, tag = "food")
        
        self.create_image(50, 50, image = self.snake, anchor = NW, tag = "head")
        self.create_image(30, 50, image = self.snake, anchor = NW, tag = "dot")
        self.create_image(40, 50, image = self.snake, anchor = NW, tag = "dot")

    def checkFoodCollision(self):
        food = self.find_withtag("food")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for i in overlap:
            if food[0] == i:
                self.score += 1
                x, y = self.coords(food)
                self.create_image(x, y, image = self.snake, anchor = NW, tag = "dot")
                self.locateFood()

    def locateFood(self):
        food = self.find_withtag("food")
        self.delete(food[0])

        rand = random.randint(0, konst.MAX_RAND_POS)
        self.foodX = rand * konst.DOT_SIZE
        rand = random.randint(0, konst.MAX_RAND_POS)
        self.foodY = rand * konst.DOT_SIZE

        self.create_image (self.foodX, self.foodY, anchor = NW, image = self.food, tag = "food")
    def moveSnake(self):
        head = self.find_withtag("head")
        dots = self.find_withtag("dot")
        items = dots + head

        a = 0
        while a < len (items) - 1:
            c1 = self.coords(items[a])
            c2 = self.coords(items[a + 1])
            self.move(items[a], c2[0] - c1[0], c2[1] - c1[1])
            a += 1
        self.move(head, self.moveX, self.moveY)

    def checkCollision1(self):
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)

        if x1 < 0:
            self.inGame = False
        if x1 > konst.WIDTH - konst.DOT_SIZE:
            self.inGame = False
        if y1 < 0:
            self.inGame = False
        if y1 > konst.HEIGHT - konst.DOT_SIZE:
            self.inGame = False
    
    def checkCollision2(self):
        head = self.find_withtag("head")
        dots = self.find_withtag("dot")      

        x1, y1, x2, y2 = self.bbox(head)
        x1, y1, x2, y2 = x1 + 10, y1 + 10, x2 - 10, y2 - 10
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for i in dots:
            for j in overlap:
                if i == j:
                    self.inGame = False
    
    def onKeyPressed(self, e):
        key = e.keysym
        
        LeftKey = "Left"
        if key == LeftKey and self.moveX <= 0:
            self.moveX = - konst.DOT_SIZE
            self.moveY = 0
        
        RightKey = "Right"
        if key == RightKey and self.moveX >= 0:
            self.moveX = konst.DOT_SIZE
            self.moveY = 0
        
        UpKey = "Up"
        if key == UpKey and self.moveY <= 0:
            self.moveX = 0
            self.moveY = - konst.DOT_SIZE
        
        DownKey = "Down"
        if key == DownKey and self.moveY >= 0:
            self.moveX = 0
            self.moveY = konst.DOT_SIZE
    
    def onTimer(self):
        self.drawScore()
        self.checkCollision1()
        self.checkCollision2()

        if self.inGame == True:
            self.checkFoodCollision()
            self.moveSnake()
            self.after(konst.DELAY, self.onTimer)
        else:
            self.gameOver()
    
    def drawScore(self):
        score = self.find_withtag("score")
        self.itemconfigure(score, text = "Score: {0}".format(self.score))
    
    def gameOver(self):
        self.delete(ALL)
        self.create_text(self.winfo_width()/2, self.winfo_height()/2, text = "Game over with score {0}".format(self.score), fill = "white")
        self.bind_all("<Key>", self.onKeyPressed2)
    
    def onKeyPressed2(self, e):
        key = e.keysym
        LeftKey = "Left"
        RightKey = "Right"
        UpKey = "Up"
        DownKey = "Down"

        if key == LeftKey or key == RightKey or key == UpKey or key == DownKey :
            self.destroy()
            Snake()
main()




