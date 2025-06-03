import pygame

pygame.init()
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption('Hexapawn')
clock = pygame.time.Clock()

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    clock.tick(60)