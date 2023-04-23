import socket
from tkinter import *
from  threading import Thread
import random
from PIL import ImageTk


screen_width = None
screen_height = None

SERVER = None
PORT  = 8000
IP_ADDRESS = '127.0.0.1'
playerName = None

canvas1 = None
canvas2 = None

nameEntry = None
nameWindow = None
gameWindow = None

ticketGrid  = []
currentNumberList = []
flashNumberList = []
flashNumberLabel = None


def createTicket():
    global gameWindow
    global ticketG
    
    mianLable = Label(gameWindow, width=75, height=16,relief='ridge', borderwidth=5, bg='white')
    mianLable.place(x=screen_width/2-130, y=screen_height/2-100)

    xPos = screen_width/2-200
    yPos = screen_height/2-150
    for row in range(0, 3):
        rowList = []
        for col in range(0, 9):
            boxButton = Button(gameWindow, font=("Chalkboard SE",30), width=3, height=2,borderwidth=5, bg="#fff176")
            boxButton.place(x=xPos, y=yPos)

            rowList.append(boxButton)
            xPos += 64
            
        ticketGrid.append(rowList)
        xPos = screen_width/2-200
        yPos +=82


def placeNumbers():
    global ticketGrid
    global currentNumberList

    for row in range(0,3):
        randomColList = []
        counter = 0
        
        while counter<=4:
            randomCol = random.randint(0,8)
            if(randomCol not in randomColList):
                randomColList.append(randomCol)
                counter+=1



def gamewindow():
    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global flashNumberLabel

    gameWindow = Tk()
    gameWindow.title("Tambola Game")
    gameWindow.attributes('-fullscreen',True)

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas( gameWindow, width = screen_width,height = screen_height)
    canvas2.pack(fill = "both", expand = True)

    canvas2.create_image( 0, 0, image = bg, anchor = "nw")

    canvas2.create_text( screen_width/2,screen_height-200, text = "Tambola Family Fun", font=("Chalkboard SE",50), fill="red")

    createTicket()
    placeNumbers()

    flashNumberLabel = canvas2.create_text(screen_width/2,200, text = "Waiting for other players to join...", font=("Chalkboard SE",30), fill="#3e2723")

    gameWindow.resizable(True, True)
    gameWindow.mainloop()



def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

    gamewindow()



def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow  = Tk()
    nameWindow.title("Tambola Family Fun")
    nameWindow.attributes('-fullscreen',True)


    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas1 = Canvas( nameWindow, width = 500,height = 500)
    canvas1.pack(fill = "both", expand = True)
    
    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/2,screen_height/5, text = "Enter Name", font=("Chalkboard SE",100), fill="#3e2723")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 30), bd=5, bg='white')
    nameEntry.place(x = screen_width/2-180, y=screen_height/2-10 )

    button = Button(nameWindow, text="Join", font=("Chalkboard SE", 30),width=11, command=saveName, height=2, bg="red", bd=3)
    button.place(x = screen_width/2 - 150, y=screen_height/2 + 100)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()





def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    askPlayerName()

setup()