import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import validMove as vm
import MiniMax as mm
import time
board = '0000000000000000000000000001200000021000000000000000000000000000'
#board = '0000000000000000000000000001200000021000000000010022211100111111'

board = board[0:64]
WHITE = '1'
BLACK = '2'
SIZE = 8
PLAYDELAY = 0.4
boards = []
boards.append(board)
positionsPlayed = []


def summary():
    return boards,"PvP"
def drawBoard(board,pastDifference):
    screen.fill(FINW)
    surface.fill((0,0,0,0))
    playingBoard = pygame.draw.rect(screen, ASPARAGUS, (wBuffer, hBuffer, wBoard, hBoard))

    for lineNum in range(9):
        pygame.draw.line(screen, FINB, (wBuffer, hBuffer + lineNum * (hBoard / 8)),
                        (wBuffer + wBoard, hBuffer + lineNum * (hBoard / 8)), max(1, hBoard // 200))
        pygame.draw.line(screen, FINB, (wBuffer + lineNum * (wBoard / 8), hBuffer),
                        (wBuffer + lineNum * (wBoard / 8), hBuffer + hBoard), max(1, wBoard // 200))

    if pastDifference != 0:
        board = boards[-(pastDifference+1)]
    count = 0
    for count,item in enumerate(board):
        if item != "0":
            drawPiece(count,item)
    

    # rectangle spans from halfway +- width/4
    # from y =0 to HBuffer
    white, black = mm.countTiles(board)
    wProportion = white / (white + black)
    bProportion = 1 - wProportion
    sliderWidth = wBoard // 2
    sliderBuffer = int(min(height,width)*0.01)
    
    pygame.draw.rect(screen,FINB,(width//4,sliderBuffer,(width//2) * wProportion,hBuffer - 2 * sliderBuffer),1)
    pygame.draw.rect(screen,FINB,(width//4 + (width//2) * wProportion,sliderBuffer,(width//2) * bProportion,hBuffer - 2 * sliderBuffer))
    t0 = time.time()
    font = pygame.font.SysFont('didot.tcc', int((hBuffer - 2 * sliderBuffer)*0.8))
    whiteText = font.render(str(white), True, FINP)
    whiteRect  = whiteText.get_rect()
    blackText = font.render(str(black),True,FINP)
    blackRect = blackText.get_rect()
    whiteRect.center = ((width//4 + 0.5*((width//2) * wProportion)),sliderBuffer + 0.5*(hBuffer - 2 * sliderBuffer))
    blackRect.center = ((width//4 + (width//2) * wProportion) + 0.5*((width//2) * bProportion),sliderBuffer + 0.5*(hBuffer - 2 * sliderBuffer))
    surface.blit(whiteText,whiteRect)
    surface.blit(blackText,blackRect)
    
    
    # Highlight the most recent move in the current position
    # as long as it is not the starting position
    if boards.index(board) != 0:
        highlightRecent(positionsPlayed[boards.index(board)-1])

    global arrowsHeight,arrowsWidth, arrowXCentre,arrowYCentre
    arrowXCentre = width - wBuffer*1.75
    arrowYCentre = height - hBuffer*0.5
    
    arrows = font.render("<< <  > >>",True,(0,0,0))
    arrowsRect = arrows.get_rect()
    arrowsRect.center = (arrowXCentre,arrowYCentre)
    surface.blit(arrows,arrowsRect)
    
    arrowsHeight,arrowsWidth = arrows.get_height(),arrows.get_width()
    
    
    global quitHeight,quitWidth,quitXCentre,quitYCentre

    quitXCentre = wBuffer*1.75
    quitYCentre = height - hBuffer*0.5

    quitButton = font.render("quit",True,(0,0,0))
    quitRect = quitButton.get_rect()
    quitRect.center = (quitXCentre,quitYCentre)
    surface.blit(quitButton,quitRect)
    quitHeight,quitWidth = quitButton.get_height(),quitButton.get_width()


    screen.blit(surface, (0, 0))
    pygame.display.update()
    return playingBoard

def end(board):
    white, black = mm.countTiles(board)
    if white < black:
        print("Black wins {b}-{w}".format(b=black,w=white))
    elif black < white:
        print("White wins {w}-{b}".format(b=black,w=white))
    else:
        print("Draw: {w}-{b}".format(b=black,w=white))
    mm.closeTable()

def drawOptions(colour,board):
    locations = mm.findAllPieces(colour,board)
    validPositions = mm.findAllValid(colour,locations,board)
    for item in validPositions:
        #highlightRecent(item)
            
        drawPiece(item,3)

def drawPiece(position, colour):
    """
    colour 1 is white
    colour 2 is black
    colour 3 is pink
    """
    x = (position%8)
    y = position//8
    x = int((x*wInterval) + wBuffer + (wInterval//2))
    y = int((y*hInterval) + hBuffer + (hInterval//2))
    if colour == WHITE:
        pygame.draw.circle(screen, FINW, (x, y), int(min(wInterval,hInterval) * 0.35))
    elif colour == BLACK:
        pygame.draw.circle(screen, FINB, (x, y), int(min(wInterval,hInterval) * 0.35))
    else:
        # Slightly smaller semi-transparent circle to be used for valid move indicator
        pygame.draw.circle(surface, FINP, (x, y), int(min(wInterval,hInterval) * 0.15))
        screen.blit(surface, (0, 0))
    pygame.display.update()

def highlightRecent(position):
    x = (position%8)
    y = position//8
    x = int((x*wInterval) + wBuffer + (wInterval//2))
    y = int((y*hInterval) + hBuffer + (hInterval//2))
    #hBoard/200
    pygame.draw.rect(surface, YELLOW, pygame.Rect(x-(0.5*wInterval)+(wBoard//200),y-(0.5*hInterval) + (hBoard//200),wInterval-1*(wBoard//200),hInterval-1*(hBoard//200)),1)
    screen.blit(surface, (0, 0))
    pygame.display.update()





curPlayer = "2"





width = 600
height = 600
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
surface = pygame.Surface((width, height), pygame.SRCALPHA)
YELLOW = (252, 252, 98)
FINP = (252, 74, 157)
FINB = (10, 10, 11)
FINW = (243, 243, 246)
ASPARAGUS = (90, 157, 67)

wBuffer = int(width * 0.1)  # gap between side of the window and start of board (width-wise)
hBuffer = int(height * 0.1)  # gap between top of the window and side of board (height-wise)
hBoard = height - 2 * hBuffer
wBoard = width - 2 * wBuffer


positions = []
hInterval = hBoard / 8
wInterval = wBoard / 8
for row in range(8):
    for col in range(8):
        positions.append(((wBuffer + wInterval // 2 + wInterval * col),
                          (hBuffer + hInterval // 2 + hInterval * row)))
count = 0

curPlayer = BLACK




arrowXCentre = width - wBuffer*1.75
arrowYCentre = height - hBuffer*0.5
arrowsHeight = 0
arrowsWidth = 0
quitXCentre = 0
quitYCentre = 0
quitHeight = 0
quitWidth = 0

running = True

# A value to store how far away from the current playing position we are when the player is using arrows to view past board states
pastDifference = 0

inPresent = True # Whether or not most recent game-state is shown




playingBoard = drawBoard(board,pastDifference)



finished = False

while running:
    locations = mm.findAllPieces(curPlayer,board)
    validPositions = mm.findAllValid(curPlayer,locations,board)
    if len(validPositions) == 0 and not finished:
        print("Black" if curPlayer=="2" else "White", "can't play")
        curPlayer = str(3-int(curPlayer))
        if not finished:
            locations = mm.findAllPieces(curPlayer,board)
            validPositions = mm.findAllValid(curPlayer,locations,board)
            if len(validPositions) == 0:
                print("Black" if curPlayer=="2" else "White", "also cant play")
                end(board)
                finished = True
            else:
                drawOptions(curPlayer,board)

    
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:

            if playingBoard.collidepoint(pygame.mouse.get_pos()) and inPresent:
                boardPos = (wBuffer, hBuffer)
                relativePos = (pygame.mouse.get_pos()[0] - boardPos[0], pygame.mouse.get_pos()[1] - boardPos[1])
                #tileNumber = (relativePos[0] // wInterval) + (relativePos[1] // hInterval) * 8
                curX = int(relativePos[0] // wInterval)
                curY = int(relativePos[1] // hInterval)
                position = curX + curY*SIZE
                
                locations = mm.findAllPieces(curPlayer,board)
                validPositions = mm.findAllValid(curPlayer,locations,board)
                
                if len(validPositions) == 0:
                    end(board)
                if (position in validPositions):
                
                    board = mm.flipAll(curPlayer,position,board)
                    boards.append(board)
                    positionsPlayed.append(position)
                    """highlightRecent(position)
                    drawPiece(position,curPlayer)
                    time.sleep(PLAYDELAY)"""
                    playingBoard = drawBoard(board,pastDifference)
                    
                    #time.sleep(2)
                    curPlayer = str(3-int(curPlayer))
                    locations = mm.findAllPieces(curPlayer,board)
                    validPositions == mm.findAllValid(curPlayer,locations,board)
                    if len(validPositions) == 0:
                        curPlayer = str(3-int(curPlayer))
                        locations = mm.findAllPieces(curPlayer,board)
                        validPositions == mm.findAllValid(curPlayer,locations,board)
                        if len(validPositions) == 0:
                            end(board)
                    else:
                        drawOptions(curPlayer,board)
            else:
                #arrows
                #<< < > >>
                # 9 characters
                xPos,yPos = pygame.mouse.get_pos()
                if  arrowXCentre-(arrowsWidth//2)  <= xPos <= arrowXCentre+(arrowsWidth//2) and arrowYCentre-(arrowsHeight//2)  <= yPos <= arrowYCentre+(arrowsHeight//2):
                    # arrows have been clicked, decide which arrow it is

                    xDistance = xPos - (arrowXCentre-(arrowsWidth//2))
                    clicked = xDistance // (arrowsWidth//9)
                    #print("Distance along",xDistance, "so clicked", clicked)

                    if 0 <= clicked <= 1:
                        pastDifference = len(boards) -1
                    elif 3 <= clicked <= 3:
                        pastDifference += 1
                    elif 5 <= clicked <= 5:
                        pastDifference -= 1
                    elif 7 <= clicked <= 8:
                        pastDifference = 0

                    pastDifference = min(pastDifference,len(boards)-1)
                    pastDifference = max(pastDifference,0)
                    if pastDifference != 0:
                        inPresent = False
                        playingBoard = drawBoard(board,pastDifference)
                    else:
                        inPresent = True
                        playingBoard = drawBoard(board,pastDifference)
                        drawOptions(curPlayer,board)
                # quit button

                elif quitXCentre-(quitWidth//2) <= xPos <= quitXCentre+(quitWidth//2) and quitYCentre-(quitHeight//2) <= yPos <= quitYCentre+(quitHeight//2):
                    mm.closeTable()
                    running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pastDifference += 1
            elif event.key == pygame.K_RIGHT:
                pastDifference -= 1



            pastDifference = min(pastDifference,len(boards)-1)
            pastDifference = max(pastDifference,0)
            if pastDifference != 0:
                inPresent = False
                playingBoard = drawBoard(board,pastDifference)
            else:
                inPresent = True
                playingBoard = drawBoard(board,pastDifference)
                drawOptions(curPlayer,board)
        elif event.type == pygame.VIDEORESIZE:
            width, height= event.w,event.h
            screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
            surface = pygame.Surface((width, height), pygame.SRCALPHA)

            wBuffer = int(width * 0.1)  
            hBuffer = int(height * 0.1)  
            hBoard = height - 2 * hBuffer
            wBoard = width - 2 * wBuffer

    
            positions = []
            hInterval = hBoard / 8
            wInterval = wBoard / 8
            for row in range(8):
                for col in range(8):
                    positions.append(((wBuffer + wInterval // 2 + wInterval * col),
                          (hBuffer + hInterval // 2 + hInterval * row)))
            
            playingBoard = drawBoard(board,pastDifference)
            if curPlayer == WHITE:
                drawOptions(WHITE,board)
            else:
                drawOptions(BLACK,board)


        elif event.type == pygame.QUIT:
            running = False

pygame.quit()
print("fini")
