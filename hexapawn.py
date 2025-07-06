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

fromList = []    # require initialisaton 
toList = []

#pieceList shows pieces on their (initial) board positions
pieceList =[None, WP2 ,WP3, None, WP1, None, BP, BP, BP ]

# main is in the while loop!
def main(pieceList): # dictionary changes to show game progress
    piecesShow(pieceList)  
    WP_toFrom() # get to&from lists for this clicked WP
    
    #redDots()
    #rearrange_pieceList(pieceList)
    #piecesShow(pieceList)  # run the view again
    #turnFlagsOff()  # flags go off before next click!
    #activate BPs here, correct indentation is a mystery!!!
    #BP.BPflag = True
    # get BP to and from possibilities   
'''         
    if BP.BPflag == True:
        to_from_BP()
        # move BP and rearrange dictionary
        moveBP(pieceList, *to_from_BP()) #unpack tuple
        BP.BPflag = False   # stop BP moving
    
    # update WP list here since a WP may be gone
    
    # view pieceList
    #print (f"86 fromList {fromList}")
    #print (f"toList {toList}")
    #print(f"88 {pieceList}") # dictionary updated
'''
def piecesShow(pieceList):
    for key, item in enumerate(pieceList):
        for num, WP in enumerate(WPList):
            if pieceList[key] == WPList[num]:   # find the WPs
                WP.WPimgRect.topleft = WP.pos(boardDict, key) 
                #position pawn rect by boardDict values
                if WP.WPflag2 == False:
                    screen.blit(WP.WPimg,(WP.WPimgRect))  # white pawn
                if WP.WPflag2 == True: # if WP clicked turn to red
                    screen.blit(WP.WPSelected,(WP.WPimgRect)) # red image
                        
        # black pawns images only           
        if pieceList[key] == BP:
            screen.blit(BP.BPimg,(BP.pos(boardDict, key)))

def WP_toFrom():
    for WP in WPList:
        if WP.WPflag1:    # true only for the WP rect clicked 
        #Get the pieceList index of the square for the WP which has been clicked
            square = pieceList.index(WP)
            # get fromList and toList for this WP
            if pieceList[square + 3] == None:   # nothing in front of this WP
                fromList.append(square)
                toList.append(square + 3)
                print (f"fromList {fromList}")
                print(f"toList {toList}")
                
            for key in range(6):    # check squares 0 to 5 for WP
                if (key % 3) > 0: 
                    # False for squares 0 & 3 (LH column), True for midddle & RH column
                    # WP can't capture diagonally to left from these squares
                    if square == key:   #get key for this WP
                        if pieceList[key+2] == BP:  # LH diagonal capture possible
                            fromList.append(square)
                            toList.append(square+2)
                            print (f"135 fromList {fromList}")
                            print(f"136 toList {toList}")
                            
                if (key % 3) < 2: 
                    if square == (key):
                    #False for squares 2 & 5, True for squares 0,1,3,4 LH & middle columns
                    # WP can't capture diagonally to right from these squares
                        if pieceList[key+4] == BP:  #RH diagonal capture possible
                            fromList.append(square)
                            toList.append(square+4)
                            print (f"145 fromList {fromList}")
                            print(f"146 toList {toList}")
        WP.WPflag1 = False   #  prevent to & from lists looping
    for RD in RDList:
        RD.redDotflag1 = True   
        # triggers code that shows Rdots for changing to from lists
'''
   
    print (f" 185 fromListWP {fromList}")
    print(f"186 toListWP {toList}")                           
    return fromList, toList   # not necessary initially


'''   
def redDots():        
    # put clickable red dots on screen in correct positions using to lists
    #print(f"93 fromList {fromList}")
    #print(f"toList {toList}")
    # print(f"tuple {WP_toFrom()}")
    for num, RD in enumerate(RDList):   # loop through RD1, RD2
        if RD.redDotflag1 == True and RD.redDotflag2 == False: 
            # flag1: RDs appear for current to from lists, flag2 False until RD clicked
            if len(toList) == 1:
                RD.redDotRect.topleft = (WP.pos(boardDict, toList[0]))
                screen.blit(RD.redDotImg,(RD.redDotRect))
            elif len(toList)==2:
                RD.redDotRect.topleft = (WP.pos(boardDict, toList[num]))
                screen.blit(RD.redDotImg,(RD.redDotRect))
        if RD.redDotflag1 == False and RD.redDotflag2 == False: 
            # both flags set to false after RD clicked
            for RD in RDList:
                screen.blit(RD.RDtransparent,(RD.redDotRect)) 
            

