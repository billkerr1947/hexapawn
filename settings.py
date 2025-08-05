"""hexapawn settings"""
import pygame
# screen settings
screen_width = 750
screen_height = 450
bg_colour = (230,230,230)

# make a dictionary sqNum : pos(x, y)
# all required pawn positions are in this dictionary
boardDict = {0 : (180,320),1 : (330, 320), 2 : (480,320),
             3 : (180, 170), 4 : (330,170),5 : (480, 170),
             6 : (180, 20), 7 : (330,20),8 : (480, 20),
             9: (30,20), 10: (30,170), 11: (30,320), 
             12: (630,20), 13: (630,170), 14: (630,320)}
'''
def grid():
    # draw line grid on screen (must be in while loop)
    pygame.draw.line(screen,"black",start_pos=(150,0),end_pos=(150,450), width = 5)
    pygame.draw.line(screen,"black",start_pos=(300,0),end_pos=(300,450))
    pygame.draw.line(screen,"black",start_pos=(450,0),end_pos=(450,450))
    pygame.draw.line(screen,"black",start_pos=(600,0),end_pos=(600,450), width = 5)
    pygame.draw.line(screen,"black",start_pos=(0,150),end_pos=(750,150))
    pygame.draw.line(screen,"black",start_pos=(0,300),end_pos=(750,300))
'''