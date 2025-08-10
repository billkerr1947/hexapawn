import pygame
import sys  # to exit
import settings
from settings import boardDict
import random
import time

pygame.init()   # initialise pygame modules
#create screen surface
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))   
pygame.display.set_caption('Hexapawn')
pygame.font.init()  # for displaying scores
clock = pygame.time.Clock() # create a clock

def grid(bgcolour):
    screen.fill(bgcolour)  #bg colour screen
    # draw line grid on screen (must be in while loop)
    pygame.draw.line(screen,"black",start_pos=(150,0),end_pos=(150,450), width = 5)
    pygame.draw.line(screen,"black",start_pos=(300,0),end_pos=(300,450))
    pygame.draw.line(screen,"black",start_pos=(450,0),end_pos=(450,450))
    pygame.draw.line(screen,"black",start_pos=(600,0),end_pos=(600,450), width = 5)
    pygame.draw.line(screen,"black",start_pos=(0,150),end_pos=(750,150))
    pygame.draw.line(screen,"black",start_pos=(0,300),end_pos=(750,300))

class Pawn:
    """make a class since want 3 white pawn instances"""
    def __init__(self): # no parameters? poor OOPs?
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

#    pawn pos method: input boardDict, num -> return board position (x, y)
    def pos(self, boardDict, num ):
        return boardDict[num]
# could have had a showPawn method here? including blit?
    
class RedDot:
    """ Need 2 red dots sometimes"""
    def __init__(self):
        self.screen = screen    # give red dots access to hexapawn screen
        self.redDotImg = pygame.image.load('images/redDot.png')
        self.RDConceal = pygame.image.load('images/redDotConceal.png')
        self.redDotRect = self.redDotImg.get_rect()
        self.concealFlag = False    # for concealing red dots
        self.redDotflag2 = False    # for red dot clicking
    
    def pos(self, boardDict, num ): # to reposition red dots
        return boardDict[num]

class Score:
    ''' need white and black scores '''
    def __init__(self, colour, wins, pos):
        self.screen = screen # give scores access to hexapawn screen
        self.wins = wins    # parameters always require attributes (yes?)
        self.colour = colour
        self.pos = pos
        
    def show_score(self):
        self.font = pygame.font.Font(None, 36) # builtin default font, freesansbold
        # render (text, antialias, color)
        self.score_text = self.font.render(f"{self.colour} = {self.wins}",True, (0,0,0))
        self.screen.blit(self.score_text, self.pos) # blit (source, destination)
        
BScore = Score('Black', 0, (630, 20))   # win = 0 initially, then BScore.wins
WScore  = Score('White', 0, (630, 320) )
    
# make 3 instances of the WP
WP1=Pawn() 
WP2=Pawn()
WP3=Pawn()

# WP list
WPList =[WP1,WP2,WP3]

#create BP instance, only one needed
BP = Pawn()
BP.BPflag = True

# create red dot instances
RD1 = RedDot()
RD2 = RedDot()
RDList = [RD1, RD2] #permanent (immutable, ha)

#pieceList shows pieces on their (initial) board positions
# items 9, 10, 11 for offboard WPs when captured
pieceList =[WP1,WP2,WP3, None, None, None, BP, BP, BP, None, None, None ]

moveNum = 1
mainCounter = 0
clickWP = False
mytuple =([7],[8])  # arbitrary starting values
gameOver = False
gameNum = 0
whiteMove = True
newGame = False

# main is in the while loop!
def main(): 
    global pieceList
    piecesShow(pieceList)
    global mainCounter
    global whiteMove
    global newGame
    global moveNum
    global gameOver
    #print (f"110 mainCounter gameOver check {mainCounter}")
    #print(f"111 gameOver {gameOver}")
    if gameOver == False:
        whiteMove = True    # if not in main() then can't move WP
    print(f"117 gameOver {gameOver}")
    print(f"118 whiteMove {whiteMove}")
    if gameOver == True:
        #sys.exit(0)
        whiteMove = False # stop scores cycling
        try:
            newGame = input ("Do you want a new game?: Y / N") # want a popup here!
        except EOFError:
            newGame ="Y"
        print("\nYES")
        # start a new game
        pieceList_new = [WP1,WP2,WP3, None, None, None, BP, BP, BP, None, None, None ]
        pieceList = pieceList_new[:]
        # hide red dots
        for RD in RDList:
            RD.concealFlag = True
        # pause before new game
        mainCounter = 0
        mainCounter += 1
        print(f"132 mainCounter newGame {mainCounter}")
        if mainCounter > 6:
            whiteMove = True
        gameOver = False
        global moveNum
        moveNum = 1
    while whiteMove:
        piecesShow(pieceList)
        #global moveNum
        if moveNum % 2 == 1: # odd number 1, 3 etc
            WPmove()
            
        whiteMove = False   # without this screen goes black. Why?
        # moveNum incremented in pieces_rearrange
        # otherwise black move happens before white move completed
        if moveNum % 2 == 0:    # even number 2, 4 etc
            # delay black move by a few cycles
            print(f"104 BPmove {moveNum}")
            mainCounter += 1
            if mainCounter > 3:
                BPmove()
                if gameOver:   # necessary
                    return  # avoid another white move when black blocked
                    #sys.exit(0)
                whiteMove = True
                mainCounter = 0
            
    