def rearrange_pieceList(pieceList):       
    # Make WP move (rearrange pieceList) when RD clicked then deactivate flags
    for num, RD in enumerate(RDList):   #num corresponds to RD1&2
        if RD.redDotflag2 == True: # True only for the RD which is clicked
            if len(toList) == 1: # only one move possible
                pieceList[toList[0]]=WP # move correct WP
                pieceList[fromList[0]]=None  #rearrange Piece dictionary
            elif len(toList) == 2:
                pieceList[toList[num]]=WP # move correct WP
                pieceList[fromList[num]]=None  #rearrange Piece dictionary
    
  
# make newToFrom & To lists for the WP which is clicked


def turnFlagsOff():
        # after dictionary rearranged & WP moves turn off red flags            
    for RD in RDList:
        RD.redDotflag1 = False #reset flags so RDs disappear
        RD.redDotflag2 = False  # click control?
    for WP in WPList:
        WP.WPflag2 = False

def to_from_BP():
    fromList =[]
    toList = []
    BPList = []
    # make a list of BP squares
    for key in range(3,9): # check squares 3 to 8
        if pieceList[key] == BP:
            BPList.append(key)  # list of squares containing a BP
            #print (BPList)
            
    for num in BPList:
        if pieceList[num - 3] == None: # empty square in front of BP
            fromList.append(num)
            toList.append(num - 3)
            #print(f"fromListBP = {fromList}")   #[6, 8]
            #print(f"toListBP = {toList}")       #[3, 5]

    for key in range(6):
        if key % 3 < 2: # key 2 & 5 False (LH diagonal from black side banned)
            for num in BPList:
                for WP in WPList: # inner loop run for each outer loop
                    if pieceList[key] == WP:    # find WP keys
                        if key + 4 == (num):    #RH diagonal from black side
                            fromList.append(num)
                            toList.append(num-4)
                            #print(f" 210 fromListBP = {fromList}")
                            #print(f"toListBP = {toList}")
                            
        if key%3 > 0:   # key 0 & 3 False (RH diagonal from black side banned)
            for num in BPList:
                for WP in WPList:
                    if pieceList[key] == WP:
                        if key + 2 == (num):
                            fromList.append(num)
                            toList.append(num-2)
                            
    print(f" 227 fromListBP = {fromList}")
    print(f"228 toListBP = {toList}")
    return fromList, toList
    # this tuple is unpacked on line 108
print(f"225 tuple to_from_BP {to_from_BP()}")
#rearrage pieceList, move BP
# NFL & NTL here needed for unpacking of tuple
def moveBP(pieceList, fromList, toList):
    r = random.randint(0, len(fromList)-1)
    pieceList[toList[r]] = BP
    pieceList[fromList[r]]  = None
    # remake WPList (a WP may have been captured)
    #print (f"WPList={WPList}")
    #print (pieceList)
    return pieceList

#def WP_ID (ID):
#    if ID ==
    
    

# after  BPs move check the WPList still valid
    for key in pieceList:
        WPList = []
        if pieceList[key] == WP1 or WP2 or WP3:
            WPList.append(pieceList[key])
            
                      
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
            for RD in RDList:
                if RD.redDotRect.collidepoint(pygame.mouse.get_pos()):
                    RD.redDotflag2 = True # rearrange pieceList

    grid(settings.bg_colour)
    main(pieceList) # show pieces
       
    pygame.display.flip()   # updates entire display
    clock.tick(1)   # speed up clock later
    

    