import pygame
import os
import json
from player import Player
from board import Board

WIDTH, HEIGHT = 1200, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monopoly")

BLACK = (0, 0, 0)
Color_line = (255, 0, 0)
FPS = 60

CAR_WIDTH, CAR_HEIGHT = 50, 50
START_X, START_Y = 680, 670
BOARD_IMAGE = pygame.image.load(os.path.join('Assets', 'monopoly.jpg'))
CAR = pygame.image.load(os.path.join('Assets', 'car.png'))
#CAR = pygame.transform.scale(CAR, (CAR_WIDTH, CAR_HEIGHT))
#BOARD_IMAGE = pygame.transform.scale(BOARD_IMAGE, (680, 680))
rect = BOARD_IMAGE.get_rect()
rect.center = (BOARD_IMAGE.get_height()/2 + 50, HEIGHT/2)

board = Board()
board.init_locations()
print(*board.properties)

car = Player("Car", 1500, START_X, START_Y)
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 14)
textsurface = myfont.render('Player 1: '+car.get_name(), False, (255, 255, 255))
textsurface2 = myfont.render('  Wealth: '+str(car.get_money()), False, (255, 255, 255))

with open('board_data.json') as json_file:
    property_dict = json.load(json_file)
    print("Type: ", type(property_dict))
    
    print(property_dict["locations"][0])
    

def draw_window():
    WINDOW.fill(BLACK)
    
    WINDOW.blit(BOARD_IMAGE, rect)
    WINDOW.blit(CAR, (car.get_x(), car.get_y()))
    
    '''
    pygame.draw.line(WINDOW, Color_line, (0, 740), (900, 740))
    pygame.draw.line(WINDOW, Color_line, (100, 0), (100, 800))
    pygame.draw.line(WINDOW, Color_line, (800, 0), (800, 800))
    pygame.draw.line(WINDOW, Color_line, (0, 50), (900, 50))
    '''
    
    WINDOW.blit(textsurface,(BOARD_IMAGE.get_width() + 100,100))
    WINDOW.blit(textsurface2,(BOARD_IMAGE.get_width() + 100,120))
    
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
