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

def grid(bgcolour):
    screen.fill(bgcolour)  #bg colour screen
    # draw line grid on screen (must be in while loop)
    pygame.draw.line(screen,"red",start_pos=(150,0),end_pos=(150,450))
    pygame.draw.line(screen,"red",start_pos=(300,0),end_pos=(300,450))
    pygame.draw.line(screen,"red",start_pos=(0,150),end_pos=(450,150))
    pygame.draw.line(screen,"red",start_pos=(0,300),end_pos=(450,300))

class Pawn:
    """make a class since want 3 white pawn instances"""
    def __init__(self):
        self.screen = screen    # give pawns access to hexapawn screen
        self.screenRect = self.screen.get_rect() # for positioning pawns later
        self.WPimg = pygame.image.load('images/whitePawn.png') #image surface!
        self.WPimgRect = self.WPimg.get_rect() # rect for mouse event detection
        self.BPimg = pygame.image.load('images/blackPawn.png')
        self.BPimgRect = self.BPimg.get_rect() 
        self.WPSelected = pygame.image.load('images/whitePawnSelected.png')
        self.WPflag1 = False # triggers WP to from lists 
        self.WPflag2 = False # changing WP colour to red
        self.BPflag = False # triggers BP to from lists and BP move

#    pawn pos method: input boardDict, num -> return board position (x, y)
    def pos(self, boardDict, num ):
        return boardDict[num]

class RedDot:
    """ Need 2 red dots sometimes"""
    def __init__(self):
        self.screen = screen    # give red dots access to hexapawn screen
        self.redDotImg = pygame.image.load('images/redDot.png')
        self.RDtransparent = pygame.image.load('images/redDotTransparent.png')
        self.redDotRect = self.redDotImg.get_rect()
        self.redDotflag1 = False    # for red dots appearinng
        self.redDotflag2 = False    # for red dot clicking

# make 3 instances of the WP
WP1=Pawn() 
WP2=Pawn()
WP3=Pawn()
# WP list, will have to modify as game progresses
WPList =[WP1,WP2,WP3]

#create BP instance, only one needed
BP = Pawn()
BP.BPflag = False   # when BPs ready to move make True
# create red dot instances
RD1 = RedDot()
RD2 = RedDot()
RDList = [RD1, RD2] #permanent (immutable, ha)

#pieceDict shows pieces on their (initial) board positions
pieceDict ={0:WP1, 1:WP2 ,2:WP3, 3:None, 4:None, 5:None,6:BP, 7:BP, 8:BP }

# pieces_show code will show the pieces when run in the while loop!
def pieces_show(pieceDict): # dictionary changes to show game progress
    # locate WPs in pieceDict and show them as clickable objects
    for key in pieceDict:
        for num, WP in enumerate(WPList):
            if pieceDict[key] == WPList[num]:   # find the WPs
                WP.WPimgRect.topleft = WP.pos(boardDict, key) 
                #position pawn rect by boardDict values
                if WP.WPflag2 == False:
                    screen.blit(WP.WPimg,(WP.WPimgRect))  #(image surface WP, positon)
                elif WP.WPflag2 == True: # if WP clicked turn to red
                    screen.blit(WP.WPSelected,(WP.WPimgRect)) # red image
                
            if WP.WPflag1 == True:
                thisWP_to_from() # get to&from lists for this clicked WP
                #print (f"82 {thisWP_to_from()}")
                for RD in RDList:
                    RD.redDotflag1 = True   #RD1 and RD2 ready for placement and show  
                WP.WPflag1 = False   #  prevent to & from lists looping
                
        # black pawns images only           
        if pieceDict[key] == BP:
            screen.blit(BP.BPimg,(BP.pos(boardDict, key)))
            
    # put clickable red dots on screen in correct positions using to lists
    # WP click activates thisWP_to_from function
    #print(f"93 newFromList {newFromList}")
    #print(f"newToList {newToList}")
    print(f"tuple {thisWP_to_from()}")
    for num, RD in enumerate(RDList):   # loop through RD1, RD2
        if RD.redDotflag1 == True:    # triggered line 81 when WPflag True
            if len(newToList) == 1:
                RD.redDotRect.topleft = (WP.pos(boardDict, newToList[0]))
                screen.blit(RD.redDotImg,(RD.redDotRect))
            elif len(newToList)==2:
                RD.redDotRect.topleft = (WP.pos(boardDict, newToList[num]))
                screen.blit(RD.redDotImg,(RD.redDotRect))
        
    # Make WP move (rearrange pieceDict) when RD clicked then deactivate flags
    for num, RD in enumerate(RDList):   #num corresponds to RD1&2
        if RD.redDotflag2 == True: # True only for the RD which is clicked
            if len(newToList) == 1: # only one move possible
                pieceDict[newToList[0]]=pieceDict[newFromList[0]] # move correct WP
                pieceDict[newFromList[0]]=None  #rearrange Piece dictionary
            elif len(newToList) == 2:
                pieceDict[newToList[num]]=pieceDict[newFromList[num]] # move correct WP
                pieceDict[newFromList[num]]=None  #rearrange Piece dictionary
                
    # after dictionary rearranged turn off red flags            
            for RD in RDList:
                RD.redDotflag1 = False #reset flags so RDs disappear
                RD.redDotflag2 = False
            for WP in WPList:
                WP.WPflag2 = False # so WPs change back to white after moving  
            #activate BPs here, correct indentation (not sure why)
            BP.BPflag = True
            
            # Make red dots transparent
    if RD.redDotflag1 == False and RD.redDotflag2 == False:
        for RD in RDList:
            screen.blit(RD.RDtransparent,(RD.redDotRect)) 
            
    if BP.BPflag == True:
        to_from_BP()
        moveBP(pieceDict, *to_from_BP()) #unpack tuple
        BP.BPflag = False   # stop BP moving

