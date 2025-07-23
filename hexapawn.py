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
    pygame.draw.line(screen,"red",start_pos=(450,0),end_pos=(450,450))
    pygame.draw.line(screen,"red",start_pos=(600,0),end_pos=(600,450))
    
    pygame.draw.line(screen,"red",start_pos=(0,150),end_pos=(750,150))
    pygame.draw.line(screen,"red",start_pos=(0,300),end_pos=(750,300))

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
    
    def pos(self, boardDict, num ): # reposition red dots sometimes
        return boardDict[num]
    
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
pieceList =[WP1,WP2,WP3, None, None, None, BP, BP, BP, None ]

moveNum = 1
mainCounter = 0
clickWP = False
mytuple =([7],[8])  # arbitrary starting values
W_wins = 0
B_wins = 0

# main is in the while loop!
def main(): 
    piecesShow(pieceList)
    global mainCounter
    global moveNum
    if moveNum == 1 or moveNum == 3 or moveNum == 5 or moveNum == 7 or moveNum == 9:
        WPmove()
        mainCounter += 1
        # make some time for pawn click before incrementing moveNum
        if mainCounter > 4:
            for WP in WPList:
                WP.WPflag2 = False
        if mainCounter > 7:
            moveNum += 1
            print(f"99 main moveNum {moveNum}")
            mainCounter = 0
            
            if moveNum == 2 or moveNum == 4 or moveNum == 6 or moveNum == 8:
                BPmove()
    #global moveNum  # WP moves odd 1 & 3, BP moves even 2 & 4
    
def WPmove():       
    print(f"107 WPmove moveNum {moveNum}")
    piecesShow(pieceList) 
    global clickWP
    global mytuple
    global blockChecker
    global W_wins
    global B_wins
    
    blockChecker = True
    if blockChecker == True:
        #print(f"116 pieceList {pieceList}")
        if blockCheck() == []:
            print(f"116 blockCheck() {blockCheck()}")
            print ("116 white blocked. black wins")
            B_wins += 1
            print(f"125 B_wins {B_wins}")
            blockChecker = False
            sys.exit(0)
            # how to stop here?
    if clickWP == True:
        # if RD on same square as WP then deactivate RDflag2 for now
        for RD in RDList:
            if RD.redDotflag2 == True:
                RD.redDotflag2 = False
        print (f"124 inside click {clickWP}")
        #WP_toFrom() # get to&from lists for clicked WP
        #print(f"120 before call old tuple {mytuple}")
        mytuple = WP_toFrom()
        #print(f"128 new tuple {mytuple}")
        
        clickWP = False
        # turn WPflag1 off immediately!
        for WP in WPList:
            WP.WPflag1 = False
        #print(f"127 outside click  tuple {mytuple}")
    # only run redDots & rearrange_PL for real fromList values
    # 
    # but ([][]) needed for when game is blocked
    print(f"138 mytuple white {mytuple}")
    list =[[0],[1],[2],[3],[4],[5],[6],[0,0], [1,1],[2,2],[4,4],[5,5],[3,3]]
    if mytuple[0] in list:  # if legitimate move fromList
        redDots(*mytuple) # red dots appear
        #print(f"143 after RDot move {moveNum}") 
        
        rearrange_pieceList(pieceList, *mytuple ) 
        piecesShow(pieceList)
    
    
    BP.BPflag = True

def BPmove():
    #BP.BPflag = True    # temporary
    if BP.BPflag == True:
        piecesShow(pieceList)
        print ("148 black move")
        global moveNum
        print(f"150 preBlackList moveNum {moveNum}")
        to_from_BP()
        # move BP and rearrange pieceList
        moveBP(pieceList, *to_from_BP()) #unpack tuple
        #if len(WPList) < 3: # necessary?
            #WPListUpdate(WPList) # update WPList
            #print ("117 WPList {WPList}")
        piecesShow(pieceList)
        BP.BPflag = False   # stop BP moving
        moveNum += 1
    
