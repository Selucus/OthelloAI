import time
SIZE = 8
WHITE = "1"
BLACK = "2"
LOOKUPSHIFT = 200156682785938776

# Opens the file containing the best moves in each position and creates the file if it doesn't already exist
transpositionTable = open("Table.txt","r+") 
table = transpositionTable.readlines()


boards = []
moves = []
scores = []
lut = {}

# Weights to determine the strength of having a piece in the corner and a 'stable' piece
cornerWeight = 40
stableWeight = 20




# Weights for every position on the board
boardWeights = [30 , -5 , 4 , 3 , 3 , 4 , -5 , 30 ,
                   -5 , -10 , 0 , 0 , 0 , 0 , -10 , -5  ,
                    4 , 0 , 1 , 1 , 1 , 1 , 0 , 4  ,
                    3 , 0 , 1 , 2 , 2 , 1 , 0 , 3  ,
                    3 , 0 , 1 , 2 , 2 , 1 , 0 , 3  ,
                    4 , 0 , 1 , 1 , 1 , 1 , 0 , 4  ,
                    -5 , -10 , 0 , 0 , 0 , 0 , -10 , -5  ,
                    30 , -5 , 4 , 3 , 3 , 4 , -5 , 30   ]


# Table of index values for the corners of the board to allow for faster lookup
cornerLocations = [0,7,56,63]


# Iterate through the data from the transposition table and split it into 3 parallel arrays to allow for easier conversion to the dictionary
for index in range(len(table)):
    boards.append(table[index].split()[0])
    moves.append(int(table[index].split()[1]))
    scores.append(float(table[index].split()[2]))

# Add the data from the transposition data to the dictionary
for index,item in enumerate(boards):
    lut[int(item)] = [moves[index],scores[index]]


# Function to count the number of a certain colour pieces in corners
def cornerCount(board,colour):
    corners = 0
    for index in cornerLocations:
        if board[index] == colour:
            corners += 1
    return corners


board = '0000000000000000000000020002202100022221002222110011111101111111'


# Function to count the number of stable pieces on the board for a given player
def stableGenerater(board,player):
    stableCount = 0
    corners = [0,7,56,63]
    directions = [[1,8],[-1,8],[1,-8],[-1,-8]]
    toCheck = [([-9,-8,-7,-1],[-9,-8,7,-1]),([-9,-8,-7,1],[9,-8,-7,1]),([9,8,7,-1],[-9,8,7,-1]),([9,8,7,1],[9,8,-7,1])]
    stable = []
    for index in range(4):
        # For every corner on the board
        curCorner = corners[index]
        if board[curCorner] == player:
            # If the player we are checking has the corner,
            # the corner is stable so check in both directions
            stableCount += 1
            stable.append(curCorner)
            curPosition = curCorner
            xDirection = directions[index][0]
            yDirection = directions[index][1]
            

            # While a valid stable tile exists from this corner, keep checking
            validFound = True
            while validFound:
                curPosition = curCorner
                validFound = False
                # Start by checking the x direction
                curPosition += xDirection
                # While a valid stable tile exists in the x direction, keep checking
                stableFound = True
                while stableFound:
                    stableFound = False
                    
                    if exists(curPosition,curPosition): 
                        # If we are checking a valid location
                    
                        if board[curPosition] == player:
                            # If every tile in every appropriate direction is stable,
                            # this tile is stable
                            checksPassed = 0
                            for checkIndex in range(4):
                                checking = curPosition + toCheck[index][0][checkIndex]
                                if (checking in stable) or (not exists(curPosition,checking)):
                                    checksPassed += 1
                                    
                            if checksPassed == 4:
                                stableCount += 1
                                stableFound = True
                                validFound = True
                                stable.append(curPosition)
                    # Move onto the next tile
                    curPosition += xDirection

                # Reset the starting position to the corner
                curPosition = curCorner
                
       
                
                curPosition += yDirection
                
                # While a valid stable tile exists in the x direction, keep checking
                stableFound = True
                while stableFound:
                    stableFound = False
                    
                    if exists(curPosition,curPosition):
                        # If we are checking a valid location
                        if board[curPosition] == player:
                            
                            # If every tile in the appropriate direction is stable,
                            # the tile is stable
                            checksPassed = 0
                            for checkIndex in range(4):
                                checking = curPosition + toCheck[index][1][checkIndex]
                                if (checking in stable) or (not exists(curPosition,checking)):
                                    
                                    checksPassed += 1
                            
                            if checksPassed == 4:
                                stableCount += 1
                                stableFound = True
                                validFound = True
                                stable.append(curPosition)

                    # Move onto the next tile
                    curPosition += yDirection
                # Change the corner to be one tile diagonally closer to the centre
                curCorner = curCorner + xDirection + yDirection
                if (curCorner - xDirection) in stable and (curCorner - yDirection) in stable and board[curCorner] == player:
                    stable.append(curCorner)
                    stableCount += 1
                else:
                    validFound = False

    return stableCount

                       