def WPmove():       
    print(f"145 WPmove moveNum {moveNum}")
    piecesShow(pieceList) 
    global clickWP
    global mytuple
    global blockChecker
    global gameOver
    
    blockChecker = True
    if blockChecker == True:
        if blockCheck() == []:
            BScore.wins += 1    # How to increment the score!
            print(f"162 white blocked so BScore.wins {BScore.wins}")
            gameOver = True 
            blockChecker = False
            
    if clickWP == True:
        # if RD on same square as WP then deactivate RDflag2
        for RD in RDList:
            if RD.redDotflag2 == True:
                RD.redDotflag2 = False
        mytuple = WP_toFrom()   # got WP toFrom values
        print(f"124 new tuple {mytuple}")
        clickWP = False
        # turn WPflag1 off immediately!
        for WP in WPList:
            WP.WPflag1 = False
    # only run redDots & rearrange_PL for real fromList values
    #print(f"130 mytuple white {mytuple}")
    # list necessary?
    list =[[0],[1],[2],[3],[4],[5],[6],[0,0], [1,1],[2,2],[4,4],[5,5],[3,3]]
    if mytuple[0] in list:  # if legitimate move fromList
        redDots(*mytuple) # red dots appear
        
        rearrange_pieceList(pieceList, *mytuple ) 
        #print("191 pieces rearranged done")
    
        piecesShow(pieceList)
    BP.BPflag = True

def BPmove():
    if BP.BPflag == True:
        
        piecesShow(pieceList)
        global moveNum
        # get BP toFrm values and move BP (randomly for now) & rearrange pieceList
        moveBP(pieceList, *to_from_BP()) #unpack tuple
        piecesShow(pieceList)
        BP.BPflag = False   # stop BP moving
        moveNum += 1
    
def piecesShow(pieceList): # show WPs and BPs
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

# get WP toFrom values    
def WP_toFrom():
    for WP in WPList:
        if WP.WPflag1 == True:    #true only for the WP rect clicked 
            fromList = []   # place here, otherwise new values are added to old!
            toList = []
        #Get the pieceList index of the square for the WP which has been clicked
            square = pieceList.index(WP)
            if square < 9: # avoid captured WPs on squares 9, 10, 11
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
            return fromList, toList

def blockCheck():
    if blockChecker == True:
        fromBlockList = []  # only need from or to values, not both
        for squares, WP in enumerate(pieceList):
            for num, WP in enumerate(WPList):
                #Get the  squares for each WP
                if pieceList[squares] == WPList[num]:
                    if squares < 9: # avoid captured WPs on squares 9, 10, 11
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
        return fromBlockList

def redDots(fromList, toList):      
    # show clickable red dots on screen in correct positions using to lists
    if len(toList) == 1:
        RD1.redDotRect.topleft = (RD1.pos(boardDict, toList[0]))
        if RD1.concealFlag == False:
            screen.blit(RD1.redDotImg,(RD1.redDotRect))
        elif RD1.concealFlag == True:
            screen.blit(RD1.RDConceal,(RD1.redDotRect))
    elif len(toList)==2:
        for num, RD in enumerate(RDList):   # loop through RD1, RD2
            RD.redDotRect.topleft = (RD.pos(boardDict, toList[num]))
            if RD.concealFlag == False:
                screen.blit(RD.redDotImg,(RD.redDotRect))
            elif RD.concealFlag == True:
                screen.blit(RD1.RDConceal,(RD1.redDotRect))
                
