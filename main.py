import pygame
import os
import json
import random

from player import Player
from board import Board

WIDTH, HEIGHT = 1200, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monopoly")
pygame.font.init()
FONT = pygame.font.Font(None, 30) #pygame.font.SysFont('Comic Sans MS', 14)

BLACK = (0, 0, 0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255,180,0)
BUTTON_COLOR = (204, 255, 255)

FPS = 100

CAR_WIDTH, CAR_HEIGHT = 50, 50
START_X, START_Y = 640, 670
BOARD_IMAGE = pygame.image.load(os.path.join('Assets', 'monopoly.jpg'))
CAR = pygame.image.load(os.path.join('Assets', 'car.png'))


board_rect = BOARD_IMAGE.get_rect()
board_rect.center = (BOARD_IMAGE.get_height()/2 + 50, HEIGHT/2)

board = Board()
board.init_locations()
print(*board.properties)


with open('board_data.json') as json_file:
    property_dict = json.load(json_file)
    print("Type: ", type(property_dict))
    print(property_dict["locations"][0])

car = Player("Car", 1500, START_X, START_Y)

class Button :
    def __init__(self, text, fontsize, rect, color):
        self.text = text
        self.rect = rect
        self.color = color
        #buttonfont = pygame.font.SysFont('Comic Sans MS', fontsize)
        self.surface = FONT.render(self.text, True, ORANGE)
        self.text_rect = self.surface.get_rect()
        self.text_rect.center = self.rect.center
        self.clicked = False
        
    def draw(self):
        pygame.draw.rect(WINDOW, self.color, self.rect)
        WINDOW.blit(self.surface, self.text_rect)
    
    def release(self):
        self.clicked = False
    
    def is_clicked(self, event):
        if self.rect.collidepoint(event.pos):
            return True
        return False

class Dice:
    def __init__(self, dice_rect, dice2_rect, color, fontsize):
        self.dice_one = '?'
        self.dice_two = '?'
        self.dice_rect = dice_rect
        self.dice2_rect = dice2_rect
        
        self.color = color
        self.fontsize = fontsize
        
        self.surface = FONT.render(self.dice_one, True, ORANGE)
        self.surface2 = FONT.render(self.dice_two, True, ORANGE)
        
        self.text_rect = self.surface.get_rect()
        self.text_rect.center = self.dice_rect.center
        self.text2_rect = self.surface2.get_rect()
        self.text2_rect.center = self.dice2_rect.center
        
    def roll(self):
        self.dice_one = str(random.randint(1, 6))
        self.dice_two = str(random.randint(1, 6))
        self.surface = FONT.render(self.dice_one, True, ORANGE)
        self.surface2 = FONT.render(self.dice_two, True, ORANGE)
    
    def draw_dice(self):
        pygame.draw.rect(WINDOW, self.color, self.dice_rect, 2)
        pygame.draw.rect(WINDOW, self.color, self.dice2_rect, 2)
        WINDOW.blit(self.surface, self.text_rect)
        WINDOW.blit(self.surface2, self.text2_rect)
    
    def get_rollsum(self):
        return int(self.dice_one) + int(self.dice_two)
    
roll_button = Button('Roll', 30, pygame.Rect(1080, 200, 100, 60), BUTTON_COLOR)
buy_button = Button('Buy', 30, pygame.Rect(1080, 280, 100, 60), BUTTON_COLOR)
die = Dice(pygame.Rect(1100, 50, 60, 60), pygame.Rect(1100, 120, 60, 60), BUTTON_COLOR, 30)

def draw_window():
    WINDOW.fill(BLACK)

    WINDOW.blit(BOARD_IMAGE, board_rect)
    WINDOW.blit(CAR, (car.get_x(), car.get_y()))
    
    #WINDOW.blit(textsurface,(BOARD_IMAGE.get_width() + 100,100)) # drawing player info
    #WINDOW.blit(textsurface2,(BOARD_IMAGE.get_width() + 100,120))
    
    roll_button.draw()
    die.draw_dice()
    buy_button.draw()
    
    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    
                    if roll_button.is_clicked(event):
                        die.roll()
                        car.move(die.get_rollsum())
                        roll_button.release()
                        
                    elif buy_button.is_clicked(event):
                        car.add_property(car.get_position())
                        print(car.get_properties())
                        
            elif event.type == pygame.QUIT:
                run = False
              
        draw_window()
        
    pygame.quit()

if __name__ == "__main__":
    main()
