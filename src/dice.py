import pygame
import random

# Define important colors
FONT = pygame.font.Font(None, 30)
SMALLFONT = pygame.font.Font(None, 20)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (155, 155, 155)
ORANGE = (255, 180, 0)
BUTTON_COLOR = (204, 255, 255)

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
    
    def draw_dice(self, WINDOW):
        pygame.draw.rect(WINDOW, self.color, self.dice_rect, 2)
        pygame.draw.rect(WINDOW, self.color, self.dice2_rect, 2)
        WINDOW.blit(self.surface, self.text_rect)
        WINDOW.blit(self.surface2, self.text2_rect)
    
    def get_rollsum(self):
        return int(self.dice_one) + int(self.dice_two)
    
    def get_dice_one(self):
        return self.dice_one
    
    def get_dice_two(self):
        return self.dice_two
    
    def set_dice(self, d1, d2):
        self.dice_one = d1
        self.dice_two = d2
        self.surface = FONT.render(self.dice_one, True, ORANGE)
        self.surface2 = FONT.render(self.dice_two, True, ORANGE)
        #print(self.dice_one + " " + self.dice_two)