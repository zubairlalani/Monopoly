import pygame
import os
import json
import random

from player import Player
from board import Board
import pygame_textinput
import option_box as ob
import gui_components as gui

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
    
roll_button = gui.Button(WINDOW, 'Roll', FONT, 30, ORANGE, pygame.Rect(1080, 200, 100, 60), BUTTON_COLOR)
buy_button = gui.Button(WINDOW, 'Buy', FONT, 30, ORANGE, pygame.Rect(1080, 280, 100, 60), BUTTON_COLOR)
trade_button = gui.Button(WINDOW, "Trade", FONT, 30, ORANGE, pygame.Rect(1080, 360, 100, 60), BUTTON_COLOR)
build_button = gui.Button(WINDOW, "Build", FONT, 30, ORANGE, pygame.Rect(1080, 440, 100, 60), BUTTON_COLOR)
mortgage_button = gui.Button(WINDOW, "Mortgage", FONT, 30, ORANGE, pygame.Rect(1080, 520, 100, 60), BUTTON_COLOR)
analysis_button = gui.Button(WINDOW, "Analysis", FONT, 30, ORANGE, pygame.Rect(1080, 600, 100, 60), BUTTON_COLOR)
end_turn_button = gui.Button(WINDOW, "End Turn", FONT, 30, ORANGE, pygame.Rect(1080, 680, 100, 60), BUTTON_COLOR)
textbox = pygame_textinput.TextInput("", font_size=20, text_color=WHITE, cursor_color=ORANGE, max_string_length=18, rect=pygame.Rect(950, 370, 110, 30))
textbox2 = pygame_textinput.TextInput("", font_size=20, text_color=WHITE, cursor_color=ORANGE, max_string_length=18, rect=pygame.Rect(760, 370, 110, 30))
player_option = ob.OptionBox(
    760, 435, 310, 30, (150, 150, 150), (100, 200, 255), FONT, 
    ["Car", "Ship", "Shoe"])

die = Dice(pygame.Rect(1100, 50, 60, 60), pygame.Rect(1100, 120, 60, 60), BUTTON_COLOR, 30)


def draw_text(text, x, y):
    text_surface = FONT.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    WINDOW.blit(text_surface, text_rect)

# drawings two sided arrow for trading
arrow_offset_x = 900
arrow_offset_y = 365
arrowscale = 8

def draw_player_info(selected_option):
    info_rect = pygame.Rect(760, 435, 310, 300)
    pygame.draw.rect(WINDOW, WHITE, info_rect, 2)
    if selected_option == 0:
        draw_text("Wealth: $"+str(car.get_money()), info_rect.left, 475)
        draw_text("Properties: ", info_rect.left, 510)

     
def draw(selected_option):
    WINDOW.fill(BLACK)

    WINDOW.blit(BOARD_IMAGE, board_rect)
    WINDOW.blit(CAR, (car.get_x(), car.get_y()))
    
    draw_player_info(selected_option)
    draw_widgets()
    
    if car.get_position() in properties:
        WINDOW.blit(properties[car.get_position()], (775, 60))
    
    draw_trading_area()
    

def draw_widgets():
    roll_button.draw()
    die.draw_dice()
    buy_button.draw()
    trade_button.draw()
    build_button.draw()
    mortgage_button.draw()
    analysis_button.draw()
    end_turn_button.draw()
    WINDOW.blit(textbox.get_surface(), (950, 400 - textbox.get_fontsize()))
    WINDOW.blit(textbox2.get_surface(), (760, 400 - textbox2.get_fontsize()))
    player_option.draw(WINDOW)

def draw_trading_area():
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
    
def main():
    clock = pygame.time.Clock()
    run = True
    first = True
    current_option = -1
    
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
                    
                    elif textbox.is_clicked(event):
                        textbox.set_enabled(True)
                        
                    elif textbox2.is_clicked(event):
                        textbox2.set_enabled(True)  
                    
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if textbox.is_enabled():
                        textbox.set_enabled(False)
                    elif textbox2.is_enabled():
                        textbox2.set_enabled(False)
                    
            elif event.type == pygame.QUIT:
                run = False
        
        if textbox.is_enabled():
            textbox.update(events)
        elif textbox2.is_enabled():
            textbox2.update(events)
        
        selected_option = player_option.update(events)
        if selected_option == -1: # When the previous option is an actual option (not -1) it keeps selected_option as the previous option
            selected_option = current_option
        if selected_option != -1:
            current_option = selected_option
        
        draw(selected_option)
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    main()