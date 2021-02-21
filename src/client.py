import pygame
import os
import json


from network import Network
from player import Player
import sys
import pygame_textinput
import gui_components as gui
import dice

#Setting up pygame
WINDOW_WIDTH, WINDOW_HEIGHT = 1250, 800
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
FPS = 60
pygame.display.set_caption("Monopoly")
pygame.font.init()

# Define important colors
FONT = pygame.font.Font(None, 30)
SMALLFONT = pygame.font.Font(None, 20)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (155, 155, 155)
ORANGE = (255, 180, 0)
BUTTON_COLOR = (204, 255, 255)

# Setup images
BOARD_IMAGE = pygame.image.load("../assets/monopoly.jpg")
board_rect = BOARD_IMAGE.get_rect()
board_rect.center = (BOARD_IMAGE.get_height()/2 + 50, WINDOW_HEIGHT/2)

#Contains all property images mapped to their respective positions
property_images = dict({
                1 : pygame.image.load("../assets/mediterranean_avenue.png"),
                3 : pygame.image.load("../assets/baltic_avenue.jpg"),
                5 : pygame.image.load("../assets/reading_railroad.jpg"),
                6 : pygame.image.load("../assets/oriental_avenue.jpg"),
                8 : pygame.image.load("../assets/vermont_avenue.jpg"),
                9 : pygame.image.load("../assets/connecticut_avenue.jpg"),
                12 : pygame.image.load("../assets/electric_company.jpg"),
                13 : pygame.image.load("../assets/states_avenue.jpg"),
                11 : pygame.image.load("../assets/st_charles_place.jpg"),
                14 : pygame.image.load("../assets/virginia_avenue.jpg"),
                15 : pygame.image.load("../assets/pennsylvania_railroad.jpg"),
                16 : pygame.image.load("../assets/st_james_place.jpg"),
                18 : pygame.image.load("../assets/tennessee_avenue.jpg"),
                19 : pygame.image.load("../assets/new_york_avenue.jpg"),
                21 : pygame.image.load("../assets/kentucky_avenue.jpg"),
                23 : pygame.image.load("../assets/indiana_avenue.jpg"),
                24 : pygame.image.load("../assets/illinois_avenue.jpg"),
                25 : pygame.image.load("../assets/b&o_railroad.jpg"),
                26 : pygame.image.load("../assets/atlantic_avenue.jpg"),
                27 : pygame.image.load("../assets/ventnor_avenue.jpg"),
                28 : pygame.image.load("../assets/water_works.jpg"),
                29 : pygame.image.load("../assets/marvin_gardens.jpg"),
                31 : pygame.image.load("../assets/pacific_avenue.jpg"),
                32 : pygame.image.load("../assets/north_carolina_avenue.jpg"),
                34 : pygame.image.load("../assets/pennsylvania_avenue.jpg"),
                35 : pygame.image.load("../assets/short_line_railroad.jpg"),
                37 : pygame.image.load("../assets/park_place.jpg"),
                39 : pygame.image.load("../assets/boardwalk.jpg"),
            })


with open('board_data.json') as json_file:
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
    
    def set_turn(self, turn):
        self.turn = turn % self.amount_of_players
        
    def get_turn(self):
        return self.turn
    
    def check_player_pos(self, player, players):
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
            elif player.get_position() == 7 or player.get_position() == 22 or player.get_position() == 36: # Chance spots
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
                    

    
    def set_dice_roll(self, dice_roll, double, player):
        self.dice_roll = dice_roll
        print(player.get_name() + " : " + str(player.get_turn_number()) + str(self.turn) + str(self.dice_roll))
        if player.is_player_turn(self.turn):
            print("ABOUT TO MOVE")
            player.move(dice_roll) # Move the player the sum of the roll
        
        if double:
            self.doubles += 1
            if self.doubles == 3: # When three doubles are rolled, player goes to jail
                if player.is_player_turn(self.turn):
                    player.go_to_jail()
                self.doubles == 0
                self.rollled = True
        else:
            self.rollled = True
        
        #self.check_player_pos()
    def set_dice(self, dice_roll):
        self.dice_roll = dice_roll
            
    def roll_complete(self):
        return self.rollled
    
    def process_trade(self):
        pass
    
    def is_player_in_jail(self, player):
        if player.is_player_turn(game.turn):
            player.increment_jail()
            if player.get_jail_count() > 3:
                player.leave_jail()
            return player.is_in_jail()
            
    def get_player_amount(self):
        return self.amount_of_players
    
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
                                     cursor_color=ORANGE, max_string_length=22, rect=pygame.Rect(920, 350, 115, 30))
textbox2 = pygame_textinput.TextInput("", font_size=20, text_color=WHITE,
                                      cursor_color=ORANGE, max_string_length=18, rect=pygame.Rect(920, 385, 110, 30))

options = [] # Harcoded for now
game = GameEngine(2)

player_option = gui.OptionBox(760, 435, 310, 30, GREY, (100, 200, 255), FONT, options)

options2 = []

trade_optionbox = gui.OptionBox(770, 370, 110, 20, GREY, (100, 200, 255), SMALLFONT, options2)
trade_optionbox2 = gui.OptionBox(770, 400, 110, 20, GREY, (100, 200, 255), SMALLFONT, options2)  

