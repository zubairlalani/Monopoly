import pygame
import os
import json
from player import Player
from board import Board

WIDTH, HEIGHT = 1200, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monopoly")

BLACK = (0, 0, 0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255,180,0)

FPS = 60

CAR_WIDTH, CAR_HEIGHT = 50, 50
START_X, START_Y = 680, 670
BOARD_IMAGE = pygame.image.load(os.path.join('Assets', 'monopoly.jpg'))
CAR = pygame.image.load(os.path.join('Assets', 'car.png'))

board_rect = BOARD_IMAGE.get_rect()
board_rect.center = (BOARD_IMAGE.get_height()/2 + 50, HEIGHT/2)

board = Board()
board.init_locations()
print(*board.properties)

car = Player("Car", 1500, START_X, START_Y)
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 14)
textsurface = myfont.render('Player 1: '+car.get_name(), True, WHITE)
textsurface2 = myfont.render('  Wealth: '+str(car.get_money()), True, WHITE)

color_light = (170,170,170) 
roll_dice_text = myfont.render('Roll', True, WHITE)

class Button :
    def __init__(self, text, fontsize, left, top ,width, height, color):
        self.text = text
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        buttonfont = pygame.font.SysFont('Comic Sans MS', fontsize)
        self.surface = buttonfont.render(self.text, True, WHITE)
        self.text_rect = self.surface.get_rect()
        self.text_rect.center = (self.left + self.width/2, self.top + self.height/2)
        
    
    def draw(self) :
        pygame.draw.rect(WINDOW, self.color, pygame.Rect(self.left, self.top, self.width, self.height))
        WINDOW.blit(self.surface, self.text_rect)

roll_button = Button('Roll', 30, 940, 300, 100, 60, RED)

with open('board_data.json') as json_file:
    property_dict = json.load(json_file)
    print("Type: ", type(property_dict))
    
    print(property_dict["locations"][0])
    

def draw_window():
    WINDOW.fill(BLACK)
    
    WINDOW.blit(BOARD_IMAGE, board_rect)
    WINDOW.blit(CAR, (car.get_x(), car.get_y()))
    WINDOW.blit(textsurface,(BOARD_IMAGE.get_width() + 100,100))
    WINDOW.blit(textsurface2,(BOARD_IMAGE.get_width() + 100,120))
    
    pygame.draw.rect(WINDOW, RED, pygame.Rect(900, 200, 60, 60), 2)
    pygame.draw.rect(WINDOW, RED, pygame.Rect(980, 200, 60, 60), 2)
    roll_button.draw()
    
    pygame.display.flip()
    
def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                car.move(1)
            if event.type == pygame.QUIT:
                run = False
                
        draw_window()
        
    pygame.quit()

if __name__ == "__main__":
    main()
