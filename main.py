import pygame
import os
import json
import random

from player import Player
from board import Board
import pygame_textinput
import option_box as ob

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
properties = dict({
                1 : pygame.image.load(os.path.join('Assets', 'mediterranean_avenue.png')),
                3 : pygame.image.load(os.path.join('Assets', 'baltic_avenue.jpg')),
                5 : pygame.image.load(os.path.join('Assets', 'reading_railroad.jpg')),
                6 : pygame.image.load(os.path.join('Assets', 'oriental_avenue.jpg')),
                8 : pygame.image.load(os.path.join('Assets', 'vermont_avenue.jpg')),
                9 : pygame.image.load(os.path.join('Assets', 'connecticut_avenue.jpg')),
                11 : pygame.image.load(os.path.join('Assets', 'st_charles_place.jpg')),
                12 : pygame.image.load(os.path.join('Assets', 'electric_company.jpg')),
                13 : pygame.image.load(os.path.join('Assets', 'states_avenue.jpg')),
                14 : pygame.image.load(os.path.join('Assets', 'virginia_avenue.jpg')),
                15 : pygame.image.load(os.path.join('Assets', 'pennsylvania_railroad.jpg')),
                16 : pygame.image.load(os.path.join('Assets', 'st_james_place.jpg')),
                18 : pygame.image.load(os.path.join('Assets', 'tennessee_avenue.jpg')),
                19 : pygame.image.load(os.path.join('Assets', 'new_york_avenue.jpg')),
                21 : pygame.image.load(os.path.join('Assets', 'kentucky_avenue.jpg')),
                23 : pygame.image.load(os.path.join('Assets', 'indiana_avenue.jpg')),
                24 : pygame.image.load(os.path.join('Assets', 'illinois_avenue.jpg')),
                25 : pygame.image.load(os.path.join('Assets', 'b&o_railroad.jpg')),
                26 : pygame.image.load(os.path.join('Assets', 'atlantic_avenue.jpg')),
                27 : pygame.image.load(os.path.join('Assets', 'ventnor_avenue.jpg')),
                28 : pygame.image.load(os.path.join('Assets', 'water_works.jpg')),
                29 : pygame.image.load(os.path.join('Assets', 'marvin_gardens.jpg')),
                31 : pygame.image.load(os.path.join('Assets', 'pacific_avenue.jpg')),
                32 : pygame.image.load(os.path.join('Assets', 'north_carolina_avenue.jpg')),
                34 : pygame.image.load(os.path.join('Assets', 'pennsylvania_avenue.jpg')),
                35 : pygame.image.load(os.path.join('Assets', 'short_line_railroad.jpg')),
                37 : pygame.image.load(os.path.join('Assets', 'park_place.jpg')),
                39 : pygame.image.load(os.path.join('Assets', 'boardwalk.jpg')),
            })


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

class Button:
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
        pygame.draw.rect(WINDOW, self.color, self.rect, border_radius=10)
        WINDOW.blit(self.surface, self.text_rect)
    
    def release(self):
        self.clicked = False
    
    def is_clicked(self, event):
        if self.rect.collidepoint(event.pos):
            return True
        return False
        
class TextBox(Button):
    def __init__(self, text, fontsize, textcolor, boxcolor, rect, mode):
        self.text = text
        self.rect = rect
        self.fontsize = fontsize
        self.textcolor = textcolor
        self.boxcolor = boxcolor
        self.mode = mode
        
        self.surface = FONT.render(self.text, True, ORANGE)
        self.text_rect = self.surface.get_rect()
        self.text_rect.center = self.rect.center
        self.clicked = False
    
    def draw(self):
        pygame.draw.rect(WINDOW, self.boxcolor, self.rect, 2)
        WINDOW.blit(self.surface, self.text_rect)
    
    def update_text(self, text):
        self.surface = FONT.render(text, True, self.textcolor)
    
    def toggle(self, state):
        self.clicked = state
    
    def is_active(self):
        return self.clicked
    
    def get_rect(self):
        return self.rect
    
        
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
trade_button = Button("Trade", 30, pygame.Rect(1080, 360, 100, 60), BUTTON_COLOR)
build_button = Button("Build", 30, pygame.Rect(1080, 440, 100, 60), BUTTON_COLOR)
end_turn_button = Button("End Turn", 30, pygame.Rect(1080, 520, 100, 60), BUTTON_COLOR)
trade_box = TextBox("", 12, WHITE, BUTTON_COLOR, pygame.Rect(950, 370, 110, 30), True)
trade_box2 = TextBox("", 12, WHITE, BUTTON_COLOR, pygame.Rect(760, 370, 110, 30), True)
textbox = pygame_textinput.TextInput("", font_size=20, text_color=WHITE, cursor_color=ORANGE)
textbox2 = pygame_textinput.TextInput("", font_size=20, text_color=WHITE, cursor_color=ORANGE)
player_option = ob.OptionBox(
    760, 435, 310, 30, (150, 150, 150), (100, 200, 255), FONT, 
    ["Car", "Ship", "Shoe"])

