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
        self.screenRect = self.screen.get_rect()
        self.WPimg = pygame.image.load('images/whitePawn.png') #image surface!
        self.WPimgRect = self.WPimg.get_rect() # for mouse event detection
        self.BPimg = pygame.image.load('images/blackPawn.png')
        self.BPimgRect = self.BPimg.get_rect() 
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

print(WP1.WPimgRect.bottomleft)
print(WP1.screenRect.bottomleft)
print(WP1.screenRect.center)
#WP1.WPimgRect.bottomleft = screenRect.bottomleft
def position (pieceList ):
    for num, piece in enumerate(pieceList):
        if piece == WP1:
            WP1.WPimgRect.topleft = WP1.pos(boardDict, num+1) #(30, 320) WP1.screenRect.bottomleft
            screen.blit(WP1.WPimg,(WP1.WPimgRect)) #  #(image surface WP, positon)
                  # blit stands for block image transfer!
        # enumerate to run two variables in for loop!
        if piece == WP2:
            WP2.WPimgRect.topleft = WP2.pos(boardDict, num+1)
            screen.blit(WP2.WPimg,(WP2.WPimgRect))
        if piece == WP3:
            WP3.WPimgRect.topleft = WP3.pos(boardDict, num+1)
            screen.blit(WP3.WPimg,(WP3.WPimgRect))
        if piece == BP1:
            screen.blit(BP1.BPimg,(BP1.pos(boardDict, num+1)))
        if piece == BP2:
            screen.blit(BP2.BPimg,(BP2.pos(boardDict, num+1)))
        if piece == BP3:
            screen.blit(BP3.BPimg,(BP3.pos(boardDict, num+1)))
            
while True:    
    for event in pygame.event.get():
        # any keyboard or mouse event will activate this loop
        if event.type == pygame.QUIT:
            # pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if WP1.WPimgRect.collidepoint(pygame.mouse.get_pos()):
                print ('Y')
            print ("mouse down")
            print(pygame.mouse.get_pos())
    
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
    #print(WP1.WPimgRect)
    
    pygame.display.flip()   # updates entire display, must come afer fill(bg_colour)
    clock.tick(60)
    

    