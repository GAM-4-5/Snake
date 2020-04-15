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
    WIDTH = 700
    HEIGHT = 600
    DELAY = 100
    DOT_SIZE = 10
    MAX_RAND_POS = 27

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
        

    def loadImages(self):
        self.food = PhotoImage (file = "food.png")
        self.snake = PhotoImage (file = "snake.png")
    
    def createObjects(self):
        self.create_text(30,10, text = "Score: {0}".format(self.score), tag = "score", fill="white")
        self.create_image(self.foodX, self.foodY, image = self.food, anchor = NW, tag = "food")
        self.create_image(50, 50, image = self.snake, anchor = NW, tag = "head")
        self.create_image(30, 50, image = self.snake, anchor = NW, tag = "dot")
        self.create_image(40, 50, image = self.snake, anchor = NW, tag = "dot")


main()




