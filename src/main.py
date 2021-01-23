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

special_locs = ["Go", "Community Chest", "Chance", "Tax", "Jail", "Free Parking", "Cop"]

class GameEngine:
    """Handles game logic such as jail, taxes, rolling doubles, turns, rent, etc
    """
    def __init__(self, amount_of_players):
        """Initilaize essential logic to the game such as players, starting turn, whether someone has rolled
        
        Args:
            amount_of_players (int): Amount of players that will participate in the game
        """
        self.amount_of_players = amount_of_players
        self.turn = 0 # Starts on first players turn
        self.rollled = False # Determines which phase of a players turn (rolling, trading, etc)
        self.doubles = 0 # Determines amount doubles rolled
        self.dice_roll = 0 # Dice roll for a single turn
    
    def change_turn(self):
        self.turn += 1
        self.turn = self.turn % self.amount_of_players # Make sure that the turn loops based on amount of players
        self.rollled = False
        self.doubles = 0
        
    def get_turn(self):
        return self.turn
    
    def check_player_pos(self):
        for player in players:
            if player.is_player_turn(self.turn):
                if player.get_position() == 30: # Jail
                    player.go_to_jail()
            
                elif player.get_position() == 4: # Tax $200
                    print("TAX 200!")
                    player.pay(200)
                elif player.get_position() == 38: # Tax $100
                    print("TAX 100!")
                    player.pay(100)
                elif player.get_position() == 2 or player.get_position() == 17 or player.get_position() == 33: # Community Chest spots
                    pass
                elif player.get_position() == 7 or player.get_position() == 22 or car.get_position() == 36: # Chance spots
                    pass
                
                for other_player in players:
                    if other_player is not player and other_player.property_owned(player.get_position()):
                        # WHen both electric community and water works is owned, 
                        # the rent is 10 times the dice roll, otherwise it is 4 times the roll
                        if player.get_position() == 12: # electric community
                            if other_player.property_owned(28): # Water works
                                rent = 10 * self.dice_roll 
                            else:
                                rent = 4 * self.dice_roll
                        elif player.get_position() == 28:
                            if other_player.property_owned(12):
                                rent = 10 * self.dice_roll
                            else:
                                rent = 4 * self.dice_roll
                        elif player.get_position() == 5 or player.get_position() == 15 or player.get_position() == 25 or player.get_position() == 35: # railroads
                            number_of_railroads = other_player.get_number_of_group_owned("RR")
                            if number_of_railroads == 1:
                                rent = property_dict["locations"][player.get_position()]["rent"]
                            elif number_of_railroads == 2:
                                rent = property_dict["locations"][player.get_position()]["rent1"]
                            elif number_of_railroads == 3:
                                rent = property_dict["locations"][player.get_position()]["rent2"]
                            elif number_of_railroads == 4:
                                rent = property_dict["locations"][player.get_position()]["rent3"]
                                
                            
                        else:
                            rent = property_dict["locations"][player.get_position()]["rent"]
                            if other_player.has_color_group(property_dict["locations"][player.get_position()]["color"]):
                                number_of_houses = other_player.get_property_house_amount(player.get_position())
                                # Determine rent based on number of nhouses
                                if number_of_houses == 0:
                                    rent = 2 * rent # When a player owns a color group the regular rent is doubled
                                elif number_of_houses == 1:
                                    rent = property_dict["locations"][player.get_position()]["rent1"]
                                elif number_of_houses == 2:
                                    rent = property_dict["locations"][player.get_position()]["rent2"]
                                elif number_of_houses == 3:
                                    rent = property_dict["locations"][player.get_position()]["rent3"]
                                elif number_of_houses == 4:
                                    rent = property_dict["locations"][player.get_position()]["rent4"]
                                elif number_of_houses == 5:
                                    rent = property_dict["locations"][player.get_position()]["rent5"]
                        other_player.make_deposit(rent)
                        player.pay(rent)
                        break
                break
                    

    
    def set_dice_roll(self, dice_roll, double):
        self.dice_roll = dice_roll
        for player in players:
            if player.is_player_turn(self.turn):
                player.move(dice_roll) # Move the player the sum of the roll
                break
        
        if double:
            self.doubles += 1
            if self.doubles == 3: # When three doubles are rolled, player goes to jail
                for player in players:
                    if player.is_player_turn(self.turn):
                        player.go_to_jail()
                        break
                self.doubles == 0
                self.rollled = True
        else:
            self.rollled = True
        
        self.check_player_pos()
        
    def roll_complete(self):
        return self.rollled
    
    def process_trade(self):
        pass
    
    def is_player_in_jail(self):
        for player in players:
            if player.is_player_turn(game.turn):
                player.increment_jail()
                if player.get_jail_count() > 3:
                    player.leave_jail()
                return player.is_in_jail()
        
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
    
    def is_double(self):
        if self.dice_one == self.dice_two:
            return True
        return False
    
    def draw_dice(self):
        pygame.draw.rect(WINDOW, self.color, self.dice_rect, 2)
        pygame.draw.rect(WINDOW, self.color, self.dice2_rect, 2)
        WINDOW.blit(self.surface, self.text_rect)
        WINDOW.blit(self.surface2, self.text2_rect)
    
    def get_rollsum(self):
        return int(self.dice_one) + int(self.dice_two)

