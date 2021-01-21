import pygame
import os
import json
import random

from player import Player
from board import Board
import pygame_textinput
import gui_components as gui

#Setting up pygame
WINDOW_WIDTH, WINDOW_HEIGHT = 1250, 800
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
FPS = 60
pygame.display.set_caption("Monopoly")
pygame.font.init()

# Define important colors
FONT = pygame.font.Font(None, 30)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (155, 155, 155)
ORANGE = (255, 180, 0)
BUTTON_COLOR = (204, 255, 255)

# Setup images
BOARD_IMAGE = pygame.image.load(os.path.join('Assets', 'monopoly.jpg'))
board_rect = BOARD_IMAGE.get_rect()
board_rect.center = (BOARD_IMAGE.get_height()/2 + 50, WINDOW_HEIGHT/2)

CAR = pygame.image.load(os.path.join('Assets', 'car.png'))
SHOE = pygame.image.load(os.path.join('Assets', 'shoe.png'))
START_X, START_Y = 640, 670 # Starting position of a player

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

class GameEngine:
    
    def __init__(self, amount_of_players):
        self.amount_of_players = amount_of_players
        self.turn = 0
        self.rollled = False # Determines which phase of a players turn (rolling, trading, etc)
        self.doubles = 0 # Determines amount doubles rolled
        self.dice_roll = 0 # Dice roll for a single turn
    
    def change_turn(self):
        self.turn += 1
        self.turn = self.turn % self.amount_of_players
        
    def get_turn(self):
        return self.turn

    def handle_event(self, events):
        pass
    
    def check_player_pos(self):
        pass
    
    def set_dice_roll(self, dice_roll):
        self.dice_roll = dice_roll
         
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
    
roll_button = gui.Button(WINDOW, 'Roll', FONT, ORANGE, pygame.Rect(1110, 200, 100, 60), BUTTON_COLOR)
buy_button = gui.Button(WINDOW, 'Buy', FONT, ORANGE, pygame.Rect(1110, 280, 100, 60), BUTTON_COLOR)
trade_button = gui.Button(WINDOW, "Trade", FONT, ORANGE, pygame.Rect(1110, 360, 100, 60), BUTTON_COLOR)
build_button = gui.Button(WINDOW, "Build", FONT, ORANGE, pygame.Rect(1110, 440, 100, 60), BUTTON_COLOR)
mortgage_button = gui.Button(WINDOW, "Mortgage", FONT, ORANGE, pygame.Rect(1110, 520, 100, 60), BUTTON_COLOR)
analysis_button = gui.Button(WINDOW, "Analysis", FONT, ORANGE, pygame.Rect(1110, 600, 100, 60), BUTTON_COLOR)
end_turn_button = gui.Button(WINDOW, "End Turn", FONT, ORANGE, pygame.Rect(1110, 680, 100, 60), BUTTON_COLOR)
textbox = pygame_textinput.TextInput("", font_size=20, text_color=WHITE,
                                     cursor_color=ORANGE, max_string_length=18, rect=pygame.Rect(950, 370, 110, 30))
textbox2 = pygame_textinput.TextInput("", font_size=20, text_color=WHITE,
                                      cursor_color=ORANGE, max_string_length=18, rect=pygame.Rect(760, 370, 110, 30))
player_option = gui.OptionBox(760, 435, 310, 30, GREY, (100, 200, 255), FONT, ["Car", "Shoe", "Ship"])

car = Player("Car", 40000, START_X, START_Y)
shoe = Player("Shoe", 40000, START_X, START_Y)

die = Dice(pygame.Rect(1100+30, 50, 60, 60), pygame.Rect(1100+30, 120, 60, 60), BUTTON_COLOR, 30)
game = GameEngine(2)

def draw_player_info(selected_option):
    info_rect = pygame.Rect(760, 435, 310, 300)
    pygame.draw.rect(WINDOW, WHITE, info_rect, 2)
    if selected_option == 0:
        gui.draw_text(WINDOW, "Wealth: $"+str(car.get_money()), FONT, WHITE, info_rect.left, 475)
        gui.draw_text(WINDOW, "Properties: ", FONT, WHITE, info_rect.left, 510)
        car.draw_player_properties(WINDOW)
    elif selected_option == 1:
        gui.draw_text(WINDOW, "Wealth: $"+str(shoe.get_money()), FONT, WHITE, info_rect.left, 475)
        gui.draw_text(WINDOW, "Properties: ", FONT, WHITE, info_rect.left, 510)
        shoe.draw_player_properties(WINDOW)
    elif selected_option == 2:
        pass
   
def draw(selected_option):
    WINDOW.fill(BLACK)

    gui.draw_text(WINDOW, "Turn: "+str(game.get_turn()), FONT, WHITE, 50, 30)
    WINDOW.blit(BOARD_IMAGE, board_rect)
    WINDOW.blit(CAR, (car.get_x(), car.get_y()))
    WINDOW.blit(SHOE, (shoe.get_x(), shoe.get_y()))
    draw_player_info(selected_option)
    draw_widgets()
    
    if game.get_turn() == 0 and car.get_position() in property_images:
        WINDOW.blit(property_images[car.get_position()], (785, 60))
    elif game.get_turn() == 1 and shoe.get_position() in property_images:
        WINDOW.blit(property_images[shoe.get_position()], (785, 60))
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

special_locs = ["Go", "Community Chest", "Chance", "Tax", "Jail", "Free Parking", "Cop"]
 
def main():
    clock = pygame.time.Clock()
    run = True
    
    current_option = 0
    
    while run:
        clock.tick(FPS)
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if roll_button.is_clicked(event):
                        die.roll()
                        if game.get_turn() == 0:
                            car.move(die.get_rollsum()) # Move the player the sum of the roll
                        elif game.get_turn() == 1:
                            shoe.move(die.get_rollsum())
                        roll_button.release()
                    elif buy_button.is_clicked(event):
                        # Can only buy properties, not any other special location
                        loc = property_dict["locations"][car.get_position()]["name"]
                        if loc not in special_locs:
                            if game.get_turn() == 0:
                                car.buy_property(car.get_position(), property_dict["locations"][car.get_position()]["color"], property_dict["locations"][car.get_position()]["cost"])
                            elif game.get_turn() == 1:
                                shoe.buy_property(shoe.get_position(), property_dict["locations"][shoe.get_position()]["color"], property_dict["locations"][shoe.get_position()]["cost"])
                    elif textbox.is_clicked(event):
                        textbox.set_enabled(True)
                    elif textbox2.is_clicked(event):
                        textbox2.set_enabled(True)  
                    elif end_turn_button.is_clicked(event):
                        game.change_turn()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # When enter is pressed it exits out of typing mode for the text boxes
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