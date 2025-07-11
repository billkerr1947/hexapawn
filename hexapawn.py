import pygame
import sys  # to exit
import settings
from settings import boardDict
import random
import time

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
        self.BPflag = True
        self.special = True

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
        self.concealFlag = False    # for red dots appearinng
        self.redDotflag2 = False    # for red dot clicking

# make 3 instances of the WP
WP1=Pawn() 
WP2=Pawn()
WP3=Pawn()
# might need a generic WP(?)
WPx= Pawn()
WPx.special = False

# WP list, will have to modify as game progresses
WPList =[WP1,WP2,WP3]

#create BP instance, only one needed
BP = Pawn()
BP.BPflag = True

# create red dot instances
RD1 = RedDot()
RD2 = RedDot()
RDList = [RD1, RD2] #permanent (immutable, ha)

#pieceList shows pieces on their (initial) board positions
pieceList =[WP1, None ,WP2, None, WP3, None, BP, BP, BP ]

moveNum = 1
mainCounter = 0

# main is in the while loop!
def main(moveNum): 
    global mainCounter
    if moveNum == 1 or moveNum == 3:
        WPmove()
        mainCounter += 1
        # wait until finished before incrementing moveNum
    if mainCounter > 10:
        moveNum += 1
        mainCounter = 0
    if moveNum == 2 or moveNum == 4:
        BPmove()
    #global moveNum  # WP moves odd 1 & 3, BP moves even 2 & 4
    #global mainCounter
    
def WPmove():       
    print(f"93 moveNum {moveNum}")
    piecesShow() 
    WP_toFrom() # get to&from lists for clicked WP
    redDots(*WP_toFrom())   # unpack toFrom tuple
    rearrange_pieceList(pieceList, *WP_toFrom())    # unpack again
    turnWPflag2Off()
    BP.BPflag = True
def BPmove():
    #BP.BPflag = True    # temporary
    if BP.BPflag == True:
        piecesShow()
        print ("104 black move")
        print(f"105 preBlackList moveNum {moveNum}")
        to_from_BP()
        # move BP and rearrange dictionary
        moveBP(pieceList, *to_from_BP()) #unpack tuple
        #if len(WPList) < 3:
            #WPListUpdate(WPList) # update WPList
            #print ("117 WPList {WPList}")
        BP.BPflag = False   # stop BP moving
    
def piecesShow(): # show WPs and BPs
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
    
    for RD in RDList:
        if RD.concealFlag == True:        
            screen.blit(RD.RDtransparent,(RD.redDotRect))  

def WP_toFrom():
    fromList = []   # otherwise new values are added to old!
    toList = []
    for WP in WPList:
        print (WPList)
        print (f"137 WP = {WP}") # it thinks I click WP1, whichever WP I click!!!
        if WP.WPflag1:    # should be true only for the WP rect clicked 
            print('138 WP1 only????????? YES')
        #Get the pieceList index of the square for the WP which has been clicked
            square = pieceList.index(WP)
            # get fromList and toList for this WP
            if pieceList[square + 3] == None:   # nothing in front of this WP
                fromList.append(square)
                toList.append(square + 3)
                print (f"152 fromList {fromList}")
                print(f"153 toList {toList}")
                
            for key in range(6):    # check squares 0 to 5 for WP
                if (key % 3) > 0: 
                    # False for squares 0 & 3 (LH column), True for midddle & RH column
                    # WP can't capture diagonally to left from these squares
                    if square == key:   #get key for this WP
                        if pieceList[key+2] == BP:  # LH diagonal capture possible
                            fromList.append(square)
                            toList.append(square+2)
                            #print (f"158 WPfromList {fromList}")
                            #print(f"159 WPtoList {toList}")
                            
                if (key % 3) < 2: 
                    if square == (key):
                    #False for squares 2 & 5, True for squares 0,1,3,4 LH & middle columns
                    # WP can't capture diagonally to right from these squares
                        if pieceList[key+4] == BP:  #RH diagonal capture possible
                            fromList.append(square)
                            toList.append(square+4)
        print (f"166 fromList {fromList}")
        print(f"167 toList {toList}")
        return fromList, toList

