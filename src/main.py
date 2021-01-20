import pygame
import os
import json
import random

from player import Player
from board import Board
import pygame_textinput
import gui_components as gui

#Setting up pygame
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
FPS = 60
pygame.display.set_caption("Monopoly")
pygame.font.init()

FONT = pygame.font.Font(None, 30)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
LIGHTBLUE = (179, 242, 255)
PINK = (255, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (50, 205, 50)
DARKBLUE = (0, 34, 204)
GREY = (155, 155, 155)

ORANGE = (255, 180, 0)
BUTTON_COLOR = (204, 255, 255)

BOARD_IMAGE = pygame.image.load(os.path.join('Assets', 'monopoly.jpg'))
board_rect = BOARD_IMAGE.get_rect()
board_rect.center = (BOARD_IMAGE.get_height()/2 + 50, WINDOW_HEIGHT/2)

CAR = pygame.image.load(os.path.join('Assets', 'car.png'))
START_X, START_Y = 640, 670 # Starting position of a player

WATER_DROPLET_IMAGE = pygame.image.load(os.path.join('Assets', 'water_droplet.png'))
LIGHTBULB_IMAGE = pygame.image.load(os.path.join('Assets', 'lightbulb.png'))
RAILROAD_IMAGE = pygame.image.load(os.path.join('Assets', 'railroad_icon.jpeg'))
railroad_icon_rect = RAILROAD_IMAGE.get_rect()

#Contains all property images mapped to their respective positions
property_images = dict({
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

with open('src/board_data.json') as json_file:
    property_dict = json.load(json_file) # Contains all info about each property including name, rent, cost, etc

   
class Dice:
    """Represents the die within the monopoly game and handles both drawing and rolling the die
    """
    
    def __init__(self, dice_rect, dice2_rect, color, fontsize):
        """Initialize class variables and the surfaces for drawing the numbers

        Args:
            dice_rect (pygame.Rect): Rectangle that represents the first dice
            dice2_rect (Pygame.Rect): Rectangle that represents the second dice
            color (Tuple): Color that dice will be drawn with
            fontsize (int): Size of the numbers within the rectangles
        """
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
    
roll_button = gui.Button(WINDOW, 'Roll', FONT, ORANGE, pygame.Rect(1080, 200, 100, 60), BUTTON_COLOR)
buy_button = gui.Button(WINDOW, 'Buy', FONT, ORANGE, pygame.Rect(1080, 280, 100, 60), BUTTON_COLOR)
trade_button = gui.Button(WINDOW, "Trade", FONT, ORANGE, pygame.Rect(1080, 360, 100, 60), BUTTON_COLOR)
build_button = gui.Button(WINDOW, "Build", FONT, ORANGE, pygame.Rect(1080, 440, 100, 60), BUTTON_COLOR)
mortgage_button = gui.Button(WINDOW, "Mortgage", FONT, ORANGE, pygame.Rect(1080, 520, 100, 60), BUTTON_COLOR)
analysis_button = gui.Button(WINDOW, "Analysis", FONT, ORANGE, pygame.Rect(1080, 600, 100, 60), BUTTON_COLOR)
end_turn_button = gui.Button(WINDOW, "End Turn", FONT, ORANGE, pygame.Rect(1080, 680, 100, 60), BUTTON_COLOR)
textbox = pygame_textinput.TextInput("", font_size=20, text_color=WHITE,
                                     cursor_color=ORANGE, max_string_length=18, rect=pygame.Rect(950, 370, 110, 30))
textbox2 = pygame_textinput.TextInput("", font_size=20, text_color=WHITE,
                                      cursor_color=ORANGE, max_string_length=18, rect=pygame.Rect(760, 370, 110, 30))
player_option = gui.OptionBox(760, 435, 310, 30, GREY, (100, 200, 255), FONT, ["Car", "Ship", "Shoe"])

car = Player("Car", 40000, START_X, START_Y)
die = Dice(pygame.Rect(1100, 50, 60, 60), pygame.Rect(1100, 120, 60, 60), BUTTON_COLOR, 30)

def draw_player_info(selected_option):
    info_rect = pygame.Rect(760, 435, 310, 300)
    pygame.draw.rect(WINDOW, WHITE, info_rect, 2)
    if selected_option == 0:
        gui.draw_text(WINDOW, "Wealth: $"+str(car.get_money()), FONT, WHITE, info_rect.left, 475)
        gui.draw_text(WINDOW, "Properties: ", FONT, WHITE, info_rect.left, 510)
        draw_property_rects()

CARD_DIST = 30
LEFT_MARGIN = 16
COLOR_GROUP_DIST = 20
OWNED_PROPERTY_WIDTH = 20
OWNED_PROPERTY_HEIGHT = 35
ROW_ONE_Y = 540
Y_DIST = 50

ROW_TWO_Y = ROW_ONE_Y + Y_DIST
ROW_THREE_Y = ROW_TWO_Y + Y_DIST
ROW_FOUR_Y = ROW_THREE_Y + Y_DIST

ROW_START = 765
ROW_ONE_START = ROW_THREE_START = 765 + 16
ROW_MIDDLE = 765 + 100
ROW_ONE_END = ROW_TWO_END = 925 + 50
ROW_THREE_END = ROW_ONE_END + CARD_DIST/2
ROW_TWO_START = 765

def draw_property_rects():
    
    if car.property_owned(1): # Mediterranean Ave.
        pygame.draw.rect(WINDOW, BROWN, pygame.Rect(ROW_ONE_START, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)) # Filled in rectangle when property is owned
    else:
        pygame.draw.rect(WINDOW, BROWN, pygame.Rect(ROW_ONE_START, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2) # Have only border of rectangle if property is unowned
        
    if car.property_owned(3): # Baltic Ave.
        pygame.draw.rect(WINDOW, BROWN, pygame.Rect(ROW_ONE_START + CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, BROWN, pygame.Rect(ROW_ONE_START + CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
    
    if car.property_owned(6): # Oriental Ave.
        pygame.draw.rect(WINDOW, LIGHTBLUE, pygame.Rect(ROW_MIDDLE, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, LIGHTBLUE, pygame.Rect(ROW_MIDDLE, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
    
    if car.property_owned(8): # Vermont Ave.
        pygame.draw.rect(WINDOW, LIGHTBLUE, pygame.Rect(ROW_MIDDLE + CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, LIGHTBLUE, pygame.Rect(ROW_MIDDLE + CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
    if car.property_owned(9): # Connecticut Ave.
        pygame.draw.rect(WINDOW, LIGHTBLUE, pygame.Rect(ROW_MIDDLE + 2*CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, LIGHTBLUE, pygame.Rect(ROW_MIDDLE + 2*CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
    
    if car.property_owned(11): # St. Charles Place
        pygame.draw.rect(WINDOW, PINK, pygame.Rect(ROW_ONE_END, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, PINK, pygame.Rect(ROW_ONE_END, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
    if car.property_owned(13): # States Ave.
        pygame.draw.rect(WINDOW, PINK, pygame.Rect(ROW_ONE_END + CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, PINK, pygame.Rect(ROW_ONE_END + CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
    if car.property_owned(14): # Virginia Ave.
        pygame.draw.rect(WINDOW, PINK, pygame.Rect(ROW_ONE_END + 2*CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, PINK, pygame.Rect(ROW_ONE_END + 2*CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
    
    
    
    if car.property_owned(16): # St. James Place
        pygame.draw.rect(WINDOW, ORANGE, pygame.Rect(ROW_TWO_START, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, ORANGE, pygame.Rect(ROW_TWO_START, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
    if car.property_owned(18): # Tennessee Ave.
        pygame.draw.rect(WINDOW, ORANGE, pygame.Rect(ROW_TWO_START + CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, ORANGE, pygame.Rect(ROW_TWO_START + CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
    if car.property_owned(19): # New York Ave.
        pygame.draw.rect(WINDOW, ORANGE, pygame.Rect(ROW_TWO_START + 2*CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, ORANGE, pygame.Rect(ROW_TWO_START + 2*CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
    
    if car.property_owned(21): # Kentucky Ave.
        pygame.draw.rect(WINDOW, RED, pygame.Rect(ROW_MIDDLE, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, RED, pygame.Rect(ROW_MIDDLE, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
    if car.property_owned(23): # Indiana Ave.
        pygame.draw.rect(WINDOW, RED, pygame.Rect(ROW_MIDDLE + CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, RED, pygame.Rect(ROW_MIDDLE + CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
    if car.property_owned(24): # Illinois Ave.
        pygame.draw.rect(WINDOW, RED, pygame.Rect(ROW_MIDDLE + 2*CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, RED, pygame.Rect(ROW_MIDDLE + 2*CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
    
    if car.property_owned(26): # Atlantic Ave.
        pygame.draw.rect(WINDOW, YELLOW, pygame.Rect(ROW_TWO_END, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, YELLOW, pygame.Rect(ROW_TWO_END, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
    if car.property_owned(27): # Ventnor Ave.
        pygame.draw.rect(WINDOW, YELLOW, pygame.Rect(ROW_TWO_END + CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, YELLOW, pygame.Rect(ROW_TWO_END + CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
    if car.property_owned(29): # Marvin Gardens
        pygame.draw.rect(WINDOW, YELLOW, pygame.Rect(ROW_TWO_END + 2*CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, YELLOW, pygame.Rect(ROW_TWO_END + 2*CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
    
    
    
    
    #UTILITIES
    if car.property_owned(12): # Electric Community
        electric_community_rect = pygame.Rect(ROW_THREE_START, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        lightbulb_rect = LIGHTBULB_IMAGE.get_rect()
        lightbulb_rect.center = electric_community_rect.center
        pygame.draw.rect(WINDOW, WHITE, electric_community_rect)
        WINDOW.blit(LIGHTBULB_IMAGE, lightbulb_rect)
    else:
        electric_community_rect = pygame.Rect(ROW_THREE_START, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        pygame.draw.rect(WINDOW, WHITE, electric_community_rect, 2)
        
    if car.property_owned(28): # Water Works
        water_works_rect = pygame.Rect(ROW_THREE_START + CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        droplet_rect = WATER_DROPLET_IMAGE.get_rect()
        droplet_rect.center = water_works_rect.center
        pygame.draw.rect(WINDOW, WHITE, water_works_rect)
        WINDOW.blit(WATER_DROPLET_IMAGE, droplet_rect)
    else:
        water_works_rect = pygame.Rect(ROW_THREE_START + CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        pygame.draw.rect(WINDOW, WHITE, water_works_rect, 2)
    
    if car.property_owned(31): # Pacific Ave.
        pygame.draw.rect(WINDOW, GREEN, pygame.Rect(ROW_MIDDLE, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, GREEN, pygame.Rect(ROW_MIDDLE, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
    if car.property_owned(32): # North Carolina Ave.
        pygame.draw.rect(WINDOW, GREEN, pygame.Rect(ROW_MIDDLE + CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, GREEN, pygame.Rect(ROW_MIDDLE + CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
    if car.property_owned(34): # Pennsylvania Ave.
        pygame.draw.rect(WINDOW, GREEN, pygame.Rect(ROW_MIDDLE + 2*CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, GREEN, pygame.Rect(ROW_MIDDLE + 2*CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
    
    if car.property_owned(37): # Park Place
        pygame.draw.rect(WINDOW, DARKBLUE, pygame.Rect(ROW_THREE_END, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, DARKBLUE, pygame.Rect(ROW_THREE_END, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
    if car.property_owned(39): # Boardwalk
        pygame.draw.rect(WINDOW, DARKBLUE, pygame.Rect(ROW_THREE_END + CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
    else:
        pygame.draw.rect(WINDOW, DARKBLUE, pygame.Rect(ROW_THREE_END + CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
    
    
    #RAILROADS
    if car.property_owned(5): # Reading Railroad
        reading_railroad_rect = pygame.Rect(ROW_MIDDLE - CARD_DIST/2, ROW_FOUR_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        pygame.draw.rect(WINDOW, GREY, reading_railroad_rect)
        railroad_icon_rect.center = reading_railroad_rect.center
        WINDOW.blit(RAILROAD_IMAGE, railroad_icon_rect)
    else:
        reading_railroad_rect = pygame.Rect(ROW_MIDDLE - CARD_DIST/2, ROW_FOUR_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        pygame.draw.rect(WINDOW, GREY, reading_railroad_rect, 2)
        
    if car.property_owned(15): # Pennsylvania Railroad
        penn_railroad_rect = pygame.Rect(ROW_MIDDLE - CARD_DIST/2 + CARD_DIST, ROW_FOUR_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        pygame.draw.rect(WINDOW, GREY, penn_railroad_rect)
        railroad_icon_rect.center = penn_railroad_rect.center
        WINDOW.blit(RAILROAD_IMAGE, railroad_icon_rect)
    else:
        penn_railroad_rect = pygame.Rect(ROW_MIDDLE - CARD_DIST/2 + CARD_DIST, ROW_FOUR_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        pygame.draw.rect(WINDOW, GREY, penn_railroad_rect, 2)
        
    if car.property_owned(25): # B & O Railroad
        bo_railraod = pygame.Rect(ROW_MIDDLE - CARD_DIST/2 + 2*CARD_DIST, ROW_FOUR_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        pygame.draw.rect(WINDOW, GREY, bo_railraod)
        railroad_icon_rect.center = bo_railraod.center
        WINDOW.blit(RAILROAD_IMAGE, railroad_icon_rect)
    else:
        bo_railraod = pygame.Rect(ROW_MIDDLE - CARD_DIST/2 + 2*CARD_DIST, ROW_FOUR_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        pygame.draw.rect(WINDOW, GREY, bo_railraod, 2)
        
    if car.property_owned(35): # Short Line
        short_line = pygame.Rect(ROW_MIDDLE - CARD_DIST/2 + 3*CARD_DIST, ROW_FOUR_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        pygame.draw.rect(WINDOW, GREY, short_line)
        railroad_icon_rect.center = short_line.center
        WINDOW.blit(RAILROAD_IMAGE, railroad_icon_rect)
    else:
        short_line = pygame.Rect(ROW_MIDDLE - CARD_DIST/2 + 3*CARD_DIST, ROW_FOUR_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        pygame.draw.rect(WINDOW, GREY, short_line, 2)
    
    
def draw(selected_option):
    WINDOW.fill(BLACK)

    WINDOW.blit(BOARD_IMAGE, board_rect)
    WINDOW.blit(CAR, (car.get_x(), car.get_y()))
    
    draw_player_info(selected_option)
    draw_widgets()
    
    if car.get_position() in property_images:
        WINDOW.blit(property_images[car.get_position()], (775, 60))
    
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
    

# drawings two sided arrow for trading
arrow_offset_x = 900 #initialize variables here so it is not called every frame
arrow_offset_y = 365
arrowscale = 8

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
                        car.move(die.get_rollsum()) #move the player the sum of the roll
                        roll_button.release()    
                    elif buy_button.is_clicked(event):
                        # Can only buy properties, not any other special location
                        loc = property_dict["locations"][car.get_position()]["name"]
                        if loc != "GO" \
                        and loc != "Community Chest" and loc != "Chance" \
                        and loc != "Tax" and loc != "Jail" and loc != "Free Parking" and loc != "Cop":
                            car.buy_property(car.get_position(), property_dict["locations"][car.get_position()]["color"], property_dict["locations"][car.get_position()]["cost"])
                            print(car.get_properties())
                            print(car.get_color_frequency())
                    elif textbox.is_clicked(event):
                        textbox.set_enabled(True)
                    elif textbox2.is_clicked(event):
                        textbox2.set_enabled(True)  
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: #When enter is pressed it exits out of typing mode for the text boxes
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
        # Makes sure that when an option is selected, it stay selected until a new option is picked
        if selected_option == -1: 
            selected_option = current_option
        if selected_option != -1:
            current_option = selected_option
        
        draw(selected_option)
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    main()