die = Dice(pygame.Rect(1100, 50, 60, 60), pygame.Rect(1100, 120, 60, 60), BUTTON_COLOR, 30)


def draw_text(text, x, y):
    text_surface = FONT.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    WINDOW.blit(text_surface, text_rect)

# drawings two sided arrow for trading
arrow_offset_x = 900
arrow_offset_y = 365
arrowscale = 8

def draw_player_info():
    pygame.draw.rect(WINDOW, WHITE, (760, 435, 310, 300), 2)
    #pygame.draw.line(WINDOW, WHITE, (760, 435+75), (760+420, 435+75), width=2)
    #pygame.draw.line(WINDOW, WHITE, (760, 435+75+75), (760+420, 435+75+75), width=2)
    #pygame.draw.line(WINDOW, WHITE, (760, 435+75+75+75), (760+420, 435+75+75+75), width=2)
    
def draw_window():
    WINDOW.fill(BLACK)

    WINDOW.blit(BOARD_IMAGE, board_rect)
    WINDOW.blit(CAR, (car.get_x(), car.get_y()))
    
    
    roll_button.draw()
    die.draw_dice()
    buy_button.draw()
    trade_button.draw()
    build_button.draw()
    end_turn_button.draw()
    player_option.draw(WINDOW)
    
    #trade_box.draw()
    #trade_box2.draw()
    
    WINDOW.blit(textbox.get_surface(), (950, 400 - textbox.get_fontsize()))
    WINDOW.blit(textbox2.get_surface(), (760, 400 - textbox2.get_fontsize()))
    if car.get_position() in properties:
        WINDOW.blit(properties[car.get_position()], (775, 60))
    
    pygame.draw.polygon(WINDOW, WHITE, 
                        (
                         (arrow_offset_x, 100/arrowscale + arrow_offset_y), (arrow_offset_x, arrow_offset_y), 
                         (-100/arrowscale + arrow_offset_x, 150/arrowscale + arrow_offset_y), 
                         (arrow_offset_x, 300/arrowscale + arrow_offset_y), 
                         (arrow_offset_x, 200/arrowscale+ arrow_offset_y), 
                         (200/arrowscale+arrow_offset_x, 200/arrowscale + arrow_offset_y), 
                         (200/arrowscale+arrow_offset_x, 300/arrowscale + arrow_offset_y), 
                         (300/arrowscale +arrow_offset_x, 150/arrowscale + arrow_offset_y), 
                         (200/arrowscale + arrow_offset_x, 0+ arrow_offset_y), 
                         (200/arrowscale+arrow_offset_x, 100/arrowscale+ arrow_offset_y)))
    pygame.draw.line(WINDOW, WHITE, (950, 400), (950+115, 400), width=4)
    pygame.draw.line(WINDOW, WHITE, (760, 400), (760+115, 400), width=4)
    
    draw_player_info()
    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    run = True
    
    while run:
        clock.tick(FPS)
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    
                    if roll_button.is_clicked(event):
                        die.roll()
                        car.move(die.get_rollsum())
                        roll_button.release()
                        
                    elif buy_button.is_clicked(event):
                        loc = property_dict["locations"][car.get_position()]["name"]
                        if loc != "GO" \
                        and loc != "Community Chest" and loc != "Chance" \
                        and loc != "Tax" and loc != "Jail" and loc != "Free Parking" and loc != "Cop":
                            car.buy_property(car.get_position(), property_dict["locations"][car.get_position()]["cost"])
                    elif trade_box.is_clicked(event):
                        trade_box.toggle(True)
                    elif trade_box2.is_clicked(event):
                        trade_box2.toggle(True)  
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if trade_box.is_active():
                        trade_box.toggle(False)
                    elif trade_box2.is_active():
                        trade_box2.toggle(False)
                    
            elif event.type == pygame.QUIT:
                run = False
        
        if trade_box.is_active():
            textbox.update(events)
        elif trade_box2.is_active():
            textbox2.update(events)
        
        selected_option = player_option.update(events)
        if selected_option >= 0:
            print(selected_option)
            
        draw_window()
        
    pygame.quit()

if __name__ == "__main__":
    main()