# make newToFrom & To lists for the WP which is clicked
newFromList = []    # require initialisaton 
newToList = []
def thisWP_to_from(): 
    for WP in WPList:
        if WP.WPflag1:    # true only for the WP rect clicked
        #Get the pieceDict key of the square for the WP which has been clicked
            sqList = []
            for sq, val in pieceDict.items():
                if val == WP:
                    sqList.append(sq)
            square = sqList[0]  # sq of clicked WP
            # modify fromList and toList for this WP
            if pieceDict[square + 3] == None:   # nothing in front of this WP
                newFromList.append(square)
                newToList.append(square + 3)
                print (f"newFromList {newFromList}")
                print(f"newToList {newToList}")
            for key in range(6):    # check squares 0 to 5 for WP
                if (key % 3) > 0: 
                    # False for squares 0 & 3 (LH column), True for midddle & RH column
                    # WP can't capture diagonally to left from these squares
                    if square == key:   #get key for this WP
                        if pieceDict[key+2] == BP:  # LH diagonal capture possible
                            newFromList.append(square)
                            newToList.append(square+2)
                            print (f"newFromList {newFromList}")
                            print(f"newToList {newToList}")
                if (key % 3) < 2: 
                    if square == (key):
                    #False for squares 2 & 5, True for squares 0,1,3,4 LH & middle columns
                    # WP can't capture diagonally to right from these squares
                        if pieceDict[key+4] == BP:  #RH diagonal capture possible
                            newFromList.append(square)
                            newToList.append(square+4)
                            print (f"newFromList {newFromList}")
                            print(f"newToList {newToList}")
    return newFromList, newToList   # not necessary initially

#print (f"175 {thisWP_to_from()}") # empty lists?

def to_from_BP():
    newFromList =[]
    newToList = []
    BPList = []
    # make a list of BP squares
    for key in range(3,9): # check squares 3 to 8
        if pieceDict[key] == BP:
            BPList.append(key)  # list of squares containing a BP
            #print (BPList)
            
    for num in BPList:
        if pieceDict[num - 3] == None: # empty square in front of BP
            newFromList.append(num)
            newToList.append(num - 3)
            #print(f"fromListBP = {newFromList}")   #[6, 8]
            #print(f"toListBP = {newToList}")       #[3, 5]

    for key in range(6):
        if key % 3 < 2: # key 2 & 5 False (LH diagonal from black side banned)
            for num in BPList:
                for WP in WPList: # inner loop run for each outer loop
                    if pieceDict[key] == WP:    # find WP keys
                        if key + 4 == (num):    #RH diagonal from black side
                            newFromList.append(num)
                            newToList.append(num-4)
                            #print(f"fromListBP = {newFromList}")
                            #print(f"toListBP = {newToList}")
                            
        if key%3 > 0:   # key 0 & 3 False (RH diagonal from black side banned)
            for num in BPList:
                for WP in WPList:
                    if pieceDict[key] == WP:
                        if key + 2 == (num):
                            newFromList.append(num)
                            newToList.append(num-2)
                            #print(f"fromListBP = {newFromList}")
                            #print(f"toListBP = {newToList}")
    
    return newFromList, newToList
    # this tuple is unpacked on line 108
print(f"211 to_from_BP {to_from_BP()}")
#rearrage pieceDict, move BP
# NFL & NTL here needed for unpacking of tuple
def moveBP(pieceDict, newFromList, newToList):
    r = random.randint(0, len(newFromList)-1)
    pieceDict[newToList[r]] = pieceDict[newFromList[r]]
    pieceDict[newFromList[r]]  = None
    # remake WPList (a WP may have been captured)
    #print (f"WPList={WPList}")
    #print (pieceDict)
    return pieceDict
    
''' 
# after  BPs move check the WPList still valid
    for key in PieceDict:
        WPList = []
        if pieceDict[key] == WP1 or WP2 or WP3:
            WPList.append(pieceDict[key])
            
'''                         
while True:    
    for event in pygame.event.get():
        # any keyboard or mouse event will activate this loop
        if event.type == pygame.QUIT:
            # pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            for WP in WPList:
                if WP.WPimgRect.collidepoint(pygame.mouse.get_pos()):
                    WP.WPflag1 = True # flag for clicked WP to from lists
                    WP.WPflag2 = True # flag for clicked WP colour red
                    
            
            # for flag 2 activate RD1 or 2 when clicked
            if RD1.redDotRect.collidepoint(pygame.mouse.get_pos()):
                RD1.redDotflag2 = True # activate RD1&2 pawn moves
            if RD2.redDotRect.collidepoint(pygame.mouse.get_pos()):
                RD2.redDotflag2 = True # activate RD1&2 pawn moves

    grid(settings.bg_colour)
    pieces_show(pieceDict) # show pieces
       
    pygame.display.flip()   # updates entire display
    clock.tick(1)   # speed up clock later
    

    