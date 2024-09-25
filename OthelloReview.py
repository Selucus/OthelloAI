import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import validMove as vm
import MiniMax as mm
import time
from tkinter import Tk,Label
import MiniMax as mm
import sys
import threading
import multiprocessing

board = '0000000000000000000000000001200000021000000000000000000000000000'


board = board[0:64]
WHITE = '1'
BLACK = '2'
SIZE = 8
PLAYDELAY = 0.4
boards = ['0000000000000000000000000001200000021000000000000000000000000000']
positionsPlayed = []

def summary():
    return boards
def drawBoard(board,pastDifference=0):
    screen.fill(FINW)
    surface.fill((0,0,0,0))
    playingBoard = pygame.draw.rect(screen, ASPARAGUS, (wBuffer, hBuffer, wBoard, hBoard))

    for lineNum in range(9):
        pygame.draw.line(screen, FINB, (wBuffer, hBuffer + lineNum * (hBoard / 8)),
                        (wBuffer + wBoard, hBuffer + lineNum * (hBoard / 8)), max(1, hBoard // 200))
        pygame.draw.line(screen, FINB, (wBuffer + lineNum * (wBoard / 8), hBuffer),
                        (wBuffer + lineNum * (wBoard / 8), hBuffer + hBoard), max(1, wBoard // 200))

    #if pastDifference != 0:
     #   board = boards[-(pastDifference+1)]

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
    if white > 0:
        whiteText = font.render(str(white), True, FINP)
        whiteRect  = whiteText.get_rect()
        whiteRect.center = ((width//4 + 0.5*((width//2) * wProportion)),sliderBuffer + 0.5*(hBuffer - 2 * sliderBuffer))
        surface.blit(whiteText,whiteRect)

    if black > 0:
        blackText = font.render(str(black),True,FINP)
        blackRect = blackText.get_rect()
        blackRect.center = ((width//4 + (width//2) * wProportion) + 0.5*((width//2) * bProportion),sliderBuffer + 0.5*(hBuffer - 2 * sliderBuffer))
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


    #highlightBest(bestMoves[len(boards)-pastDifference-1])

    changeEvaluation()
    
    screen.blit(surface, (0, 0))
    pygame.display.update()
    return playingBoard

def end(board):
    white, black = mm.countTiles(board)
    endText = ""
    if white < black:
        endText = ("Black wins {b}-{w}".format(b=black,w=white))
    elif black < white:
        endText = ("White wins {w}-{b}".format(b=black,w=white))
    else:
        endText = ("Draw: {w}-{b}".format(b=black,w=white))
    mm.closeTable()
    
    window = Tk()
    lbl=Label(window, text=endText, fg='blue', font=("Helvetica", 16))
    lbl.place(x=5, y=5)
    window.title('')
    window.geometry("200x50+10+10")
    window.mainloop()

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

def highlightBest(position):
    x = (position%8)
    y = position//8
    x = int((x*wInterval) + wBuffer + (wInterval//2))
    y = int((y*hInterval) + hBuffer + (hInterval//2))
    pygame.draw.rect(surface, FINR, pygame.Rect(x-(0.5*wInterval)+(wBoard//200),y-(0.5*hInterval) + (hBoard//200),wInterval-1*(wBoard//200),hInterval-1*(hBoard//200)),2)
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

# Procedure to calculate the size of the evaluation text based upon window size and write the current evaluation
def changeEvaluation():
    global evaluations
    sliderBuffer = int(min(height,width)*0.01)
    font = pygame.font.SysFont('didot.tcc', int((hBuffer - 2 * sliderBuffer)*0.8))

    
    evalXCentre = wBuffer*0.75
    evalYCentre = hBuffer*0.5
    
    try:
        evalText = font.render("Eval: "+str(evaluations[len(boards)-pastDifference-1]),True,(0,0,0))
    except:
        evalText = font.render("Eval: ",True,(0,0,0))

    evalRect = evalText.get_rect()
    evalRect.center = (evalXCentre, evalYCentre)


    pygame.draw.rect(surface, FINW,(0,0,wBuffer*2,hBuffer*0.9))
    surface.blit(evalText,evalRect)
    

def review(reviewBoards):
    global boards
    boards = reviewBoards
    global pastDifference
    pastDifference = len(boards)-1

    
    # Generate positionsPlayed based on what changes between board states
    global positionsPlayed
    prev = boards[0]
    for item in boards[1:]:
        for index in range(len(item)):
            if prev[index] == "0" and (item[index] == "2" or item[index] == "1"):
                positionsPlayed.append(index)
        prev = item
    
    # Begin calculating a prelimenary best move in each position at depth 1
    bestMovesThread = threading.Thread(target=lambda: genBestMoves(boards,1))
    bestMovesThread.start()

    # Run the main board interface at the same time
    main()



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
FINR = (239,71,111)
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



# A value to store how far away from the current playing position we are when the player is using arrows to view past board states
pastDifference = 0

inPresent = True # Whether or not most recent game-state is shown




playingBoard = drawBoard(board,pastDifference)
drawOptions(BLACK,boards[0])


def main():
    global pastDifference
    running = True
    prevPastDifference = 0
    while running:
        
        if len(bestMoves)>(len(boards)-pastDifference-1):
            # Highlight the best move
            highlightBest(bestMoves[len(boards)-pastDifference-1])
            # If we are still looking at the same board state as before
            if prevPastDifference == pastDifference:
                # If the running thread has terminated
                if not bestMoveThread.is_alive():
                    #Increase the depth
                    depth = depth + 2
                    # Update the evaluation display
                    changeEvaluation()
                    pygame.display.update()
                    # Start a new thread at the greater depth
                    bestMoveThread = threading.Thread(target=lambda: genBestMove(boards[len(boards)-pastDifference-1],depth))
                    bestMoveThread.start()
            else:
                # If the board state has changed

                # Update the previous board state is now the current one
                prevPastDifference = pastDifference

                # Update the evaluation display for the new board state
                changeEvaluation()
                pygame.display.update()

                # Reset the depth and begin the first thread
                depth = 2
                bestMoveThread = threading.Thread(target=lambda: genBestMove(boards[len(boards)-pastDifference-1],depth))
                bestMoveThread.start()
            
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:

                if True:
                    #arrows
                    #<< < > >>
                    # 9 characters
                    xPos,yPos = pygame.mouse.get_pos()
                    if  arrowXCentre-(arrowsWidth//2)  <= xPos <= arrowXCentre+(arrowsWidth//2) and arrowYCentre-(arrowsHeight//2)  <= yPos <= arrowYCentre+(arrowsHeight//2):
                        # arrows have been clicked, decide which arrow it is

                        xDistance = xPos - (arrowXCentre-(arrowsWidth//2))
                        clicked = xDistance // (arrowsWidth//9)
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
                        inPresent = False
                        playingBoard = drawBoard(board,pastDifference)
                        
                        if pastDifference !=len(boards)-1:
                            drawOptions(boards[-(pastDifference)][(positionsPlayed[-(pastDifference)])],boards[-(pastDifference+1)])
                        else:
                            drawOptions(BLACK,boards[0])

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
                inPresent = False
                playingBoard = drawBoard(board,pastDifference)
                if pastDifference !=len(boards)-1:
                    drawOptions(boards[-(pastDifference)][(positionsPlayed[-(pastDifference)])],boards[-(pastDifference+1)])
                else:
                    drawOptions(BLACK,boards[0])
                        
                
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
             

            elif event.type == pygame.QUIT:
                running = False

    pygame.quit()


bestMoves = []
evaluations = []


# Function to generate the best move in a single position that is called
# With increasing depth for more and more accuracy
def genBestMove(board,depth):
    global bestMoves,evaluations
    index = boards.index(board)
    curPlayer = boards[index+1][positionsPlayed[index]]
    val, position = mm.minimaxUnlimited(board,depth,curPlayer == WHITE,1,len(boards),float("-inf"),float("inf"),[])
    bestMoves[index] = position
    evaluations[index] = val
    return position


# Procedure to generate a preliminary best move in every position
# with a limited depth for speed
def genBestMoves(boards,depth):
    global bestMoves,evaluations
    for index,board in enumerate(boards[:len(boards)-1]):
        curPlayer = boards[index+1][positionsPlayed[index]]        
        val, position = mm.minimaxUnlimited(board,depth,curPlayer == WHITE,1,len(boards),float("-inf"),float("inf"),[])
        bestMoves.append(position)
        evaluations.append(val)
    



    