die = dice.Dice(pygame.Rect(1100+30, 50, 60, 60), pygame.Rect(1100+30, 120, 60, 60), BUTTON_COLOR, 30)


def redrawWindow(WINDOW, player, player2, selected_option):
    WINDOW.fill(BLACK)
    WINDOW.blit(BOARD_IMAGE, board_rect)
    if (player.is_player_turn(game.get_turn())):
        gui.draw_text(WINDOW, "Turn: " + player.get_name(), FONT, WHITE, 50, 30, False)
    else:
        gui.draw_text(WINDOW, "Turn: " + player2.get_name(), FONT, WHITE, 50, 30, False)
    
    info_rect = pygame.Rect(760, 435, 310, 300)
    pygame.draw.rect(WINDOW, WHITE, info_rect, 2) # Player property box
    
    # Draw two players and their properties
    player.draw(WINDOW) 
    player2.draw(WINDOW)
    #player.draw_player_properties(WINDOW)
    
    if selected_option == player.get_turn_number():
        gui.draw_text(WINDOW, "Wealth: $"+str(player.get_money()), FONT, WHITE, info_rect.left, 475, False)
        gui.draw_text(WINDOW, "Properties: ", FONT, WHITE, info_rect.left, 510, False)
        player.draw_player_properties(WINDOW)
    else:
        gui.draw_text(WINDOW, "Wealth: $"+str(player2.get_money()), FONT, WHITE, info_rect.left, 475, False)
        gui.draw_text(WINDOW, "Properties: ", FONT, WHITE, info_rect.left, 510, False)
        player2.draw_player_properties(WINDOW)
    
    #player2.draw_player_properties(WINDOW)
    
    if player.is_player_turn(game.get_turn()) and player.get_position() in property_images:
        WINDOW.blit(property_images[player.get_position()], (785, 60))
    elif player2.is_player_turn(game.get_turn()) and player2.get_position() in property_images:
        WINDOW.blit(property_images[player2.get_position()], (785, 60))
    
    # Draw different buttons on the side
    draw_widgets() 
    pygame.display.update()

def draw_widgets():
    roll_button.draw()
    die.draw_dice(WINDOW)
    buy_button.draw()
    trade_button.draw()
    build_button.draw()
    mortgage_button.draw()
    analysis_button.draw()
    end_turn_button.draw()
    
    WINDOW.blit(textbox.get_surface(), (textbox.get_rect().left, textbox.get_rect().centery))#(950, 400 - textbox.get_fontsize()))
    WINDOW.blit(textbox2.get_surface(), (textbox2.get_rect().left, textbox2.get_rect().centery))
    player_option.draw(WINDOW)
    trade_optionbox2.draw(WINDOW)
    pygame.draw.line(WINDOW, WHITE, (920, 380), (950+115, 380), width=4)
    pygame.draw.line(WINDOW, WHITE, (920, 413), (950+115, 413), width=4)
         
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network() 
    p = n.get_p()
    switch_turn = False
    first = True
    
    while run:
        clock.tick(FPS)
        
        
        send_objs_list = []
        if switch_turn:
            send_objs_list = [p, str(game.get_turn()), die.get_dice_one(), die.get_dice_two()]
            switch_turn = False
        else:
            send_objs_list = [p, "x", die.get_dice_one(), die.get_dice_two()]

        data = n.send(send_objs_list)  
        p2 = data[0]
        #print(str(data[1]))
        
        temp = game.get_turn()
        game.set_turn(int(data[1]))
        if p.is_player_turn(game.get_turn()) and temp != game.get_turn():
           player_option.set_selected_option(game.get_turn())
           
        die.set_dice(data[2], data[3])
        player_list = [p, p2]
        
        if first:
            options = []
            for _ in range(len(player_list)):
                options.append(None)
            for player in player_list:
                options[player.get_turn_number()] = player.get_name()
            first = False
            player_option.set_option_list(options)
            
            options2 = options.copy()
            options2.pop(p.get_turn_number())
            #trade_optionbox.set_option_list(options2)
            trade_optionbox2.set_option_list(options2)
        
        #player_option.set_option_list(options)
        
        
        
        events = pygame.event.get()
        
        selected_option = player_option.update(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if roll_button.is_clicked(event) and not game.roll_complete() and not game.is_player_in_jail(p):
                    die.roll()
                    game.set_dice_roll(die.get_rollsum(), die.is_double(), p)
                
                elif buy_button.is_clicked(event):
                    loc = property_dict["locations"][p.get_position()]["name"]
                    if p.is_player_turn(game.get_turn()) and loc not in special_locs:
                        pos = p.get_position()
                        col = property_dict["locations"][pos]["color"]
                        cost = property_dict["locations"][pos]["cost"]
                        p.buy_property(pos, col, cost)
                        break
                        
                elif end_turn_button.is_clicked(event) and game.roll_complete():
                    game.change_turn()
                    switch_turn = True
                    player_option.set_selected_option(game.get_turn())
                    #trade_optionbox2.set_option_list(option_list)
                    
                    
            elif event.type == pygame.QUIT:
                run = False

        
        redrawWindow(WINDOW, p, p2, selected_option)
    pygame.quit()

main()
        