def piecesShow(pieceList): # show WPs and BPs
    for RD in RDList:   # conceal red dots
        if RD.concealFlag == True:        
            screen.blit(RD.RDtransparent,(RD.redDotRect))  

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
    #print("180 visiting WPTF")
    for WP in WPList:
        if WP.WPflag1 == True:    #true only for the WP rect clicked 
            fromList = []   # otherwise new values are added to old!
            toList = []
        #Get the pieceList index of the square for the WP which has been clicked
            square = pieceList.index(WP)
            if square < 9:
                # get fromList and toList for this WP
                if pieceList[square + 3] == None:   # nothing in front of this WP
                    fromList.append(square)
                    toList.append(square + 3)
                    
                for key in range(6):    # check squares 0 to 5 for WP
                    if (key % 3) > 0: 
                        # False for squares 0 & 3 (LH column), True for midddle & RH column
                        # WP can't capture diagonally to left from these squares
                        if square == key:   #get key for this WP
                            if pieceList[key+2] == BP:  # LH diagonal capture possible
                                fromList.append(square)
                                toList.append(square+2)
                                
                    if (key % 3) < 2: 
                        if square == (key):
                        #False for squares 2 & 5, True for squares 0,1,3,4 LH & middle columns
                        # WP can't capture diagonally to right from these squares
                            if pieceList[key+4] == BP:  #RH diagonal capture possible
                                fromList.append(square)
                                toList.append(square+4)
            
            print (f"209 fromList exit {fromList}")
            print(f"210 toList exit {toList}")
            return fromList, toList

def blockCheck():
    if blockChecker == True:
        fromBlockList = []   # otherwise new values are added to old!
                #toBlockList = []
        #sqList = [] 
        for squares, WP in enumerate(pieceList):
            for num, WP in enumerate(WPList):
                #Get the  squares for each WP
                
                if pieceList[squares] == WPList[num]:
                    if squares < 9:
                        if pieceList[squares + 3] == None:   # move forward possible
                            fromBlockList.append(squares)
                        for key in range(6):
                            if key % 3 < 2: #False for keys 2 and 5
                                            # True for keys 0, 1, 3 and 4
                                if squares == key:
                                    if pieceList[squares + 4] == BP:  # capture possible
                                        fromBlockList.append(squares)
                            if (key % 3) > 0:  
                                if squares == key:  
                                    if pieceList[squares + 2] == BP:  # capture possible
                                        fromBlockList.append(squares)
                                    # if fromBlocklist =[] then white can't move
        print(f"255 fromBlockList {fromBlockList}")                              
        return fromBlockList

def redDots(fromList, toList):      
    # show clickable red dots on screen in correct positions using to lists
    #print(f"215 RDots start  fromList {fromList}")
    #print(f"216 toList RDots start {toList}")
    #print(f"217 RDots tuple start {WP_toFrom()}")
    
    if len(toList) == 1:
        RD1.redDotRect.topleft = (RD1.pos(boardDict, toList[0]))
        screen.blit(RD1.redDotImg,(RD1.redDotRect))
    elif len(toList)==2:
        for num, RD in enumerate(RDList):   # loop through RD1, RD2
            RD.redDotRect.topleft = (RD.pos(boardDict, toList[num]))
            screen.blit(RD.redDotImg,(RD.redDotRect))
    #print ("258 red dots completed")
    #return pieceList
                
