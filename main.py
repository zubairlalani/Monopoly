import pygame
import os

WIDTH, HEIGHT = 900, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")

WHITE = (255, 255, 255)
Color_line = (255, 0, 0)
FPS = 60

CAR_WIDTH, CAR_HEIGHT = 50, 50
BOARD_IMAGE = pygame.image.load(os.path.join('Assets', 'monopoly.jpg'))
CAR = pygame.image.load(os.path.join('Assets', 'car.png'))
#CAR = pygame.transform.scale(CAR, (CAR_WIDTH, CAR_HEIGHT))
rect = BOARD_IMAGE.get_rect()
rect.center = (WIDTH/2, HEIGHT/2)

def draw_window():
    WINDOW.fill(WHITE)
    WINDOW.blit(BOARD_IMAGE, rect)
    WINDOW.blit(CAR, (675, 700))
    pygame.draw.line(WINDOW, Color_line, (0, 740), (900, 740))
    pygame.draw.line(WINDOW, Color_line, (100, 0), (100, 800))
    pygame.draw.line(WINDOW, Color_line, (800, 0), (800, 800))
    pygame.draw.line(WINDOW, Color_line, (0, 50), (900, 50))
    pygame.display.update()
    
def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
        draw_window()
        
    pygame.quit()


if __name__ == "__main__":
    main()
