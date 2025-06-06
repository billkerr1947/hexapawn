import pygame
import sys  # to exit
import settings
#from pawn import Pawn

pygame.init()   # initialise pygame modules
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))   
#create screen surface
pygame.display.set_caption('Hexapawn')
clock = pygame.time.Clock() # create a clock
#self.pawn1 = Pawn()

while True:    
    for event in pygame.event.get():
        # any keyboard or mouse event will activate this loop
        if event.type == pygame.QUIT:
            # pygame.quit()
            sys.exit()
    
    screen.fill(settings.bg_colour)  
    #pawn1.blitme()
    pygame.display.flip()   # updates entire display, must come afer fill(bg_colour)
    clock.tick(60)
    