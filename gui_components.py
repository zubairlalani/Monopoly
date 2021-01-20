import pygame

class Button:
    def __init__(self, window, text, font, fontsize, textcolor, rect, color):
        self.text = text
        self.rect = rect
        self.color = color
        self.window = window
        #buttonfont = pygame.font.SysFont('Comic Sans MS', fontsize)
        self.surface = font.render(self.text, True, textcolor)
        self.text_rect = self.surface.get_rect()
        self.text_rect.center = self.rect.center
        self.clicked = False
        
    def draw(self):
        pygame.draw.rect(self.window, self.color, self.rect, border_radius=10)
        self.window.blit(self.surface, self.text_rect)
    
    def release(self):
        self.clicked = False
    
    def is_clicked(self, event):
        if self.rect.collidepoint(event.pos):
            return True
        return False
    
def draw_text(window, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    window.blit(text_surface, text_rect)