def redDots(fromList, toList):        
    # show clickable red dots on screen in correct positions using to lists
    print(f"172 RD  fromList {fromList}")
    print(f"173 toList RD {toList}")
    print(f"174 tuple {WP_toFrom()}")
    if len(toList) == 1:
        RD1.redDotRect.topleft = (WP.pos(boardDict, toList[0]))
        screen.blit(RD1.redDotImg,(RD1.redDotRect))
    elif len(toList)==2:
        for num, RD in enumerate(RDList):   # loop through RD1, RD2
            RD.redDotRect.topleft = (WP.pos(boardDict, toList[num]))
            screen.blit(RD.redDotImg,(RD.redDotRect))
            
def rearrange_pieceList(pieceList, fromList, toList):       
    # Make WP move (rearrange pieceList) when RD clicked then deactivate flags
    if len(toList) == 1: # only one move possible
        if RD1.redDotflag2 == True: # True when RD1 clicked
            getPawn = pieceList[fromList[0]]
            getNone = pieceList[toList[0]]
            pieceList[toList[0]]=getPawn # move correct WP?
            pieceList[fromList[0]]=getNone  #rearrange pieceList
            RD1.redDotflag2 = False
            RD1.concealFlag = True
            
            
    elif len(toList) == 2:
        for num, RD in enumerate(RDList):   #num corresponds to RD1&2
            if RD.redDotflag2 == True:
                getPawn = pieceList[fromList[num]]
                #getNone = pieceList[toList[num]]
                pieceList[toList[num]]=getPawn # move correct WP?
                pieceList[fromList[num]]=None  #rearrange pieceList
                
                #print(f"201 {RD.concealFlag}")
                RD.redDotflag2 = False
            
            RD.concealFlag = True
            # conceal both RDots    
    print(f"216 after W move {pieceList}")
  
def turnWPflag2Off():
    for WP in WPList:
        WP.WPflag2 = False

# make BP to & from lists    
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
            #print(f"fromListBP = {fromList}")   
            #print(f"toListBP = {toList}")       

    for key in range(6):
        if key % 3 < 2: # key 2 & 5 False (LH diagonal from black side banned)
            for num in BPList:
                for WP in WPList: # inner loop run for each outer loop
                    if pieceList[key] == WP:    # find WP keys
                        if key + 4 == (num):    #RH diagonal from black side
                            fromList.append(num)
                            toList.append(num-4)
                            
                            
        if key%3 > 0:   # key 0 & 3 False (RH diagonal from black side banned)
            for num in BPList:
                for WP in WPList:
                    if pieceList[key] == WP:
                        if key + 2 == (num):
                            fromList.append(num)
                            toList.append(num-2)
                            
    print(f" 260 fromListBP = {fromList}")
    print(f"261 toListBP = {toList}")
    return fromList, toList
    # this tuple is unpacked on line 108 still!
print(f"254 tuple to_from_BP {to_from_BP()}")

#rearrage pieceList, move random BP
# FL & TL here needed for unpacking of tuple
def moveBP(pieceList, fromList, toList):
    r = random.randint(0, len(fromList)-1)
    pieceList[toList[r]] = BP   # rearrange pieceList
    pieceList[fromList[r]]  = None
    # remake WPList (a WP may have been captured)
    #print (f" 262 WPList={WPList}")
    #print (f"263 {pieceList}")
    return pieceList

# after  BPs move check the WPList still valid
def WPListUpdate(WPList):
    newWPList = []
    if len(WPList) == 0:
        return WPList
    else:
        for WP in WPList:
            if WP in pieceList:
                newWPList.append(WP)
        WPList = newWPList
        return (WPList)


            
mainWhileCounter = 0                      
while True:
    mainWhileCounter = mainWhileCounter + 1 
    #print (f"287 moveNum {moveNum}")
    #print ( f"288 mainWhileCounter = {mainWhileCounter}")  
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
                    
            # for flag 2 activate RD1 or  +=2 when clicked
            for RD in RDList:
                if RD1.redDotRect.collidepoint(pygame.mouse.get_pos()):
                    RD1.redDotflag2 = True # rearrange pieceList
                if RD2.redDotRect.collidepoint(pygame.mouse.get_pos()):
                    RD2.redDotflag2 = True # rearrange pieceList
                

    grid(settings.bg_colour)
    main(moveNum) # show pieces and more
       
    pygame.display.flip()   # updates entire display
    clock.tick(1)   # speed up clock later
    
    

    