# Initialize GUI components and players
roll_button = gui.Button(WINDOW, 'Roll', FONT, ORANGE, pygame.Rect(1110, 200, 100, 60), BUTTON_COLOR)
buy_button = gui.Button(WINDOW, 'Buy', FONT, ORANGE, pygame.Rect(1110, 280, 100, 60), BUTTON_COLOR)
trade_button = gui.Button(WINDOW, "Trade", FONT, ORANGE, pygame.Rect(1110, 360, 100, 60), BUTTON_COLOR)
build_button = gui.Button(WINDOW, "Build", FONT, ORANGE, pygame.Rect(1110, 440, 100, 60), BUTTON_COLOR)
mortgage_button = gui.Button(WINDOW, "Mortgage", FONT, ORANGE, pygame.Rect(1110, 520, 100, 60), BUTTON_COLOR)
analysis_button = gui.Button(WINDOW, "Analysis", FONT, ORANGE, pygame.Rect(1110, 600, 100, 60), BUTTON_COLOR)
end_turn_button = gui.Button(WINDOW, "End Turn", FONT, ORANGE, pygame.Rect(1110, 680, 100, 60), BUTTON_COLOR)
bail_button = gui.Button(WINDOW, "Pay Bail", FONT, (0, 0, 255), pygame.Rect(1110-250, 200, 100, 60), (255, 0, 0))

textbox = pygame_textinput.TextInput("", font_size=20, text_color=WHITE,
                                     cursor_color=ORANGE, max_string_length=18, rect=pygame.Rect(950, 370, 110, 30))
textbox2 = pygame_textinput.TextInput("", font_size=20, text_color=WHITE,
                                      cursor_color=ORANGE, max_string_length=18, rect=pygame.Rect(760, 370, 110, 30))
player_option = gui.OptionBox(760, 435, 310, 30, GREY, (100, 200, 255), FONT, ["Car", "Shoe", "Ship", ])

car = Player("Car", 40000, START_X, START_Y, 0)
shoe = Player("Shoe", 40000, START_X, START_Y, 1)
players = [car, shoe]

die = Dice(pygame.Rect(1100+30, 50, 60, 60), pygame.Rect(1100+30, 120, 60, 60), BUTTON_COLOR, 30)
game = GameEngine(2)

def draw_player_info(selected_option):
    info_rect = pygame.Rect(760, 435, 310, 300)
    pygame.draw.rect(WINDOW, WHITE, info_rect, 2)
    for player in players:
        if selected_option == player.get_turn_number():
            gui.draw_text(WINDOW, "Wealth: $"+str(player.get_money()), FONT, WHITE, info_rect.left, 475, False)
            gui.draw_text(WINDOW, "Properties: ", FONT, WHITE, info_rect.left, 510, False)
            player.draw_player_properties(WINDOW)
            break

def draw_turn_info():
    for player in players:
        if player.is_player_turn(game.get_turn()): 
            gui.draw_text(WINDOW, "Turn: " + player.get_name(), FONT, WHITE, 50, 30, False)
            break
        
def draw(selected_option):
    WINDOW.fill(BLACK)

    draw_turn_info()
    
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
    if (game.get_turn() == 0 and car.is_in_jail()) or (game.get_turn() == 1 and shoe.is_in_jail()):
        bail_button.draw()
        
    WINDOW.blit(textbox.get_surface(), (950, 400 - textbox.get_fontsize()))
    WINDOW.blit(textbox2.get_surface(), (760, 400 - textbox2.get_fontsize()))
    player_option.draw(WINDOW)
    
    
# draw two sided arrow for trading
arrow_offset_x = 900 #initialize variables here so it is not called every frame
arrow_offset_y = 365
arrowscale = 8
def draw_trading_area():
    # Draw a double sided arrow and two lines to indicate the text input areas
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
    
    while run:
        clock.tick(FPS)
        events = pygame.event.get()
        selected_option = player_option.update(events)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if roll_button.is_clicked(event) and not game.roll_complete() and not game.is_player_in_jail():
                    die.roll()
                    game.set_dice_roll(die.get_rollsum(), die.is_double())
                
                elif buy_button.is_clicked(event):
                    for player in players:
                        loc = property_dict["locations"][player.get_position()]["name"]
                        if player.is_player_turn(game.get_turn()) and loc not in special_locs:
                            pos = player.get_position()
                            col = property_dict["locations"][pos]["color"]
                            cost = property_dict["locations"][pos]["cost"]
                            player.buy_property(pos, col, cost)
                            break
                
                elif build_button.is_clicked(event) and textbox.represents_int():
                    pos = int(textbox.get_text())
                    if len(property_dict["locations"]) >= pos and "house_price" in property_dict["locations"][pos]:
                        color = property_dict["locations"][pos]["color"]
                        for player in players:
                            if player.is_player_turn(game.get_turn()) and player.has_color_group(color):
                                color_property = property_dict["locations"][pos]["friend_id"] # property in same color group as location where house is being built
                                house_price = property_dict["locations"][pos]["house_price"]
                                if "friend_id2" in property_dict["locations"][pos]:
                                    color_property2 = property_dict["locations"][pos]["friend_id2"]
                                    player.buy_house(pos, color, house_price, color_property, color_property2)
                                else:
                                    player.buy_house(pos, color, house_price, color_property)
                                break
                        
                elif analysis_button.is_clicked(event):
                    pass
                
                elif textbox.is_clicked(event):
                    textbox.set_enabled(True)
                
                elif textbox2.is_clicked(event):
                    textbox2.set_enabled(True)  
                
                elif end_turn_button.is_clicked(event):
                    game.change_turn()
                    for player in players:
                        if player.is_player_turn(game.get_turn()):
                            player_option.set_selected_option(player.get_turn_number())
                            break
                        
                elif bail_button.is_clicked(event):
                    for player in players:
                        if player.is_player_turn(game.get_turn()) and player.is_in_jail():
                            player.pay(50)
                            player.leave_jail()
                            break
                            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # When enter is pressed it exits out of typing mode for the text boxes
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
        
        draw(selected_option)
            
        pygame.display.flip()
        
        
    pygame.quit()

if __name__ == "__main__":
    main()