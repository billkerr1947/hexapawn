import pygame
import sys  # to exit
import settings

pygame.init()   # initialise pygame modules
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))   
#create screen surface
pygame.display.set_caption('Hexapawn')
clock = pygame.time.Clock() # create a clock

class Pawn:
    """make a class since want six pawns"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)   # pawn position
        self.screen = screen    # pawn access to hexapawn screen
        self.pawn_image_white = pygame.image.load('images/whitePawn.png')
        self.pawn_image_black = pygame.image.load('images/blackPawn.png')
        self.pawn_rect_white = self.pawn_image_white.get_rect()   # the image needs a rect
        self.pawn_rect_black = self.pawn_image_black.get_rect()   # the image needs a rect

# make a dictionary pawn_init_pos
boardDict = {1 : (25,300),2 : (175, 300), 3 : (325,300),4 : (25, 10), 5 : (175,10),6 : (325, 10),}
#for loop here?
pos1 = boardDict[1]
pos2 = boardDict[2]
pos3 = boardDict[3]
pos4 = boardDict[4]
pos5 = boardDict[5]
pos6 = boardDict[6]

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
    #screen.blits(blit_sequence=(pawn1.pawn_image,(pawn1.pos)), (pawn2.pawn_image,(100,150)))   #(pawn image, x,y pos from top left)
    screen.blit(pawn1.pawn_image_white,(pawn1.pos))
    screen.blit(pawn2.pawn_image_white,(pawn2.pos))   #(pawn image, x,y pos from top left)
    screen.blit(pawn3.pawn_image_white,(pawn3.pos))   #(pawn image, x,y pos from top left)
    screen.blit(pawn4.pawn_image_black,(pawn4.pos)) 
    screen.blit(pawn5.pawn_image_black,(pawn5.pos))
    screen.blit(pawn6.pawn_image_black,(pawn6.pos)) #(pawn image, x,y pos from top left)
    pygame.display.flip()   # updates entire display, must come afer fill(bg_colour)
    clock.tick(60)
    