def rearrange_pieceList(pieceList, fromList, toList):     
    global moveNum
    global  gameOver
    global whiteMove
    # Make WP move (rearrange pieceList) when RD clicked then deactivate flags
    if len(toList) == 1: # only one move possible
        if RD1.redDotflag2 == True: # True when RD1 clicked
            start = fromList[0]
            end = toList[0]
            getPawn = pieceList[start]
            pieceList[end] = getPawn # move correct WP
            pieceList[start] = None  # WP has left this square
            if end == 6 or end == 7  or end == 8:
                print("308 white wins reaches third row")
                print("WP disappears! rearrange revisited!")
                WScore.wins += 1
                print(f"311 WScore.wins  {WScore.wins}")
                gameOver = True
                BP.BPmove = False
                # make all WPs white
                for WP in WPList:
                    WP.WPflag2 = False
                RD1.redDotflag2 = False # disable click immediately!!
                RD1.concealFlag = True
                
                return "317 white reaches 3rd row"
            RD1.redDotflag2 = False # disable click immediately!!
            moveNum += 1 # wait for white move to finish before black move
            # make all WPs white
            for WP in WPList:
                WP.WPflag2 = False
            RD1.concealFlag = True
    elif len(toList) == 2:
        for num, RD in enumerate(RDList):
            if RD.redDotflag2 == True:
                start = fromList[num]
                end = toList[num]
                getPawn = pieceList[start]
                pieceList[end] = getPawn # move correct WP
                pieceList[start]=None  # WP has left this square
                if end == 6 or end == 7  or end == 8:
                    print("285 white wins reaches third row")
                    WScore.wins += 1
                    print(f"287 WScore.wins  {WScore.wins}")
                    gameOver = True
                RD.redDotflag2 = False # disable click immediately!!
                moveNum += 1 # wait for white move to finish before black move
            # make all WPs white
                for WP in WPList:
                    WP.WPflag2 = False
                for RD in RDList:
                    RD.concealFlag = True
                #return pieceList # unnecessary, why?

# make BP to & from lists    
def to_from_BP():
    fromList =[]
    toList = []
    BPList = []
    # make a list of BP squares
    for key in range(3,9): # check squares 3 to 8
        if pieceList[key] == BP:
            BPList.append(key)  # list of squares containing a BP
    for num in BPList:
        if pieceList[num - 3] == None: # empty square in front of BP
            fromList.append(num)
            toList.append(num - 3)

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
    return fromList, toList
    # this tuple is unpacked by moveBP (currently line 145)

#rearrage pieceList, move random BP
# FL & TL here needed for unpacking of tuple
def moveBP(pieceList, fromList, toList):
    # time.sleep(5)
    global gameOver
    if len(fromList) == 0:
        print("372 black blocked, white wins")
        WScore.wins +=1
        print (f"374 WScore.wins {WScore.wins}")
        gameOver = True
        if gameOver:
            return "black blocked, white wins"
            #sys.exit(0)
    # move random possible black pawn    
    r = random.randint(0, len(fromList)-1)
    BP_fromSq = fromList[r]
    BP_toMoveSq = toList[r]
    difference = fromList[r] - toList[r]
    
    if difference == 2 or difference == 4:
        # find WP that will be captured and move it off the board
        getWP = pieceList[BP_toMoveSq]    # pick up captured pawn
        if pieceList[9] == None:
            pieceList[9] = getWP  #move captured pawn off the board
        elif pieceList[9] != None and pieceList[10] == None:
            pieceList[10] = getWP
        elif pieceList[9] != None and pieceList[10] != None:
            pieceList[11] = getWP
            print("384 all white pawns captured, black wins")
            BScore.wins +=1
            print(f"386 BScore.wins {BScore.wins}")
            gameOver = True
       
    pieceList[BP_toMoveSq] = BP   # rearrange pieceList
    pieceList[BP_fromSq]  = None
    
    if BP_toMoveSq == 0 or BP_toMoveSq == 1 or BP_toMoveSq == 2:
        print ("403 black reaches row 1 wins")
        BScore.wins += 1
        print(f"405 BScore.wins {BScore.wins}")
        gameOver = True
    return (pieceList)

mainWhileCounter = 0   
                   
while True:
    mainWhileCounter = mainWhileCounter + 1 
    #print ( f"279 mainWhileCounter = {mainWhileCounter}")  
    for event in pygame.event.get():
        # any keyboard or mouse event will activate this loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            #pygame.display.update()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            for WP in WPList:
                if WP.WPimgRect.collidepoint(pygame.mouse.get_pos()):
                    WP.WPflag1 = True # flag for clicked WP to from lists
                    WP.WPflag2 = True # flag for clicked WP colour red
                    clickWP = True
                    for RD in RDList:
                        RD.concealFlag = False
                    
            # for flag 2 activate RD1 or 2 when clicked
            for RD in RDList:
                if RD1.redDotRect.collidepoint(pygame.mouse.get_pos()):
                    RD1.redDotflag2 = True # rearrange pieceList
                if RD2.redDotRect.collidepoint(pygame.mouse.get_pos()):
                    RD2.redDotflag2 = True # rearrange pieceList

    grid(settings.bg_colour)
    main() # show pieces and run the game
    # show the scores
    BScore.show_score() 
    WScore.show_score()
       
    pygame.display.flip()   # updates entire display
    clock.tick(1)   # speed up clock later
    
    

    