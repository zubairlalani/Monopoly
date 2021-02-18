import socket
import threading
import pickle
import pygame
from player import Player
import time

HEADER = 64
PORT = 5555
SERVER = "192.168.1.214"
#SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind(ADDR)
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection....Server Started!")

connected = set()
idCount = 0

START_X, START_Y = 640, 670 # Starting position of a player
car = Player("Car", 40000, START_X, START_Y, 0)
shoe = Player("Shoe", 40000, START_X, START_Y, 1)
players = [car, shoe]
turn = 0
dice_rolls = ["?", "?", "0"]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    global turn
    
    while True:
        try:
            data = pickle.loads(conn.recv(1024 * 10))
            players[player] = data[0]
            
            if not data:
                print("Disconnected")
                break
            else:        
                if player == 1:
                    reply = players[0]
                    if dice_rolls[2] == str(player):
                        if data[1] != "x":
                            dice_rolls[2] = data[1]
                            print("SWITCHING TURNS: ", dice_rolls[2])
                        dice_rolls[0] = data[2]
                        dice_rolls[1] = data[3] 
                    
                else:
                    reply = players[1]
                    if dice_rolls[2] == str(player):
                        if data[1] != "x":
                            dice_rolls[2] = data[1]
                            print("SWITCHING TURNS: ", dice_rolls[2])
                        dice_rolls[0] = data[2]
                        dice_rolls[1] = data[3]
                  
            rep = [reply, dice_rolls[2], dice_rolls[0], dice_rolls[1]]
            conn.sendall(pickle.dumps(rep))
            
        except:
            break
            
    print("Lost Connection")
    conn.close()
        
currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    
    threading.Thread(target=threaded_client, args=(conn, currentPlayer)).start()
    currentPlayer += 1
    print("Amount of players", currentPlayer)
