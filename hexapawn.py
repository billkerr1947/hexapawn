import pygame
import sys  # to exit
import settings

pygame.init()   # initialise pygame modules
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))   
#create screen surface
pygame.display.set_caption('Hexapawn')
clock = pygame.time.Clock() # create a clock

class Pawn:
    """make a class since want six pawns, 3 white, 3 black"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)   # pawn position
        self.screen = screen    # pawn access to hexapawn screen
        self.pawn_image_white = pygame.image.load('images/whitePawn.png')
        self.pawn_image_black = pygame.image.load('images/blackPawn.png')
        # put selected white image here too!
        self.pawn_image_white_selected = pygame.image.load('images/whitePawnSelected.png')
        self.pawn_rect_white = self.pawn_image_white.get_rect()   # the image needs a rect
        self.pawn_rect_black = self.pawn_image_black.get_rect()   # the image needs a rect

# make a dictionary pawn_init_pos
boardDict = {1 : (25,320),2 : (175, 320), 3 : (325,320),4 : (25, 20), 5 : (175,20),6 : (325, 20),}
#for loop here?
pos1 = boardDict[1] #tuple (25,320)
pos2 = boardDict[2]
pos3 = boardDict[3]
pos4 = boardDict[4]
pos5 = boardDict[5]
pos6 = boardDict[6]
# create pawn instances
pawn1 =  Pawn (*pos1) #unpacking tuple, boardDict[1] fails, why?
pawn2 = Pawn (*pos2)
pawn3 = Pawn (*pos3)
pawn4 = Pawn (*pos4)
pawn5 = Pawn (*pos5)
pawn6 = Pawn (*pos6)
 
while True:    
    for event in pygame.event.get():
        # any keyboard or mouse event will activate this loop
        if event.type == pygame.QUIT:
            # pygame.quit()
            sys.exit()
    
    screen.fill(settings.bg_colour)  
    # draw line grid on screen (must be in while loop)
    pygame.draw.line(screen,"red",start_pos=(150,0),end_pos=(150,450))
    pygame.draw.line(screen,"red",start_pos=(300,0),end_pos=(300,450))
    pygame.draw.line(screen,"red",start_pos=(0,150),end_pos=(450,150))
    pygame.draw.line(screen,"red",start_pos=(0,300),end_pos=(450,300))
   
    # display images using lists and for loops
    pawn_list_W = [pawn1, pawn2, pawn3]
    pawn_list_B = [pawn4, pawn5, pawn6]
    for pawn in pawn_list_W:    
        screen.blit(pawn.pawn_image_white,(pawn.pos))
    for pawn in pawn_list_B:    
        screen.blit(pawn.pawn_image_black,(pawn.pos))
    
    pygame.display.flip()   # updates entire display, must come afer fill(bg_colour)
    clock.tick(60)
    