import pygame
import os

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
YELLOW = (255, 255, 0)
GREEN = (50, 205, 50)
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
    def __init__(self, name, money, x, y):
        self.name = name
        self.money = money
        self.properties = set()
        self.color_frequency = {}
        
        self.position = 0
        self.x = x
        self.y = y
        
        self.in_jail = False
        self.jail_count = 0
                 
    def move(self, dice_roll):
        temp_pos = self.position
        self.position += dice_roll
        self.position = self.position % 40
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
    
    def property_owned(self, property_id):
        return property_id in self.properties
    
    def make_deposit(self, amount):
        self.money += amount
    
    def pay(self, amount):
        self.money -= amount
        
    def get_position(self):
        return self.position

    def set_position(self, pos, x, y):
        self.position = pos
        self.x = x
        self.y = y
        
    def get_money(self):
        return self.money

    def get_properties(self):
        return self.properties

    def get_color_frequency(self):
        return self.color_frequency
    
    def get_name(self):
        return self.name
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def draw_player_properties(self, WINDOW):
        
        if self.property_owned(1): # Mediterranean Ave.
            pygame.draw.rect(WINDOW, BROWN, pygame.Rect(ROW_ONE_START, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT)) # Filled in rectangle when property is owned
        else:
            pygame.draw.rect(WINDOW, BROWN, pygame.Rect(ROW_ONE_START, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2) # Have only border of rectangle if property is unowned
            
        if self.property_owned(3): # Baltic Ave.
            pygame.draw.rect(WINDOW, BROWN, pygame.Rect(ROW_ONE_START + CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, BROWN, pygame.Rect(ROW_ONE_START + CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
        if self.property_owned(6): # Oriental Ave.
            pygame.draw.rect(WINDOW, LIGHTBLUE, pygame.Rect(ROW_MIDDLE, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, LIGHTBLUE, pygame.Rect(ROW_MIDDLE, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
        if self.property_owned(8): # Vermont Ave.
            pygame.draw.rect(WINDOW, LIGHTBLUE, pygame.Rect(ROW_MIDDLE + CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, LIGHTBLUE, pygame.Rect(ROW_MIDDLE + CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
            
        if self.property_owned(9): # Connecticut Ave.
            pygame.draw.rect(WINDOW, LIGHTBLUE, pygame.Rect(ROW_MIDDLE + 2*CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, LIGHTBLUE, pygame.Rect(ROW_MIDDLE + 2*CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
        if self.property_owned(11): # St. Charles Place
            pygame.draw.rect(WINDOW, PINK, pygame.Rect(ROW_ONE_END, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, PINK, pygame.Rect(ROW_ONE_END, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
            
        if self.property_owned(13): # States Ave.
            pygame.draw.rect(WINDOW, PINK, pygame.Rect(ROW_ONE_END + CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, PINK, pygame.Rect(ROW_ONE_END + CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
            
        if self.property_owned(14): # Virginia Ave.
            pygame.draw.rect(WINDOW, PINK, pygame.Rect(ROW_ONE_END + 2*CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, PINK, pygame.Rect(ROW_ONE_END + 2*CARD_DIST, ROW_ONE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
        if self.property_owned(16): # St. James Place
            pygame.draw.rect(WINDOW, ORANGE, pygame.Rect(ROW_TWO_START, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, ORANGE, pygame.Rect(ROW_TWO_START, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
            
        if self.property_owned(18): # Tennessee Ave.
            pygame.draw.rect(WINDOW, ORANGE, pygame.Rect(ROW_TWO_START + CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, ORANGE, pygame.Rect(ROW_TWO_START + CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
            
        if self.property_owned(19): # New York Ave.
            pygame.draw.rect(WINDOW, ORANGE, pygame.Rect(ROW_TWO_START + 2*CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, ORANGE, pygame.Rect(ROW_TWO_START + 2*CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
        if self.property_owned(21): # Kentucky Ave.
            pygame.draw.rect(WINDOW, RED, pygame.Rect(ROW_MIDDLE, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, RED, pygame.Rect(ROW_MIDDLE, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
            
        if self.property_owned(23): # Indiana Ave.
            pygame.draw.rect(WINDOW, RED, pygame.Rect(ROW_MIDDLE + CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, RED, pygame.Rect(ROW_MIDDLE + CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
            
        if self.property_owned(24): # Illinois Ave.
            pygame.draw.rect(WINDOW, RED, pygame.Rect(ROW_MIDDLE + 2*CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, RED, pygame.Rect(ROW_MIDDLE + 2*CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
        if self.property_owned(26): # Atlantic Ave.
            pygame.draw.rect(WINDOW, YELLOW, pygame.Rect(ROW_TWO_END, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, YELLOW, pygame.Rect(ROW_TWO_END, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
            
        if self.property_owned(27): # Ventnor Ave.
            pygame.draw.rect(WINDOW, YELLOW, pygame.Rect(ROW_TWO_END + CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, YELLOW, pygame.Rect(ROW_TWO_END + CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
            
        if self.property_owned(29): # Marvin Gardens
            pygame.draw.rect(WINDOW, YELLOW, pygame.Rect(ROW_TWO_END + 2*CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, YELLOW, pygame.Rect(ROW_TWO_END + 2*CARD_DIST, ROW_TWO_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
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
        
        if self.property_owned(31): # Pacific Ave.
            pygame.draw.rect(WINDOW, GREEN, pygame.Rect(ROW_MIDDLE, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, GREEN, pygame.Rect(ROW_MIDDLE, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
            
        if self.property_owned(32): # North Carolina Ave.
            pygame.draw.rect(WINDOW, GREEN, pygame.Rect(ROW_MIDDLE + CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, GREEN, pygame.Rect(ROW_MIDDLE + CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
            
        if self.property_owned(34): # Pennsylvania Ave.
            pygame.draw.rect(WINDOW, GREEN, pygame.Rect(ROW_MIDDLE + 2*CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, GREEN, pygame.Rect(ROW_MIDDLE + 2*CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
        if self.property_owned(37): # Park Place
            pygame.draw.rect(WINDOW, DARKBLUE, pygame.Rect(ROW_THREE_END, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, DARKBLUE, pygame.Rect(ROW_THREE_END, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
            
        if self.property_owned(39): # Boardwalk
            pygame.draw.rect(WINDOW, DARKBLUE, pygame.Rect(ROW_THREE_END + CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, DARKBLUE, pygame.Rect(ROW_THREE_END + CARD_DIST, ROW_THREE_Y, OWNED_PROPERTY_WIDTH, OWNED_PROPERTY_HEIGHT), 2)
        
        
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
    