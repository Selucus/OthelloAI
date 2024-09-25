import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Prevent pygame startup information from showing
import pygame
import validMove as vm
import MiniMax as mm
import time
import random
from tkinter import Tk,Label

# Initialise the board
board = '0000000000000000000000000001200000021000000000000000000000000000'

# Set constants used
WHITE = '1'
BLACK = '2'
SIZE = 8
PLAYDELAY = 0.4

# Create the structures to store the boards and positions played
boards = [board]
positionsPlayed = []


# Function to return the board states over the game to be stored in the database
def summary():
    return [boards,difficulty]


# Function to draw the game window and board
def drawBoard(board,pastDifference=0):
    # Clear the gamewindwow by painting the screen and surface white
    screen.fill(FINW)
    surface.fill((0,0,0,0))

    # Draw the green playing board
    playingBoard = pygame.draw.rect(screen, ASPARAGUS, (wBuffer, hBuffer, wBoard, hBoard))

    # Draw the grid lines on the board
    for lineNum in range(9):
        pygame.draw.line(screen, FINB, (wBuffer, hBuffer + lineNum * (hBoard / 8)),
                        (wBuffer + wBoard, hBuffer + lineNum * (hBoard / 8)), max(1, hBoard // 200))
        pygame.draw.line(screen, FINB, (wBuffer + lineNum * (wBoard / 8), hBuffer),
                        (wBuffer + lineNum * (wBoard / 8), hBuffer + hBoard), max(1, wBoard // 200))


    # If currently looking at past board state, set the board to draw to be the past board
    if pastDifference != 0:
        board = boards[-(pastDifference+1)]
        
    # Iterate through the pieces of the board and draw them
    for count,item in enumerate(board):
        if item != "0":
            drawPiece(count,item)
    

    # Drawing the slider at the top of the board
    
    white, black = mm.countTiles(board)
    # Find the percentage of pieces that are black or white
    wProportion = white / (white + black)
    bProportion = 1 - wProportion
    sliderWidth = wBoard // 2
    sliderBuffer = int(min(height,width)*0.01)
    # Draw the slider
    pygame.draw.rect(screen,FINB,(width//4,sliderBuffer,
                                  (width//2) * wProportion,hBuffer - 2 * sliderBuffer),1)
    pygame.draw.rect(screen,FINB,(width//4 + (width//2) * wProportion,sliderBuffer,
                                  (width//2) * bProportion,hBuffer - 2 * sliderBuffer))


    # Load the font to display the slider text at the right size
    font = pygame.font.SysFont('didot.tcc', int((hBuffer - 2 * sliderBuffer)*0.8))
    if white > 0:
        # Render white text if there are tiles on the board
        whiteText = font.render(str(white), True, FINP)
        whiteRect  = whiteText.get_rect()
        whiteRect.center = ((width//4 + 0.5*((width//2) * wProportion)),
                            sliderBuffer + 0.5*(hBuffer - 2 * sliderBuffer))
        surface.blit(whiteText,whiteRect)

    if black > 0:
        # Render black text if there are tiles on the board
        blackText = font.render(str(black),True,FINP)
        blackRect = blackText.get_rect()
        blackRect.center = ((width//4 + (width//2) * wProportion) + 0.5*((width//2) * bProportion),
                            sliderBuffer + 0.5*(hBuffer - 2 * sliderBuffer))
        surface.blit(blackText,blackRect)
    
    
    # Highlight the most recent move in the current position as long as it is not the starting position
    if boards.index(board) != 0:
        highlightRecent(positionsPlayed[boards.index(board)-1])



    # Render the arrows to allow the user to click forward and backward through the game
    global arrowsHeight,arrowsWidth, arrowXCentre,arrowYCentre
    arrowXCentre = width - wBuffer*1.75
    arrowYCentre = height - hBuffer*0.5
    
    arrows = font.render("<< <  > >>",True,(0,0,0))
    arrowsRect = arrows.get_rect()
    arrowsRect.center = (arrowXCentre,arrowYCentre)
    surface.blit(arrows,arrowsRect)
    
    arrowsHeight,arrowsWidth = arrows.get_height(),arrows.get_width()
    

    # Render the quit text as a button for the user
    global quitHeight,quitWidth,quitXCentre,quitYCentre

    quitXCentre = wBuffer*1.75
    quitYCentre = height - hBuffer*0.5

    quitButton = font.render("quit",True,(0,0,0))
    quitRect = quitButton.get_rect()
    quitRect.center = (quitXCentre,quitYCentre)
    surface.blit(quitButton,quitRect)
    quitHeight,quitWidth = quitButton.get_height(),quitButton.get_width()

    # Render the surface and update the screen
    screen.blit(surface, (0, 0))
    pygame.display.update()
    return playingBoard


# Procedure to be run when the match finishes
def end(board):
    # Print the scores of the match
    white, black = mm.countTiles(board)
    endText = ""
    if white < black:
        endText = ("Black wins {b}-{w}".format(b=black,w=white))
    elif black < white:
        endText = ("White wins {w}-{b}".format(b=black,w=white))
    else:
        endText = ("Draw: {w}-{b}".format(b=black,w=white))

    # Close the transposition table file 
    mm.closeTable()

    # Create and display the pop-up label of the score
    window = Tk()
    lbl=Label(window, text=endText, fg='blue', font=("Helvetica", 16))
    lbl.place(x=5, y=5)
    window.title('')
    window.geometry("200x50+10+10")
    window.mainloop()


# Procedure to find all the valid moves for a colour and draw them as options
def drawOptions(colour,board):
    locations = mm.findAllPieces(colour,board)
    validPositions = mm.findAllValid(colour,locations,board)
    for item in validPositions:
        drawPiece(item,3)
    pygame.display.update()
        
# Procedure to draw either a piece or an indicator that there is a valid move
def drawPiece(position, colour):
    """
    colour 1 is white
    colour 2 is black
    colour 3 is pink
    """

    # Calculate the x and y location of where the circle is going to be drawn
    x = (position%8)
    y = position//8
    x = int((x*wInterval) + wBuffer + (wInterval//2))
    y = int((y*hInterval) + hBuffer + (hInterval//2))
    if colour == WHITE:
        # Draw a white circle
        pygame.draw.circle(screen, FINW, (x, y), int(min(wInterval,hInterval) * 0.35))
    elif colour == BLACK:
        # Draw a black circle
        pygame.draw.circle(screen, FINB, (x, y), int(min(wInterval,hInterval) * 0.35))
    else:
        # Slightly smaller semi-transparent circle to be used for valid move indicator
        pygame.draw.circle(surface, FINP, (x, y), int(min(wInterval,hInterval) * 0.15))
        screen.blit(surface, (0, 0))


# Procedure to highlight the most recently played location on the board
def highlightRecent(position):

    # Calculate the x and y location of the tile to be highlighted
    x = (position%8)
    y = position//8
    x = int((x*wInterval) + wBuffer + (wInterval//2))
    y = int((y*hInterval) + hBuffer + (hInterval//2))

    # Draw a rectangle around the tile highlighting it
    pygame.draw.rect(surface, YELLOW, pygame.Rect(x-(0.5*wInterval)+(wBoard//200),y-(0.5*hInterval) + (hBoard//200),wInterval-1*(wBoard//200),hInterval-1*(hBoard//200)),1)
    screen.blit(surface, (0, 0))
    pygame.display.update()




# Ask the user if they want to play as white, black or a random colour
answer = "-1"
options = ["1","2","3"]
while answer not in options:
    answer = input("Would you like to play as:\nWhite: 1\nBlack: 2\nRandom: 3\n")

# Select a random colour if selected
if answer == "3":
    import random
    answer = str(random.randint(1,2))
    if answer == "1":
        print("You are White")
    else:
        print("You are Black")

# Set the AI colour to the opposite of the player
AIplayer = str(3-int(answer))
player = answer


# Ask which difficulty they wish to play
options = ["1","2","3","4","5"]
answer = "-1"
while answer.lower() not in options:
    answer = input ("""Which difficulty do you wish to play on:\nBeginner: 1\nEasy: 2\nMedium: 3\nHard: 4\nExpert: 5\n""")

# Set the difficulty string to be stored in the database
# Set the depth of the AI based on the difficulty
if answer == "1":
    difficulty = "Beginner"
    depth = -1
elif answer == "2":
    difficulty = "Easy"
    depth = 0
elif answer == "3":
    difficulty = "Medium"
    depth = 1
elif answer == "4":
    difficulty = "Hard"
    depth = 3
elif answer == "5":
    difficulty = "Expert"
    depth = 5


# Initialise the pygame window 
width = 600
height = 600
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
surface = pygame.Surface((width, height), pygame.SRCALPHA)

# Define the colour RGB values
YELLOW = (252, 252, 98)
FINP = (252, 74, 157)
FINB = (10, 10, 11)
FINW = (243, 243, 246)
ASPARAGUS = (90, 157, 67)

wBuffer = int(width * 0.1)  # gap between side of the window and start of board (width-wise)
hBuffer = int(height * 0.1)  # gap between top of the window and side of board (height-wise)
hBoard = height - 2 * hBuffer
wBoard = width - 2 * wBuffer



# Iterate through and generate all the X,Y positions of the centres of the tiles on the board
positions = []
hInterval = hBoard / 8
wInterval = wBoard / 8
for row in range(8):
    for col in range(8):
        positions.append(((wBuffer + wInterval // 2 + wInterval * col),
                          (hBuffer + hInterval // 2 + hInterval * row)))
count = 0

# Set the starting player to be Black
curPlayer = BLACK



# Initialise location values 
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

running = True # Boolean to store if the match is in progress

while running:

    if curPlayer == AIplayer and inPresent:

        # Generate all possible AI moves
        AILocations = mm.findAllPieces(curPlayer,board)
        AIValidPositions = mm.findAllValid(curPlayer,AILocations,board)

        if len(AIValidPositions) != 0: # If there is a location where the AI can play
            if depth == -1:
                # Beginner difficulty so pick random location to play
                randomIndex= random.randint(0,len(AIValidPositions)-1)
                position = AIValidPositions[randomIndex]
                
            elif depth == 0:
                # Easy difficulty so pick the move that maximises the number of AI tiles
                position = mm.easyAI(board,curPlayer)
            else:
                # Medium or above so use MiniMax algorithm with the depth set by difficulty
                val, position = mm.minimax(board,depth,curPlayer == WHITE,1,len(boards),float("-inf"),float("inf"),[])
                

            board = mm.flipAll(curPlayer,position,board) # Flip all the pieces
            boards.append(board) # Add the board to the list of baord states
            positionsPlayed.append(position) # Add the location played to a list of all past locations

            # Draw the most recent played piece
            drawPiece(position,curPlayer)
            highlightRecent(position)

            # Add a short constant delay between playing the piece and flipping the pieces
            # This allows the user to better see what is happening
            time.sleep(PLAYDELAY)

            # Update the board
            playingBoard = drawBoard(board,pastDifference)
            
        # AI cannot play or has just played so change current player to the PLAYER
        curPlayer = str(3-int(curPlayer)) 
        playerLocations = mm.findAllPieces(curPlayer,board)
        playerValidPositions = mm.findAllValid(curPlayer,playerLocations,board)
        
        while len(playerValidPositions) == 0:

            #If the player cannot play, check whether the AI also cannot play and if so, the match is finished
            AILocations = mm.findAllPieces(str(3-int(curPlayer)),board)
            AIValidPositions = mm.findAllValid(str(3-int(curPlayer)),AILocations,board)
            if len(AIValidPositions) == 0:
                end(board)
                break

            playingBoard = drawBoard(board,pastDifference)
            
            curPlayer = str(3-int(curPlayer))
            time.sleep(2) # Small delay to allow user to realise they cannot play


            if depth == -1:
                # Beginner difficulty so pick random location to play
                randomIndex= random.randint(0,len(AIValidPositions)-1)
                position = AIValidPositions[randomIndex]
                
            elif depth == 0:
                # Easy difficulty so pick the move that maximises the number of AI tiles
                position = mm.easyAI(board,curPlayer)
            else:
                # Medium or above so use MiniMax algorithm
                val, position = mm.minimax(board,depth,curPlayer == WHITE,1,len(boards),float("-inf"),float("inf"),[])
                

            # Draw the piece and update the board
            board = mm.flipAll(curPlayer,position,board)
            positionsPlayed.append(position)
            boards.append(board)
            drawPiece(position,curPlayer)

            time.sleep(PLAYDELAY)
            
            # Draw the options for the player
            curPlayer = str(3-int(curPlayer))
            drawOptions(curPlayer,board)
            playerLocations = mm.findAllPieces(curPlayer,board)
            playerValidPositions = mm.findAllValid(curPlayer,playerLocations,board)
            
        playingBoard = drawBoard(board,pastDifference)
        drawOptions(curPlayer,board)
        
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:

            # If the board has been clicked and the current board state is the most recent board
            if playingBoard.collidepoint(pygame.mouse.get_pos()) and inPresent:

                # Find the position of the press
                boardPos = (wBuffer, hBuffer)
                relativePos = (pygame.mouse.get_pos()[0] - boardPos[0],
                               pygame.mouse.get_pos()[1] - boardPos[1])
                curX = int(relativePos[0] // wInterval)
                curY = int(relativePos[1] // hInterval)
                position = curX + curY*SIZE

                # Check if the user has clicked a valid position
                locations = mm.findAllPieces(player,board)
                validPositions = mm.findAllValid(player,locations,board)
    
                if (position in validPositions):
                    # Play the move clicked by the user
                    board = mm.flipAll(player,position,board)
                    boards.append(board)
                    positionsPlayed.append(position)
                    playingBoard = drawBoard(board,pastDifference)
                    curPlayer = AIplayer
            else:
                #arrows
                #<< < > >>
                # 9 characters
                xPos,yPos = pygame.mouse.get_pos()
                if  arrowXCentre-(arrowsWidth//2)  <= xPos <= arrowXCentre+(arrowsWidth//2) and arrowYCentre-(arrowsHeight//2)  <= yPos <= arrowYCentre+(arrowsHeight//2):
                    # arrows have been clicked, decide which arrow it is

                    xDistance = xPos - (arrowXCentre-(arrowsWidth//2))
                    clicked = xDistance // (arrowsWidth//9)
  

                    if 0 <= clicked <= 1:
                        pastDifference = len(boards) -1  # Set the difference to the maximum
                    elif 3 <= clicked <= 3:
                        pastDifference += 1 # Increase the difference, stepping backwards
                    elif 5 <= clicked <= 5:
                        pastDifference -= 1 # Decrease the difference, stepping forwards
                    elif 7 <= clicked <= 8:
                        pastDifference = 0 # Set the difference back to the present

                    # Restrict the difference to not cause an error
                    pastDifference = min(pastDifference,len(boards)-1)
                    pastDifference = max(pastDifference,0)

                    # Redraw the board in the new state
                    if pastDifference != 0:
                        inPresent = False
                        playingBoard = drawBoard(board,pastDifference)
                    else:
                        inPresent = True
                        playingBoard = drawBoard(board,pastDifference)
                        drawOptions(curPlayer,board)
                
                # Check if the quit button is pressed
                elif quitXCentre-(quitWidth//2) <= xPos <= quitXCentre+(quitWidth//2) and quitYCentre-(quitHeight//2) <= yPos <= quitYCentre+(quitHeight//2):
                    # Close and save the transposition table then quit the program
                    mm.closeTable()
                    running = False
        # Check if an arrowkey is pressed
        elif event.type == pygame.KEYDOWN:

            # Step forwards or backwards based on the direction of the arrow key
            if event.key == pygame.K_LEFT:
                pastDifference += 1
            elif event.key == pygame.K_RIGHT:
                pastDifference -= 1


            # Restrict the difference to not cause an error
            pastDifference = min(pastDifference,len(boards)-1)
            pastDifference = max(pastDifference,0)

            # Redraw the board in the new state
            if pastDifference != 0:
                inPresent = False
                playingBoard = drawBoard(board,pastDifference)
            else:
                inPresent = True
                playingBoard = drawBoard(board,pastDifference)
                drawOptions(curPlayer,board)

        # Check if the game window size has been changed
        elif event.type == pygame.VIDEORESIZE:

            # Save the new width and height of the window
            # Update the size of the screen and surface to match this
            width, height= event.w,event.h
            screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
            surface = pygame.Surface((width, height), pygame.SRCALPHA)


            # Calculate new board widths and buffers
            wBuffer = int(width * 0.1)  
            hBuffer = int(height * 0.1)  
            hBoard = height - 2 * hBuffer
            wBoard = width - 2 * wBuffer


            # Recalculate the positions of each playing square
            positions = []
            hInterval = hBoard / 8
            wInterval = wBoard / 8
            for row in range(8):
                for col in range(8):
                    positions.append(((wBuffer + wInterval // 2 + wInterval * col),
                          (hBuffer + hInterval // 2 + hInterval * row)))

            # Draw the updated board 
            playingBoard = drawBoard(board,pastDifference)
            drawOptions(curPlayer,board)

        # Check if the window close button is pressed
        elif event.type == pygame.QUIT:
            # Close and save the lookup table and quit the program
            mm.closeTable()
            running = False

# Close the pygame window and stop all processes
pygame.quit()
