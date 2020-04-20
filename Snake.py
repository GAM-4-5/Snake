from tkinter import *
import random
import time


def main(): ##Glavna naredba preko koje se pokrene igrica
    root = Tk()
    Snake () ##pozvana klasa koja opisuje kako da se napravi taj prozor
    root.resizable(False, False) ##onemugućavanje mijenjenje veličine prozora
    root.wm_attributes("-topmost", 1)
    root.mainloop()

class Snake (Frame): ##opisana klasa Snake 
    def __init__(self):
        super().__init__()
        self.master.title("Snake")
        self.board = Board() ##pozvana funkcija koja crta prozor sa svim karakteristikama

class konst: ##konstante koje su napravljenje za lako mijenjanje važnih veličina u igrici
    WIDTH = 600
    HEIGHT = 600
    DELAY = 100
    DOT_SIZE = 20
    MAX_RAND_POS = 29
    
class Board(Canvas): ##opisana funkcija board
    def __init__(self):
        super().__init__(width = konst.WIDTH, height = konst.HEIGHT, background = "black", highlightthickness = 0)
        self.startGame() ##pozvana funkcija koja pokreće samu igricu
        self.pack()

    def startGame(self): ## opisane osnovne karakteristike igrice
        self.inGame = True ## naredba s kojom možemo kasnije pokrenuti Game over
        self.dots = 3 ##veličina zmije
        self.score = 0 ##postavljanje našeg scorea

        self.moveX = konst.DOT_SIZE ##početni smjer kretanja zmije
        self.moveY = 0

        self.foodX = 100 ##početna pozicija prve mrvice hrane
        self.foodY = 190

        self.loadImages() ##pozvana fun za učitavanje slika za zmiju i za hranu
        self.createObjects() ##pozvana fun za crtanje tih slika

        self.bind_all("<Key>", self.onKeyPressed) ##bind za tipke za kretanje

        self.after(konst.DELAY, self.onTimer)  ##timer nakon kojeg se počinju promatrati kolizije      

    def loadImages(self): ##opisana funkcija za učitavanje slika
        self.food = PhotoImage (file = "food.png")
        self.snake = PhotoImage (file = "snake.png")
    
    def createObjects(self): ##opisana funkcija za ucčitavanje slika i teksta
        self.create_text(30,10, text = "Score: {0}".format(self.score), tag = "score", fill="white")
        self.create_image(self.foodX, self.foodY, image = self.food, anchor = NW, tag = "food")
        
        self.create_image(50, 50, image = self.snake, anchor = NW, tag = "head")
        self.create_image(30, 50, image = self.snake, anchor = NW, tag = "dot")
        self.create_image(40, 50, image = self.snake, anchor = NW, tag = "dot")

    def checkFoodCollision(self): ##promatranje jeli pozicija glave bila na istoj poziciji kao i hrana - tj jeli zmija pojela komadić hrane
        food = self.find_withtag("food")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head) ##naredba koja gleda jesu li pozicije glave i hrane bile iste
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for i in overlap:
            if food[0] == i:
                self.score += 1
                x, y = self.coords(food)
                self.create_image(x, y, image = self.snake, anchor = NW, tag = "dot") ##crta se produljenje zmije
                self.locateFood() ## poziva se funkcija koja crta novu hranu

    def locateFood(self): ##opisna fun koja crta novu hranu
        food = self.find_withtag("food")
        self.delete(food[0])

        rand = random.randint(0, konst.MAX_RAND_POS) ##randomiziranje poz stvaranje hrane
        self.foodX = rand * konst.DOT_SIZE
        rand = random.randint(0, konst.MAX_RAND_POS)
        self.foodY = rand * konst.DOT_SIZE

        self.create_image (self.foodX, self.foodY, anchor = NW, image = self.food, tag = "food")

    def moveSnake(self): ##funkcija koja pokreće zmiju
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

    def checkCollision1(self):  ##funkcija koja provjerava kolizije zmije s rubom polja
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)

        if x1 < 0:
            self.inGame = False   ##pokreće se game over
        if x1 > konst.WIDTH - konst.DOT_SIZE:
            self.inGame = False
        if y1 < 0:
            self.inGame = False
        if y1 > konst.HEIGHT - konst.DOT_SIZE:
            self.inGame = False
    
    def checkCollision2(self): ##funkcija koja provjerava kolizije zmije s samom sobom
        head = self.find_withtag("head")
        dots = self.find_withtag("dot")      

        x1, y1, x2, y2 = self.bbox(head)
        x1, y1, x2, y2 = x1 + 10, y1 + 10 , x2 - 10, y2 - 10 
        
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for i in dots:
            for j in overlap:
                if i == j:
                    self.inGame = False
    
    def onKeyPressed(self, e): ##funkcija koja omogućava pokretanje zmije pomoći tipki
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
    
    def onTimer(self): ##timer koji tek naknadno pokreće provjeravanje kolizija
        self.drawScore()
        self.checkCollision1()
        self.checkCollision2()
       

        if self.inGame == True:
            self.checkFoodCollision()
            self.moveSnake()
            self.after(konst.DELAY, self.onTimer)
        else:
            self.gameOver()     ##ako je inGame == 0 onda se pokreće game over
    
    def drawScore(self):  ##crtanje Scorea
        score = self.find_withtag("score")
        self.itemconfigure(score, text = "Score: {0}".format(self.score))
        
    
    def gameOver(self): ##zaustavljanje igrice te omogućavanje ponovnog pokretanja igrice
        self.delete(ALL)
        self.create_text(self.winfo_width()/2, self.winfo_height()/2, text = "Game over with score {0}, to play again press any of the arrow keys.".format(self.score), fill = "white")     
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


def mainMenu(): ##funkcija koja pokreće Main Menu
    rootM = Tk()
    MenuStyle()
    rootM.resizable(False, False)
    rootM.wm_attributes("-topmost", 1)
    rootM.mainloop()

class MenuStyle (Frame):  ##klase koje opisuju Main Menu
    def __init__(self):
        super().__init__()
        self.master.title("Main Menu")
        self.board = Board2()

class Board2(Canvas):
    def __init__(self):
        super().__init__(width = konst.WIDTH, height = konst.HEIGHT, background = "black", highlightthickness = 0)
        self.pack()
        self.bind_all("<Key>", self.onKeyPressed3)
        self.createObjects2()

    def createObjects2(self):     ##pisanje teksta 
        self.create_text(300, 300, text = "Welcome to the game of Snake, if you want to start playing press any of the arrow keys.", fill = "white")
    
    def onKeyPressed3(self, e): ##omogućavanje da se pokrene igrica
        key = e.keysym
        LeftKey = "Left"
        RightKey = "Right"
        UpKey = "Up"
        DownKey = "Down"

        if key == LeftKey or key == RightKey or key == UpKey or key == DownKey :
            self.destroy()
            main()

mainMenu() ##pozivanje funkcije koja pokreće cijeli program