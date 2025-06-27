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

def grid(colour):
    screen.fill(settings.bg_colour)  
    # draw line grid on screen (must be in while loop)
    pygame.draw.line(screen,"red",start_pos=(150,0),end_pos=(150,450))
    pygame.draw.line(screen,"red",start_pos=(300,0),end_pos=(300,450))
    pygame.draw.line(screen,"red",start_pos=(0,150),end_pos=(450,150))
    pygame.draw.line(screen,"red",start_pos=(0,300),end_pos=(450,300))

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
        self.RDtransparent = pygame.image.load('images/redDotTransparent.png')
        self.redDotRect = self.redDotImg.get_rect()
        self.redDotflag1 = False    # for red dots appearinng
        self.redDotflag2 = False    # for red dot clicking

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
RDList = [RD1, RD2]

#pieceDict shows pieces on their board positions
pieceDict ={0:WP1, 1:None ,2:WP3, 3:None, 4:WP2, 5:None,6:BP, 7:BP, 8:BP }
#print(f"WP 63 = {WP}")
# pieces_show code will show the pieces when run in the while loop!
def pieces_show(pieceDict):
    flag3 = False
    #print(f"WP 66 = {WP}") local variable WP
    for key in pieceDict:
        for num, WP in enumerate(WPList):
            if pieceDict[key] == WPList[num]:
                WP.WPimgRect.topleft = WP.pos(boardDict, key) 
                #position pawn rect by boardDict values
                if WP.WPflag == False:
                    screen.blit(WP.WPimg,(WP.WPimgRect))  #(image surface WP, positon)
                elif WP.WPflag == True: # WP clicked
                    screen.blit(WP.WPSelected,(WP.WPimgRect)) # red image
    
    # put red dots on screen in correct positions
    if RD1.redDotflag1 == True:    # triggered at bottom of thisWP_to_from
        if len(newToList) == 1:
            RD1.redDotRect.topleft = (WP.pos(boardDict, newToList[0]))
            screen.blit(RD1.redDotImg,(RD1.redDotRect))
        
    # Make WP move when RDs clicked
    if RD1.redDotflag2 == True: # True for both RD1 & 2 when red dot clicked
        if len(newToList) == 1:
            pieceDict[newFromList[0]]=None
            pieceDict[newToList[0]]=WP # which WP issue again
            #print(pieceDict)    # changes, confirmed
            RD1.redDotflag1 = False #reset flags so RDs disappear
            RD1.redDotflag2 = False
            flag3 = True
            WP.WPflag = False # so WPs change back to white after moving
    
    # Make red dots transparent
    if RD1.redDotflag2 == False and RD1.redDotflag1 == False and flag3 == True: 
        RD1.redDotRect.topleft = (WP.pos(boardDict, newToList[0]))
        screen.blit(RD1.RDtransparent,(RD1.redDotRect)) 
    
    for key in pieceDict:   # repeating the loop for WPs, necessary?          
        # black pawns images only
        if pieceDict[key] == BP:
            screen.blit(BP.BPimg,(BP.pos(boardDict, key)))

#setup up from and to lists for WP
fromList =[]
toList = []

def to_from ():
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
          
# make newToFrom & To lists for the WP which is clicked
newFromList = []
newToList = []
def thisWP_to_from(): 
    for WP in WPList:
        if WP.WPflag:    # true when a WP rect clicked
        #Get the pieceDict key of the square for the WP which has been clicked
            sqList = []
            for sq, val in pieceDict.items():
                if val == WP:
                    sqList.append(sq)
            #print(f"square = {sqList}")
            square = sqList[0]
            #print(pieceDict) #0:WP
            # modify fromList and toList for this WP
            for i, val in enumerate(fromList):
                if val==square: #changes when WP moves
                    newFromList.append(fromList[i])
                    newToList.append(toList[i])
            print(f"fromList {fromList}")
            print(f"toList {toList}")
            print (f"newFromList {newFromList}")
            print(f"newToList {newToList}")
        # red dots can appear after newTo and from Lists adjusted
        for RD in RDList:
            RD.redDotflag1 = True   #RD1 and RD2 ready for placement and show
    
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
                    to_from() # generates ALL possible moves after clicking pawn
                    thisWP_to_from() #to&from just for this clicked WP
            
            #for RD in RDList:        
            if RD1.redDotRect.collidepoint(pygame.mouse.get_pos()):
                RD1.redDotflag2 = True # activate pawn moves
                    #print(f"RD.redDotflag2 {RD.redDotflag2}")

    grid(settings.bg_colour)
    pieces_show(pieceDict)
       
    pygame.display.flip()   # updates entire display, must come afer fill(bg_colour)
    clock.tick(1)
    

    