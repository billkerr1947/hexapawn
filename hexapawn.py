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
        self.WPflag = False

#    pawn pos method -> input boardDict, num -> return board position (x, y)
    def pos(self, boardDict, num ):
        return boardDict[num]

class RedDot:
    """ Need 2 red dots sometimes"""
    def __init__(self):
        self.screen = screen
        self.redDotImg = pygame.image.load('images/redDot.png')
        self.redDotRect = self.redDotImg.get_rect()

# make 3 instances of the WP
WP1=Pawn()
WP2=Pawn()
WP3=Pawn()
# WP list
WPList =[WP1,WP2,WP3]

#create BP instances
BP = Pawn()
# create red dot instances
RD1 = RedDot()
RD2 = RedDot()
#boole = False
#Flag = False

#pieceDict shows pieces on their board positions
pieceDict ={0:WP1, 1:None ,2:WP2, 3:None, 4:WP3, 5:None,6:BP, 7:BP, 8:BP }

# pieces_show code will show the pieces when run in the while loop!
# excellent code here solving problems encountered
def pieces_show(pieceDict):
    for key in pieceDict:
        for num, WP in enumerate(WPList):
                if pieceDict[key] == WPList[num]:
                    WP.WPimgRect.topleft = WP.pos(boardDict, key) 
                    #position pawn rect by boardDict values
                    screen.blit(WP.WPimg,(WP.WPimgRect))  #(image surface WP, positon)
                    if WP.WPflag:    # true when a WP rect clicked
                        screen.blit(WP.WPSelected,(WP.WPimgRect)) # red image
                        #Get the pieceDict key of the square for the WP which has been clicked
                        squares = []
                        for sq, val in pieceDict.items():
                            if val == WP:
                                squares.append(sq)
                        #print(squares)
                        n = squares[0]
                        # modify fromList and toList for this WP, eg. WP1
                        newFromList = []
                        newToList = []
                        for i, val in enumerate(fromList):
                            if val==n:
                                newFromList.append(fromList[i])
                                newToList.append(toList[i])
                                
                        print (newFromList) 
                        print (newToList)    
                        if len(newToList)==1:
                            RD1.redDotRect.topleft = (WP.pos(boardDict, newToList[0]))
                            screen.blit(RD1.redDotImg,(RD1.redDotRect))
                        elif len(newToList)==2:
                            RD1.redDotRect.topleft = (WP.pos(boardDict, newToList[0]))
                            screen.blit(RD1.redDotImg,(RD1.redDotRect))
                            RD2.redDotRect.topleft = (WP.pos(boardDict, newToList[1]))
                            screen.blit(RD2.redDotImg,(RD2.redDotRect))
        

                        
                        
        # black pawns
        if pieceDict[key] == BP:
            screen.blit(BP.BPimg,(BP.pos(boardDict, key)))
        #print(pieceList)

#setup up from and to lists for WP
fromList =[]
toList = []

def to_from (pieceDict):
    for key in range(6):    # check squares 0 to 5
        for num in range(len(WPList)):  #3
            if pieceDict[key] == WPList[num]:   #if WPn detected
                if pieceDict[key+3] == None:    # if nothing in front of WP
                    fromList.append(key)
                    toList.append(key+3)
                if (key % 3) > 0: 
                    # False for squares 0 & 3 (LH column), True for midddle & RH column
                    # WP can't capture diagonally to left from these squares
                    if pieceDict[key+2] == BP:  # LH diagonal capture possible
                        fromList.append(key)
                        toList.append(key+2)
                if (key % 3) < 2: 
                    #False for squares 2 & 5, True for squares 0,1,3,4 LH & middle columns
                    # WP can't capture diagonally to right from these squares
                    if pieceDict[key+4] == BP:  #RH diagonal capture possible
                        fromList.append(key)
                        toList.append(key+4) 
    
#to_from(pieceDict)
#print (f"fromList {fromList}")
#print (f"toList {toList}")

while True:    
    for event in pygame.event.get():
        # any keyboard or mouse event will activate this loop
        if event.type == pygame.QUIT:
            # pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            for WP in WPList:
                if WP.WPimgRect.collidepoint(pygame.mouse.get_pos()):
                    WP.WPflag = True # flag for clicked WP (touch move!)
                    to_from(pieceDict) # generates ALL possible moves after clicking pawn
                    values = WP1
                    keys = [key for key, val in pieceDict.items() if val == values]
                    n = keys[0]
                    for i, val in enumerate(fromList):
                        if val==n:
                            print(f"toList {toList}")

                   
                    
                    print(pygame.mouse.get_pos())
                
                
            #
                #begin = pieceList.index(WP)    # board pos of this WP
                # True if mouse clicks inside WPimgRect
                #boole = True #turn on redDot
            #if RD1.redDotRect.collidepoint(pygame.mouse.get_pos()):
                #boole = False   #turn off redDot
                #end = begin + 3     # +3 for normal move
                #flag = 2    # move piece to new positions
            #if RD2.redDotRect.collidepoint(pygame.mouse.get_pos()):
                #boole = False   #turn off redDot
                #end = begin + 4 #capture to right
                #flag = 2    # move piece to new positions
        
        
            #print(pygame.mouse.get_pos())
        
    screen.fill(settings.bg_colour)  
    # draw line grid on screen (must be in while loop)
    pygame.draw.line(screen,"red",start_pos=(150,0),end_pos=(150,450))
    pygame.draw.line(screen,"red",start_pos=(300,0),end_pos=(300,450))
    pygame.draw.line(screen,"red",start_pos=(0,150),end_pos=(450,150))
    pygame.draw.line(screen,"red",start_pos=(0,300),end_pos=(450,300))
    
    pieces_show(pieceDict)
    #to_from(pieceDict)
    #print (f"fromList {fromList}")
    #print (f"toList {toList}")
    #print(pieceList)
       
    pygame.display.flip()   # updates entire display, must come afer fill(bg_colour)
    clock.tick(1)
    

    