def rearrange_pieceList(pieceList, fromList, toList):     
    global W_wins  
    # Make WP move (rearrange pieceList) when RD clicked then deactivate flags
    print(f"262 rearrange tuple {WP_toFrom()}")
    if len(toList) == 1: # only one move possible
        if RD1.redDotflag2 == True: # True when RD1 clicked
            start = fromList[0]
            end = toList[0]
            getPawn = pieceList[fromList[0]]
            #getNone = pieceList[toList[0]]
            pieceList[toList[0]]=getPawn # move correct WP
            pieceList[fromList[0]]=None  # WP has left this square
            print(f"272 WP one option start {start}, end {end}")
            if end == 6 or end == 7  or end == 8:
                print("white wins reaches third row")
                W_wins += 1
                print(f"288 W_wins  {W_wins}")
                sys.exit(0)
            RD1.redDotflag2 = False # disable click
            RD1.concealFlag = True  # conceal red dots
            
    elif len(toList) == 2:
        for num, RD in enumerate(RDList):
            if RD.redDotflag2 == True:
                start = fromList[num]
                end = toList[num]
                fromListNum = fromList[num] 
                toListNum = toList[num]
                getPawn = pieceList[fromListNum]
                #getNone = pieceList[toListNumS]
                pieceList[toList[num]]=getPawn # move correct WP
                pieceList[fromList[num]]=None  #rearrange pieceList
                #print(f"201 {RD.concealFlag}")
                print(f"287 WP two options start {start}, end {end}")
                if end == 6 or end == 7  or end == 8:
                    print("white wins reaches third row")
                    W_wins += 1
                    print(f"310 W_wins  {W_wins}")
                    sys.exit(0)
                RD.redDotflag2 = False
                
                for RD in RDList:
                    RD.concealFlag = True
            # conceal both RDots 
    print ("266 rearrange completed")  
    return pieceList

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
                            
    print(f" 291 fromListBP = {fromList}")
    print(f"292 toListBP = {toList}")
    return fromList, toList
    # this tuple is unpacked on line 157 (at the moment!)

#rearrage pieceList, move random BP
# FL & TL here needed for unpacking of tuple
def moveBP(pieceList, fromList, toList):
    if len(fromList) == 0:
        print("340 black blocked, white wins") # working
        W_wins +=1
        print (f"351 W_wins {W_wins}")
        sys.exit(0)
        # how to stop here?
    r = random.randint(0, len(fromList)-1)
    BP_fromSq = fromList[r]
    BP_toMoveSq = toList[r]
    difference = fromList[r] - toList[r]
    print(f"346 black move from = {BP_fromSq}, to = {BP_toMoveSq}") 
    
    if difference == 2 or difference == 4:
        # find WP that will be captured and move or delete it
        getWP=pieceList[BP_toMoveSq]    # pick up captured pawn
        pieceList[9]=getWP  #move captured pawn off the board
       
    pieceList[BP_toMoveSq] = BP   # rearrange pieceList
    pieceList[BP_fromSq]  = None
    
    if BP_toMoveSq == 0 or BP_toMoveSq == 1 or BP_toMoveSq == 2:
        print ("black reaches row 1 wins")
        B_wins += 1
        print(B_wins)
        sys.exit(0)
    
    
    return (pieceList)

# after  BPs move check the WPList still valid
# may not be necessary
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
    #print ( f"279 mainWhileCounter = {mainWhileCounter}")  
    for event in pygame.event.get():
        # any keyboard or mouse event will activate this loop
        if event.type == pygame.QUIT:
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            for WP in WPList:
                if WP.WPimgRect.collidepoint(pygame.mouse.get_pos()):
                    WP.WPflag1 = True # flag for clicked WP to from lists
                    WP.WPflag2 = True # flag for clicked WP colour red
                    clickWP = True
                    print (f"355 clickWP {clickWP}")
                    
            # for flag 2 activate RD1 or  +=2 when clicked
            for RD in RDList:
                if RD1.redDotRect.collidepoint(pygame.mouse.get_pos()):
                    RD1.redDotflag2 = True # rearrange pieceList
                if RD2.redDotRect.collidepoint(pygame.mouse.get_pos()):
                    RD2.redDotflag2 = True # rearrange pieceList
                #print(f"362 RD1 clicked here {RD1.redDotflag2}" )
                #print(f"363 RD2 clicked here {RD2.redDotflag2}" )

    grid(settings.bg_colour)
    main() # show pieces and more
       
    pygame.display.flip()   # updates entire display
    clock.tick(1)   # speed up clock later
    
    

    