import pygame
import sys  # to exit
import settings

pygame.init()   # initialise pygame modules
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))   
#create screen surface
pygame.display.set_caption('Hexapawn')
clock = pygame.time.Clock() # create a clock

# make a dictionary sqNum : pos(x, y)
# all required pawn positions are in this dictionary
boardDict = {1 : (30,320),2 : (180, 320), 3 : (330,320),
             4 : (30, 170), 5 : (180,170),6 : (330, 170),
             7 : (30, 20), 8 : (180,20),9 : (330, 20)
             }

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
    
    WP_startList = [WP1, WP2, WP3]
    BP_startList = [BP1, BP2, BP3]
    for num, P in enumerate(WP_startList):
        screen.blit(P.WP,(P.pos(boardDict, num+1)))   #(image surface WP, positon)
        # blit stands for block image transfer!
        # enumerate to run two variables in for loop!
    for num, P in enumerate(BP_startList):
        screen.blit(P.BP,(P.pos(boardDict, num+7)))
             
    pygame.display.flip()   # updates entire display, must come afer fill(bg_colour)
    clock.tick(60)
    