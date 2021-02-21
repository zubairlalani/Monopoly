import pygame

class Button:
    
    
    def __init__(self, window, text, font, textcolor, rect, color):
        self.text = text
        self.rect = rect
        self.color = color
        self.window = window
        #buttonfont = pygame.font.SysFont('Comic Sans MS', fontsize)
        self.surface = font.render(self.text, True, textcolor)
        self.text_rect = self.surface.get_rect()
        self.text_rect.center = self.rect.center
        
    def draw(self):
        pygame.draw.rect(self.window, self.color, self.rect, border_radius=10)
        self.window.blit(self.surface, self.text_rect)
    
    def is_clicked(self, event):
        if self.rect.collidepoint(event.pos):
            return True
        return False

class OptionBox():
    

    def __init__(self, x, y, w, h, color, highlight_color, font, option_list, selected = 0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        print(self.option_list)
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        white = (255, 255, 255)
        black = (0, 0, 0)
        pygame.draw.rect(surf, self.highlight_color if self.menu_active else self.color, self.rect)
        pygame.draw.rect(surf, white, self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, black)
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, black)
                surf.blit(msg, msg.get_rect(center = rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(surf, white, outer_rect, 2)

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    return self.active_option
        return self.selected
    
    def set_selected_option(self, index):
        self.selected = index
    
    def get_option_list(self):
        return self.option_list
    
    def set_option_list(self, option_list):
        self.option_list = option_list
    
    def print_option_list(self):
        print(self.option_list)
    
    def get_selected_option(self):
        return self.option_list[self.selected]

def draw_text(window, text, font, color, x, y, centered):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if centered:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    window.blit(text_surface, text_rect)
    