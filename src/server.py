import socket
import threading
import pickle
import pygame
from player import Player

HEADER = 64
PORT = 5050
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

s.listen()
print("Waiting for a connection....Server Started!")

connected = set()
idCount = 0

START_X, START_Y = 640, 670 # Starting position of a player
car = Player("Car", 40000, START_X, START_Y, 0)
shoe = Player("Shoe", 40000, START_X, START_Y, 1)
players = [car, shoe]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    string_data = False
    while True:
        try:
            data = pickle.loads(conn.recv(2048 * 14))
            if isinstance(data, str):
                string_data = True
                print("RECEIVED: " + data)
            else:
                string_data = False
                players[player] = data
            #turn = conn.recv(4096).decode()
            
            if not data:
                print("Disconnected")
                break
            else:
                if string_data == False:
                    if player == 1:
                        reply = players[0]
                    else:
                        reply = players[1]
                else:
                    reply = "Hello"
                #print("Received: ", data)
                #print("Sending : ", reply)
             
            conn.sendall(pickle.dumps(reply))
            #conn.sendall(str.encode(turn))
            
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