def exists(before,after):
    valid = True
    if after < 0 or after > 63:
        valid = False
    elif abs(after-before) == 1:
        #if we are checking in the x direction:
        if after//8 != before//8:
            # If we have crossed over into the next row
            valid = False
    elif abs(after-before) == 9:
        if before % 8 == 7 or before % 8 == 0:
            valid = False
    elif abs(after-before) == 7:
        if before % 8 == 7 or before % 8 == 0:
            valid = False
        
    return valid

# Function to generate the numerical evaluation of a board
def evaluation(board):
    # Initialise evaluation at 0
    curEval = 0


    # Adjust the evaluation based on the number of white and black corner pieces
    wCorners = cornerCount(board,WHITE)
    bCorners = cornerCount(board,BLACK)
    curEval += (wCorners-bCorners)* cornerWeight


    # If a corner has been taken, run the stable piece checker function
    if wCorners > 0 or bCorners > 0:
        curEval += (stableGenerater(board,"1") - stableGenerater(board,"2")) * stableWeight

    # Commented version of the globally defined boardWeights for ease of understanding
    """boardWeights = [30 , -5 , 4 , 3 , 3 , 4 , -5 , 30 ,
                   -5 , -10 , 0 , 0 , 0 , 0 , -10 , -5  ,
                    4 , 0 , 1 , 1 , 1 , 1 , 0 , 4  ,
                    3 , 0 , 1 , 2 , 2 , 1 , 0 , 3  ,
                    3 , 0 , 1 , 2 , 2 , 1 , 0 , 3  ,
                    4 , 0 , 1 , 1 , 1 , 1 , 0 , 4  ,
                    -5 , -10 , 0 , 0 , 0 , 0 , -10 , -5  ,
                    30 , -5 , 4 , 3 , 3 , 4 , -5 , 30   ]"""


    # Add or subtract the board position evaluation if there is a white or black tile there
    for index,score in enumerate(boardWeights):
        if board[index] == WHITE:
             curEval += score
        elif board[index] == BLACK:
             curEval -= score

    return curEval
        
    
    
# Function converting a decimal representation of the board state to the 0,1,2 ternary form used for processing
def toTernary(n):
    n = int(n) + LOOKUPSHIFT
    if n == 0:
        return 0
    else:
        result = ""
        while n > 0:
            n,remainder = divmod(n,3)
            result += str(remainder)
    return result[::-1].zfill(64)

# Function converting the ternary 0,1,2 representation of a board into decimal for storage
def toDecimal(n):
    n = str(n)[::-1]
    decimal = 0
    for power in range(64):
        decimal += int(n[power]) * (3**power)
    return decimal - LOOKUPSHIFT


# Procedure to close the file used for the transpositionTable once the program has finished to remove it from memory
def closeTable():
    global tranpositionTable
    transpositionTable.close()


# Helper function to return the number of white and black tiles respectively
def countTiles(board):
    return board.count(WHITE) , board.count(BLACK)


