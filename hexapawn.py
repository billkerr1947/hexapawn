import pygame
import sys  # to exit

pygame.init()   # initialise pygame modules
screen = pygame.display.set_mode((300, 300))    #create screen surface
pygame.display.set_caption('Hexapawn')
clock = pygame.time.Clock() # create a clock
bg_colour = (230,230,230)   #bg colour value

while True:    
    for event in pygame.event.get():
        # any keyboard or mouse event will activate this loop
        if event.type == pygame.QUIT:
            # pygame.quit()
            sys.exit()
    
    screen.fill(bg_colour)  
    pygame.display.flip()   # updates entire display, must come afer fill(bg_colour)
    clock.tick(60)
    