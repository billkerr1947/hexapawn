import pygame
import sys  # to exit
import settings
from settings import boardDict

pygame.init()   # initialise pygame modules
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))   
#create screen surface
pygame.display.set_caption('Hexapawn')
clock = pygame.time.Clock() # create a clock

class Pawn:
    """make a class since want six pawns, 3 white, 3 black"""
    def __init__(self):
        self.screen = screen    # pawn access to hexapawn screen
        self.WP = pygame.image.load('images/whitePawn.png') #image surface!
        self.BP = pygame.image.load('images/blackPawn.png')
        self.WPSelected = pygame.image.load('images/whitePawnSelected.png')

#    pawn method -> input square ID, return position
    def pos(self, boardDict, num ):
        return boardDict[num]

#create WP instances   
WP1 = Pawn()
WP2 = Pawn()
WP3 = Pawn()
#create BP instances
BP1 = Pawn()
BP2 = Pawn()
BP3 = Pawn()

def position (pieceList ):
    for num, piece in enumerate(pieceList):
        if piece == WP1:
            screen.blit(WP1.WP,(WP1.pos(boardDict, num+1)))   #(image surface WP, positon)
        # blit stands for block image transfer!
        # enumerate to run two variables in for loop!
        if piece == WP2:
            screen.blit(WP2.WP,(WP2.pos(boardDict, num+1)))
        if piece == WP3:
            screen.blit(WP3.WP,(WP3.pos(boardDict, num+1)))
        if piece == BP1:
            screen.blit(BP1.BP,(BP1.pos(boardDict, num+1)))
        if piece == BP2:
            screen.blit(BP2.BP,(BP2.pos(boardDict, num+1)))
        if piece == BP3:
            screen.blit(BP3.BP,(BP3.pos(boardDict, num+1)))
            
while True:    
    for event in pygame.event.get():
        # any keyboard or mouse event will activate this loop
        if event.type == pygame.QUIT:
            # pygame.quit()
            sys.exit()
    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                print('key press')  #works
                #restart (WP_startList, BP_startList )   #running but can't see it?
        
    screen.fill(settings.bg_colour)  
    # draw line grid on screen (must be in while loop)
    pygame.draw.line(screen,"red",start_pos=(150,0),end_pos=(150,450))
    pygame.draw.line(screen,"red",start_pos=(300,0),end_pos=(300,450))
    pygame.draw.line(screen,"red",start_pos=(0,150),end_pos=(450,150))
    pygame.draw.line(screen,"red",start_pos=(0,300),end_pos=(450,300))
    
    pieceList =[WP1, WP2, None, None, None, WP3, BP1, BP2, BP3 ]
    position(pieceList)
    
    pygame.display.flip()   # updates entire display, must come afer fill(bg_colour)
    clock.tick(60)
    