# Function to find an array of all the index locations of a piece of a certain colour
def findAllPieces(colour,board):
    locations = []
    for boardIndex in range(64):
        if board[boardIndex] == colour:
            locations.append(boardIndex)
    return locations



# Function to find all valid locations for the current player to play
def findAllValid(colour,locations,board):
    valid_locations = []
    for item in locations:
        for dx in range(-1,2):
            for dy in range(-1,2):
                if dx == 0 and dy == 0:
                    pass
                else:
                    valid, pos = checkValid(item,(dx,dy),colour,board)
                    if(valid):
                        valid_locations.append(pos)
    return valid_locations

# Recursive function to move in a direction checking if a move is going to be valid
def checkValid(location,direction,colour,board):
    # We are checking if the colour passed in is able to play
    # location is the current tile to be looked at
    # direction is a tuple (dx,dy)

    curX = (location%8) + direction[0]
    curY = (location//8) - direction[1]
    

    
    if (curX < 0) or (curX >= SIZE) or (curY < 0) or (curY >= SIZE):
        # If we are off the edge of the board, it is not valid
        return False, -1
    elif board[curY*8 + curX] == colour:
        # If we find a tile that is the same colour,
        # there is not going to be a valid move in this direction 
        return False, -1
    elif board[curY*8 + curX] == str(3-int(colour)):
        # If it is the opposite colour, there could be a valid move this way so recurse
        return checkValid((curX+curY*8),direction,colour,board)
    else:
        # If a blank tile is found
        if board[location] == str(3-int(colour)):
            # If the previous tile is the opposite colour, this is a valid location to play
            return True, curY*8+curX
        else:
            # If the previous tile is the same colour,
            # there have been no opposite colour tiles to flip so not valid
            return False, -1


# Function to iterate through all directions and check if they can be flipped
def flipAll(colour,location,board):
    board = board[:location] + colour + board[location+1:]
    for dx in range(-1,2):
        for dy in range(-1,2):
            if dx == 0 and dy == 0:
                pass
            else:
                # Call the recursive function flipIfValid in the direction specified
                temp, board = flipIfValid(location,(dx,dy),colour,board) 
    return board




def flipIfValid(location,direction,colour,board):
    
    curX = (location%8) + direction[0]
    curY = (location//8) - direction[1]

    
    if curX < 0 or curY < 0 or curX >= SIZE or curY >= SIZE:
        # If we are off the edge of the board, it is not valid
        return False, board
    elif board[curY*8 + curX] == '0':
        # If we find a blank tile, this direction is not valid
        return False, board
    elif board[curY*8 + curX] == colour:
        # If we find a tile that is the same as the tile we are checking,
        # this is a valid direction to flip so pass True back to the previous call
            
        return True, board
            
    else:
            
        # If the tile is the opposite colour,
        # call the subroutine on the next tile in this direction
        change, board = flipIfValid(curY*8+curX,direction,colour,board)
        # If the subroutine finds this is a valid direction, change will be True
        
        if change:
            # Change the board variable so that the current tile is flipped
            board = board[:curY*8 + curX] + colour + board[1+curY*8 + curX:]

        # Return whether we are changing and the new board version
        return change,board




# A version of the above flipAll function that is more efficient time wise
# This version is used in the review system by MiniMaxUnlimited()
def flipAll2(colour,location,board):
    # First place the piece in the location specified
    board = board[:location] + colour + board[location+1:]
    other = str(3-int(colour))
    for dx in range(-1,2):
        for dy in range(-8,9,8):
            if dx == 0 and dy == 0:
                pass
            else:
                cur = location+dx+dy
                new = cur+dx+dy
                try:
                    while board[cur] == other and 64>cur and cur>0:

                        if (cur % 8 == 0 and location % 8 != 0) or (cur % 8 == 7 and location % 8 != 7 ) or new > 63 or new < 0:
                            break
                        cur = new
                        new = cur+dx+dy
                
                    if board[cur] == colour and board[cur-dx-dy] == other:
                        # If we reach the same colour and the previous tile
                        # Is the opposite colour, valid direction
                        cur = location+dx+dy
                        # reset cur to the starting location
                        while cur != new:
                            # Iterate through every tile in this direction
                            # Flip the piece in each location
                            board = board[:cur] + colour + board[cur+1:]
                            cur = cur + dx + dy

                except:
                    # Except clause to more efficiently handle index errors that
                    # indicate the end of the board rather than repeated comparison operation
                    pass
    return board
    




def minimax(board, depth, maximisingPlayer,count,moveCount,alpha=float("-inf"),beta=float("inf"),table=[]):
    if count == 1:
        # Convert the board state to Decimal to optimise lookup
        decBoard = toDecimal(board)
        if decBoard in lut:
            #If the board is found in the lookup table, return the appropriate value
            return lut[decBoard][1],lut[decBoard][0]


    if depth == 0:
        # Base Case where the evaluation of the position is returned
        return evaluation(board)
    elif maximisingPlayer:
        # White is being checked
        val = float("-inf")

        # Find all valid moves for White
        locations = findAllPieces(WHITE,board)
        validPositions = findAllValid(WHITE,locations,board)
        validPositions = list(set(validPositions))
        
        if len(validPositions) == 0:
            # If there are no valid moves found for White, find all valid moves for black
            locations = findAllPieces(BLACK,board)
            validPositions = findAllValid(BLACK,locations,board)

            
            if len(validPositions)== 0:
                # If black also has no valid moves, someone has won so
                # count up the tiles to determine the winner and return the
                # appropriate value of + or - infinity
                white, black = countTiles(board)
                if white > black:
                    return float("inf")
                elif white < black:
                    return float("-inf")
                else:
                    # Return 0 if a draw is reached
                    return 0
            else:
                # Black has valid moves but White doesn't so skip White's turn
                # and call the algorithm for Black
                return minimax(board,depth,False,count+1,moveCount+1,alpha,beta)
            
        for pos in validPositions:

            # For every valid move White has, call the MiniMax algorithm recursively
            positionVal =  minimax(flipAll(WHITE,pos,board),depth-1,False,count+1,moveCount+1,alpha,beta)

            # If this current postion is the numerically best thus far, save the move and the evaluation
            if positionVal >= val:
                bestLocation = pos
                val = positionVal

            # Update the alpha value
            alpha = max(alpha,val)

            # Stop checking positions if Beta cutoff is reached
            if beta<= alpha:
                break

        # If this is the first layer of the call, return the evaluation of the board and
        # the best possible move in the situation, if not just return the evaluation
        if count == 1:
            # If there is only one valid move return that one
            if len(validPositions) == 1:
                return val, validPositions[0]

            # Write to the transposition table:
            # the state of the board, the best move and the corresponding evaluation
            towrite = str(toTernary(board))+" "+str(bestLocation)+" "+str(val)+" 1\n"
            transpositionTable.write(towrite)
            return val, bestLocation
        else:
            return val
    else:
        # Black is being checked
        # The samge system as White is being used but is mirrored to be applicable to Black
        val = float("inf")


        locations = findAllPieces(BLACK,board)
        validPositions = findAllValid(BLACK,locations,board)
        validPositions = list(set(validPositions))
        if len(validPositions) == 0:
            locations = findAllPieces(WHITE,board)
            validPositions = findAllValid(WHITE,locations,board)
            if len(validPositions)== 0:
                white, black = countTiles(board)
                if white > black:
                    return float("inf")
                elif white < black:
                    return float("-inf")
                else:
                    return 0
            else:
                return minimax(board,depth,True,count+1,moveCount+1,alpha,beta)
        for pos in validPositions:

            positionVal =  minimax(flipAll(BLACK,pos,board),depth-1,True,count+1,moveCount+1,alpha,beta)

            
            if positionVal <= val:

                bestLocation = pos
                val = positionVal
            beta = min(beta,val)
            if beta<= alpha:
                break
        
        if count == 1:
            if len(validPositions) == 1:
                
        
                return val, validPositions[0]
            towrite = str(toDecimal(board))+" "+str(bestLocation)+" "+str(val)+" 2\n"
            transpositionTable.write(towrite)
 
            return val, bestLocation
        else:
            return val


# A second minimax algorithm which is more optimised for deeper searches in the review system due to the faster flipAll procedure
def minimaxUnlimited(board, depth, maximisingPlayer,count,moveCount,alpha=float("-inf"),beta=float("inf"),table=[]):

    
    if depth <= 0 and maximisingPlayer:
        return evaluation(board)
    elif maximisingPlayer:
        #white
        val = float("-inf")

        locations = findAllPieces(WHITE,board)
        validPositions = findAllValid(WHITE,locations,board)
        if len(validPositions) == 0:
            locations = findAllPieces(BLACK,board)
            validPositions = findAllValid(BLACK,locations,board)
            if len(validPositions)== 0:
                white, black = countTiles(board)
                if white > black:
                    return float("inf")
                elif white < black:
                    return float("-inf")
                else:
                    return 0
            else:
                return minimaxUnlimited(board,depth,False,count+1,moveCount+1,alpha,beta,table)
            
        for pos in validPositions:
            positionVal =  minimaxUnlimited(flipAll2(WHITE,pos,board),depth-1,False,count+1,moveCount+1,alpha,beta,table)
            
            if positionVal >= val:
                
                bestLocation = pos
                val = positionVal
            alpha = max(alpha,val)
            if beta<= alpha:
                break
        
        if count == 1:
            if len(validPositions) == 1:
                return val, validPositions[0]
            return val, bestLocation
        else:
            return val
    else:
        val = float("inf")  
        try:
            index = boards.index(board)
            if count == 1:
                return scores[index], moves[index]
            else:
                return scores[index]
        except:
            pass
            
        locations = findAllPieces(BLACK,board)
        validPositions = findAllValid(BLACK,locations,board)
        if len(validPositions) == 0:
            locations = findAllPieces(WHITE,board)
            validPositions = findAllValid(WHITE,locations,board)
            if len(validPositions)== 0:
                white, black = countTiles(board)
                if white > black:
                    return float("inf")
                elif white < black:
                    return float("-inf")
                else:
                    return 0
            else:
                return minimaxUnlimited(board,depth,True,count+1,moveCount+1,alpha,beta,table)
        for pos in validPositions:
            positionVal =  minimaxUnlimited(flipAll2(BLACK,pos,board),depth-1,True,count+1,moveCount+1,alpha,beta,table)
            
            if positionVal <= val:

                bestLocation = pos
                val = positionVal
            beta = min(beta,val)
            if beta<= alpha:
                break
        
        if count == 1:
            if len(validPositions) == 1:
                return val, validPositions[0]
            return val, bestLocation
        else:
            return val

# The AI function for the Easy difficulty AI
# Plays the move that maximises the number of tiles flipped
def easyAI(board,curPlayer):
    # Find all valid moves
    locations = findAllPieces(curPlayer,board)
    validPositions = findAllValid(curPlayer,locations,board)

    # Create an empty array of integers to store tile counts
    tileCounts = [0] * len(validPositions)
    
    for index in range(len(validPositions)):
        # Iterates through every valid move and calculates
        # the number of tiles of each colour and stores
        # the difference (white-black) in the array
        white,black = countTiles(flipAll(curPlayer,validPositions[index],board))
        tileCounts[index] = white-black

    if curPlayer == WHITE:
        # If the AI is playing as white,
        # play the move that maximises the value of white-black
        return validPositions[tileCounts.index(max(tileCounts))] 
    else:
        # If the AI is playing as black,
        # play the move that minimises the value of white-black
        return validPositions[tileCounts.index(min(tileCounts))]





