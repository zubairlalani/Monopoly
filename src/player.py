import pygame
import os
import gui_components as gui
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

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
LIGHTBLUE = (179, 242, 255)
PINK = (255, 0, 255)
RED = (255, 0, 0)
DARK_RED = (179,0,30)
YELLOW = (255, 255, 0)
GREEN = (50, 205, 50)
DARK_GREEN = (0,102,51)
DARKBLUE = (0, 34, 204)
GREY = (155, 155, 155)
ORANGE = (255, 180, 0)

WATER_DROPLET_IMAGE = pygame.image.load(os.path.join('Assets', 'water_droplet.png'))
LIGHTBULB_IMAGE = pygame.image.load(os.path.join('Assets', 'lightbulb.png'))
RAILROAD_IMAGE = pygame.image.load(os.path.join('Assets', 'railroad_icon.jpeg'))
railroad_icon_rect = RAILROAD_IMAGE.get_rect()

class Player:
    """Single player for a monopoly game
    """
    owned_properties = set()
    def __init__(self, name, money, x, y, turn_number):
        self.name = name
        self.money = money
        self.properties = set()
        self.color_frequency = {}
        self.houses = {}
        self.turn_number = turn_number
        
        self.position = 0
        self.x = x
        self.y = y
        
        self.in_jail = False
        self.jail_turns = 0
                 
    def move(self, dice_roll):
        temp_pos = self.position
        self.position += dice_roll
        self.position = self.position % 40
        if temp_pos > self.position:
            self.make_deposit(200) # passed GO so player earns $200 salary
            
        while temp_pos != self.position:
            if temp_pos < 10:
                self.x += 56 * -1
                self.y = 670
            elif temp_pos >= 10 and temp_pos < 20:
                self.y += 56 * -1
                self.x = 70
            elif temp_pos >= 20 and temp_pos < 30:
                self.x += 56
                self.y = 90
            elif temp_pos >= 30 and temp_pos <= 40:
                self.y += 56
                self.x = 640
            temp_pos += 1
            temp_pos = temp_pos % 40
    
    def buy_property(self, property_id, property_color, price):
        if self.money - price >= 0 and property_id not in Player.owned_properties:
            self.properties.add(property_id)
            Player.owned_properties.add(property_id)
            if property_color in self.color_frequency:
                self.color_frequency[property_color] += 1
            else:
                self.color_frequency[property_color] = 1
            
            self.money -= price
    
    def buy_house(self, property_id, property_color, price, color_property, color_property2=None):
        if self.money - price >= 0: # Make sure that player has the funds to buy the house
            
            if property_id in self.houses:
                if color_property2 != None:
                    if (self.get_property_house_amount(property_id) - self.get_property_house_amount(color_property)) < 1 \
                    and (self.get_property_house_amount(property_id) - self.get_property_house_amount(color_property2)) < 1 and self.get_property_house_amount(property_id) < 5:
                        self.houses[property_id] += 1 # Maps properties to the amount of houses they have
                        self.money -= price
                elif (self.get_property_house_amount(property_id) - self.get_property_house_amount(color_property)) < 1 and self.get_property_house_amount(property_id) < 5:
                        self.houses[property_id] += 1
                        self.money -= price
            else:
                self.houses[property_id] = 1
                self.money -= price
            
              
    def property_owned(self, property_id):
        return property_id in self.properties
    
    def make_deposit(self, amount):
        self.money += amount
    
    def pay(self, amount):
        self.money -= amount
    
    def has_color_group(self, color):
        print(self.color_frequency)
        if color in self.color_frequency:
            if (color == "Brown" or color == "Dark Blue") and self.color_frequency[color] == 2:
                return True
            elif self.color_frequency[color] == 3:
                return True
        return False
    
    def get_property_house_amount(self, property_id):
        if property_id not in self.houses:
            return 0
        return self.houses[property_id]
    
    def get_position(self):
        return self.position

    def set_position(self, pos, x, y):
        self.position = pos
        self.x = x
        self.y = y
    
    def go_to_jail(self):
        self.set_position(10, 70, 680)
        self.in_jail = True
    
    def leave_jail(self):
        self.in_jail = False
        self.jail_turns = 0
    
    def increment_jail(self):
        if self.in_jail:
            self.jail_turns += 1
    
    def get_jail_count(self):
        return self.jail_turns
    
    def is_in_jail(self):
        return self.in_jail
    
    def is_player_turn(self, turn):
        if self.turn_number == turn:
            return True
        return False
    
    def get_turn_number(self):
        return self.turn_number
    
    def get_money(self):
        return self.money

    def get_properties(self):
        return self.properties
    
    def get_houses(self):
        return self.houses
    def get_color_frequency(self):
        return self.color_frequency
    
    def get_name(self):
        return self.name
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def draw_houses(self, window, property_id, rect):
        if self.get_property_house_amount(property_id) > 0 and self.get_property_house_amount(property_id) < 5:
                #gui.draw_text(WINDOW, str(self.get_property_house_amount(1)), FONT, GREEN, rect.centerx, rect.centery, True)
                house = pygame.Rect(rect.x, rect.y, OWNED_PROPERTY_WIDTH/4, OWNED_PROPERTY_WIDTH/4)
                for x in range(self.get_property_house_amount(property_id)):
                    pygame.draw.rect(window, DARK_GREEN, house)
                    house.topleft = house.topright
        elif self.get_property_house_amount(property_id) == 5:
            hotel = pygame.Rect(rect.x, rect.y, OWNED_PROPERTY_WIDTH, 5)
            pygame.draw.rect(window, DARK_RED, hotel)
        
    def draw_player_properties(self, WINDOW, FONT):
        
        rect = pygame.Rect(ROW_ONE_START, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(1): # Mediterranean Ave.
            pygame.draw.rect(WINDOW, BROWN, rect) # Filled in rectangle when property is owned
            self.draw_houses(WINDOW, 1, rect)
        else:
            pygame.draw.rect(WINDOW, BROWN, rect, 2) # Have only border of rectangle if property is unowned
        
        rect = pygame.Rect(ROW_ONE_START + CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(3): # Baltic Ave.
            pygame.draw.rect(WINDOW, BROWN, rect)
            self.draw_houses(WINDOW, 3, rect)
        else:
            pygame.draw.rect(WINDOW, BROWN, rect, 2)
        
        rect = pygame.Rect(ROW_MIDDLE, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(6): # Oriental Ave.
            pygame.draw.rect(WINDOW, LIGHTBLUE, rect)
            self.draw_houses(WINDOW, 6, rect)
        else:
            pygame.draw.rect(WINDOW, LIGHTBLUE, rect, 2)
        
        rect = pygame.Rect(ROW_MIDDLE + CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(8): # Vermont Ave.
            pygame.draw.rect(WINDOW, LIGHTBLUE, rect)
            self.draw_houses(WINDOW, 8, rect)
        else:
            pygame.draw.rect(WINDOW, LIGHTBLUE, rect, 2)
            
        rect = pygame.Rect(ROW_MIDDLE + 2*CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(9): # Connecticut Ave.
            pygame.draw.rect(WINDOW, LIGHTBLUE, rect)
            self.draw_houses(WINDOW, 9, rect)
        else:
            pygame.draw.rect(WINDOW, LIGHTBLUE, rect, 2)
        
        rect = pygame.Rect(ROW_ONE_END, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(11): # St. Charles Place
            pygame.draw.rect(WINDOW, PINK, rect)
            self.draw_houses(WINDOW, 11, rect)
        else:
            pygame.draw.rect(WINDOW, PINK, rect, 2)
        
        rect = pygame.Rect(ROW_ONE_END + CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(13): # States Ave.
            pygame.draw.rect(WINDOW, PINK, rect)
            self.draw_houses(WINDOW, 13, rect)
        else:
            pygame.draw.rect(WINDOW, PINK, rect, 2)
        
        rect = pygame.Rect(ROW_ONE_END + 2*CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(14): # Virginia Ave.
            pygame.draw.rect(WINDOW, PINK, rect)
            self.draw_houses(WINDOW, 14, rect)
        else:
            pygame.draw.rect(WINDOW, PINK, rect, 2)
        
        rect = pygame.Rect(ROW_TWO_START, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(16):  # St. James Place
            pygame.draw.rect(WINDOW, ORANGE, rect)
            self.draw_houses(WINDOW, 16, rect)
        else:
            pygame.draw.rect(WINDOW, ORANGE, rect, 2)
           
        rect =  pygame.Rect(ROW_TWO_START + CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(18): # Tennessee Ave.
            pygame.draw.rect(WINDOW, ORANGE, rect)
            self.draw_houses(WINDOW, 18, rect)
        else:
            pygame.draw.rect(WINDOW, ORANGE, rect, 2)
        
        rect =  pygame.Rect(ROW_TWO_START + 2*CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(19): # New York Ave.
            pygame.draw.rect(WINDOW, ORANGE, rect)
            self.draw_houses(WINDOW, 19, rect)
        else:
            pygame.draw.rect(WINDOW, ORANGE, rect, 2)
        
        rect = pygame.Rect(ROW_MIDDLE, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(21): # Kentucky Ave.
            pygame.draw.rect(WINDOW, RED, rect)
            self.draw_houses(WINDOW, 21, rect)
        else:
            pygame.draw.rect(WINDOW, RED, rect, 2)
        
        rect = pygame.Rect(ROW_MIDDLE + CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(23): # Indiana Ave.
            pygame.draw.rect(WINDOW, RED, rect)
            self.draw_houses(WINDOW, 23, rect)
        else:
            pygame.draw.rect(WINDOW, RED, rect, 2)
        
        rect = pygame.Rect(ROW_MIDDLE + 2*CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(24): # Illinois Ave.
            pygame.draw.rect(WINDOW, RED, rect)
            self.draw_houses(WINDOW, 24, rect)
        else:
            pygame.draw.rect(WINDOW, RED, rect, 2)
        
        rect = pygame.Rect(ROW_TWO_END, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(26): # Atlantic Ave.
            pygame.draw.rect(WINDOW, YELLOW, rect)
            self.draw_houses(WINDOW, 26, rect)
        else:
            pygame.draw.rect(WINDOW, YELLOW, rect, 2)
        
        rect = pygame.Rect(ROW_TWO_END + CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(27): # Ventnor Ave.
            pygame.draw.rect(WINDOW, YELLOW, rect)
            self.draw_houses(WINDOW, 27, rect)
        else:
            pygame.draw.rect(WINDOW, YELLOW, rect, 2)
        
        rect = pygame.Rect(ROW_TWO_END + 2*CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(29): # Marvin Gardens
            pygame.draw.rect(WINDOW, YELLOW, rect)
            self.draw_houses(WINDOW, 29, rect)
        else:
            pygame.draw.rect(WINDOW, YELLOW, rect, 2)
        
        #UTILITIES
        if self.property_owned(12): # Electric Community
            electric_community_rect = pygame.Rect(ROW_THREE_START, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
            lightbulb_rect = LIGHTBULB_IMAGE.get_rect()
            lightbulb_rect.center = electric_community_rect.center
            pygame.draw.rect(WINDOW, WHITE, electric_community_rect)
            WINDOW.blit(LIGHTBULB_IMAGE, lightbulb_rect)
        else:
            electric_community_rect = pygame.Rect(ROW_THREE_START, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
            pygame.draw.rect(WINDOW, WHITE, electric_community_rect, 2)
            
        if self.property_owned(28): # Water Works
            water_works_rect = pygame.Rect(ROW_THREE_START + CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
            droplet_rect = WATER_DROPLET_IMAGE.get_rect()
            droplet_rect.center = water_works_rect.center
            pygame.draw.rect(WINDOW, WHITE, water_works_rect)
            WINDOW.blit(WATER_DROPLET_IMAGE, droplet_rect)
        else:
            water_works_rect = pygame.Rect(ROW_THREE_START + CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
            pygame.draw.rect(WINDOW, WHITE, water_works_rect, 2)
        
        rect = pygame.Rect(ROW_MIDDLE, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(31): # Pacific Ave.
            pygame.draw.rect(WINDOW, GREEN, rect)
            self.draw_houses(WINDOW, 31, rect)
        else:
            pygame.draw.rect(WINDOW, GREEN, rect, 2)
        
        rect = pygame.Rect(ROW_MIDDLE + CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(32): # North Carolina Ave.
            pygame.draw.rect(WINDOW, GREEN, rect)
            self.draw_houses(WINDOW, 32, rect)
        else:
            pygame.draw.rect(WINDOW, GREEN, rect, 2)
        
        rect = pygame.Rect(ROW_MIDDLE + 2*CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(34): # Pennsylvania Ave.
            pygame.draw.rect(WINDOW, GREEN, rect)
            self.draw_houses(WINDOW, 34, rect)
        else:
            pygame.draw.rect(WINDOW, GREEN, rect, 2)
        
        rect = pygame.Rect(ROW_THREE_END, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(37): # Park Place
            pygame.draw.rect(WINDOW, DARKBLUE, rect)
            self.draw_houses(WINDOW, 37, rect)
        else:
            pygame.draw.rect(WINDOW, DARKBLUE, rect, 2)
         
        rect = pygame.Rect(ROW_THREE_END + CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
        if self.property_owned(39): # Boardwalk
            pygame.draw.rect(WINDOW, DARKBLUE, rect)
            self.draw_houses(WINDOW, 39, rect)
        else:
            pygame.draw.rect(WINDOW, DARKBLUE, rect, 2)
        
        
        #RAILROADS
        if self.property_owned(5): # Reading Railroad
            reading_railroad_rect = pygame.Rect(ROW_MIDDLE - CARD_DIST/2, ROW_FOUR_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
            pygame.draw.rect(WINDOW, GREY, reading_railroad_rect)
            railroad_icon_rect.center = reading_railroad_rect.center
            WINDOW.blit(RAILROAD_IMAGE, railroad_icon_rect)
        else:
            reading_railroad_rect = pygame.Rect(ROW_MIDDLE - CARD_DIST/2, ROW_FOUR_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
            pygame.draw.rect(WINDOW, GREY, reading_railroad_rect, 2)
            
        if self.property_owned(15): # Pennsylvania Railroad
            penn_railroad_rect = pygame.Rect(ROW_MIDDLE - CARD_DIST/2 + CARD_DIST, ROW_FOUR_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
            pygame.draw.rect(WINDOW, GREY, penn_railroad_rect)
            railroad_icon_rect.center = penn_railroad_rect.center
            WINDOW.blit(RAILROAD_IMAGE, railroad_icon_rect)
        else:
            penn_railroad_rect = pygame.Rect(ROW_MIDDLE - CARD_DIST/2 + CARD_DIST, ROW_FOUR_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
            pygame.draw.rect(WINDOW, GREY, penn_railroad_rect, 2)
            
        if self.property_owned(25): # B & O Railroad
            bo_railraod = pygame.Rect(ROW_MIDDLE - CARD_DIST/2 + 2*CARD_DIST, ROW_FOUR_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
            pygame.draw.rect(WINDOW, GREY, bo_railraod)
            railroad_icon_rect.center = bo_railraod.center
            WINDOW.blit(RAILROAD_IMAGE, railroad_icon_rect)
        else:
            bo_railraod = pygame.Rect(ROW_MIDDLE - CARD_DIST/2 + 2*CARD_DIST, ROW_FOUR_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
            pygame.draw.rect(WINDOW, GREY, bo_railraod, 2)
            
        if self.property_owned(35): # Short Line
            short_line = pygame.Rect(ROW_MIDDLE - CARD_DIST/2 + 3*CARD_DIST, ROW_FOUR_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
            pygame.draw.rect(WINDOW, GREY, short_line)
            railroad_icon_rect.center = short_line.center
            WINDOW.blit(RAILROAD_IMAGE, railroad_icon_rect)
        else:
            short_line = pygame.Rect(ROW_MIDDLE - CARD_DIST/2 + 3*CARD_DIST, ROW_FOUR_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)
            pygame.draw.rect(WINDOW, GREY, short_line, 2)
    