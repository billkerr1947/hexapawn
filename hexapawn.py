import pygame
import sys  # to exit
import settings
from settings import boardDict
import random

pygame.init()   # initialise pygame modules
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))   
#create screen surface
pygame.display.set_caption('Hexapawn')
clock = pygame.time.Clock() # create a clock

class Pawn:
    """make a class since want six pawns, 3 white, 3 black"""
    def __init__(self):
        self.screen = screen    # give pawns access to hexapawn screen
        self.screenRect = self.screen.get_rect() # for positioning pawns later
        self.WPimg = pygame.image.load('images/whitePawn.png') #image surface!
        self.WPimgRect = self.WPimg.get_rect() # rect for mouse event detection
        self.BPimg = pygame.image.load('images/blackPawn.png')
        self.BPimgRect = self.BPimg.get_rect() 
        self.WPSelected = pygame.image.load('images/whitePawnSelected.png')

#    pawn pos method -> input boardDict, num -> return board position (x, y)
    def pos(self, boardDict, num ):
        return boardDict[num]

class RedDot:
    """ Need 2 red dots sometimes"""
    def __init__(self):
        self.screen = screen
        self.redDotImg = pygame.image.load('images/redDot.png')
        self.redDotRect = self.redDotImg.get_rect()

#create WP instances 
# do I need to number them, boardDict key is an ID?  
WP = Pawn()
#WP = Pawn()
#WP = Pawn()
#create BP instances
BP = Pawn()
BP = Pawn()
BP = Pawn()
# create red dot instances
RD1 = RedDot()
RD2 = RedDot()
boole = False
flag = 1

# position and show rect/images in pieceList positions
def position (pieceList ):
    for num, piece in enumerate(pieceList):
        # enumerate indexes the for loop!
        if piece == WP:
            WP.WPimgRect.topleft = WP.pos(boardDict, num) 
            #(30, 320) position pawn rect by boardDict values
            screen.blit(WP.WPimg,(WP.WPimgRect))  #(image surface WP, positon)
                  # blit stands for block image transfer!
            if boole: #boole set to True when WP clicked
                screen.blit(WP.WPSelected,(WP.WPimgRect)) # selected WP image
                RD1.redDotRect.topleft = (WP.pos(boardDict, num + 3)) 
                RD2.redDotRect.topleft = (WP.pos(boardDict, num + 4))
                # redDot rect plus 3 from WP
                screen.blit(RD1.redDotImg,(RD1.redDotRect)) # show redDot img
                screen.blit(RD2.redDotImg,(RD2.redDotRect))
        
        if piece == BP:
            screen.blit(BP.BPimg,(BP.pos(boardDict, num)))
        if piece == BP:
            screen.blit(BP.BPimg,(BP.pos(boardDict, num)))
        if piece == BP:
            screen.blit(BP.BPimg,(BP.pos(boardDict, num)))

#setup up from and to lists for WP
fromList =[]
toList = []
pieceList =[None ,None, None, None ,None, WP,None, BP,BP ]
def to_from (pieceList):
    for num in range(6):
        if pieceList[num] == WP:
            if pieceList[num+3] == None:
                fromList.append(pieceList.index(WP))
                toList.append(pieceList.index(WP)+3)
            if pieceList.index(WP) % 3 > 0:
                if pieceList[num+2] == BP:
                    fromList.append(pieceList.index(WP))
                    toList.append(pieceList.index(BP))
            if pieceList.index(WP) % 3 < 2:
                if pieceList[num+4] == BP:
                    fromList.append(pieceList.index(WP))
                    toList.append(pieceList.index(BP))
            
    print (fromList)        
    print (toList)

to_from(pieceList)

while True:    
    for event in pygame.event.get():
        # any keyboard or mouse event will activate this loop
        if event.type == pygame.QUIT:
            # pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if WP.WPimgRect.collidepoint(pygame.mouse.get_pos()):
                begin = pieceList.index(WP)    # board pos of this WP
                # True if mouse clicks inside WPimgRect
                boole = True #turn on redDot
            if RD1.redDotRect.collidepoint(pygame.mouse.get_pos()):
                boole = False   #turn off redDot
                end = begin + 3     # +3 for normal move
                flag = 2    # move piece to new positions
            if RD2.redDotRect.collidepoint(pygame.mouse.get_pos()):
                boole = False   #turn off redDot
                end = begin + 4 #capture to right
                flag = 2    # move piece to new positions
        
        
            #print(pygame.mouse.get_pos())
        
    screen.fill(settings.bg_colour)  
    # draw line grid on screen (must be in while loop)
    pygame.draw.line(screen,"red",start_pos=(150,0),end_pos=(150,450))
    pygame.draw.line(screen,"red",start_pos=(300,0),end_pos=(300,450))
    pygame.draw.line(screen,"red",start_pos=(0,150),end_pos=(450,150))
    pygame.draw.line(screen,"red",start_pos=(0,300),end_pos=(450,300))
    
    if flag == 1:
        # flag = 1 in preamble
        # start position
        pieceList =[None, WP ,None , None, None, None,  BP, BP, BP ]
    if flag == 2:
        #move WP1 from begin pos to end pos
        pieceList[begin] = None
        pieceList[end] = WP
        #pieceList is now changed
        #move black pawn BP from begin pos to end pos
        # how to choose one from all possibles? random from list
        Bfrom = [7,8]   # possible BP start squares, BP & 3
        choice = random.choice(Bfrom)   #choose one of the squares
        Bto = [4,5]     # possible BP end squares
        n = Bfrom.index(choice) # index number of choice
        pieceList[choice] = None    #remove BP from choice sq
        to = Bto[n] # number of desired end sq for BP
        pieceList[to] = BP # move BP to end sq
        boole = True # redDot back on
        flag = 3    # jump out 
        # reset clock to 1!?!?
                
    position(pieceList)
    #print(pieceList.index(WP1))
        
    pygame.display.flip()   # updates entire display, must come afer fill(bg_colour)
    clock.tick(1)
    

    