import mysql.connector
import base64
import datetime
LOOKUPSHIFT = 200156682785938776

pas = b'ZWxlbm5hMDY='
p = base64.b64decode(pas).decode("ascii")
# Open the connection to the SQL server
connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password=p,
  database="othello"
)



# Function to convert a board state that has been stored to the 0,1,2 - Blank,White,Black representation
def toTernary(n):
    n = int(n)
    n += LOOKUPSHIFT # Correct by the look up shift value
    if n == 0:
        return 0
    else:
        result = ""
        while n > 0:
            n,remainder = divmod(n,3)  
            result += str(remainder)
    # Pad the result with 0s to ensure the string is 64 characters long and follows the standard board format
    return result[::-1].zfill(64)  


# Function to convert a board state from the 0,1,2 representation to decimal
def toDecimal(n):
    n = str(n)[::-1]
    decimal = 0
    for power in range(64):
        decimal += int(n[power]) * (3**power)
    return decimal - LOOKUPSHIFT  # Shifts by the look up shift value to reduce storage size


# Takes in all the board states from a match and converts it into data to be stored in the table
def boardsToData(boards):
    data = ""
    for item in boards:
        data += str(toDecimal(item))
        data += 'n'
    return data

# Takes in the data from the table and converts it into all the board states for processing
def dataToBoards(data):
    boards = []
    #print(data)
    boards = data.split("n")
    boards.remove('')
    for index in range(len(boards)):
        
        boards[index] = str(toTernary(boards[index]))
    return boards

    
# Creates the SQL database
def create_database(connection,query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        #print("Database success")
    except Exception as e:
        print(e)


# Executes a generic SQL query passed to the function
def execute_query(connection,query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        #print("Query Success")
    except Exception as e:
        errorFile = open("errorLog.txt","w+")
        errorFile.write(e)
        errorFile.close()
        print(e)

# Exectures a SQL query which has a return value and returns that result
def execute_read_query(connection,query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        errorFile = open("errorLog.txt","w+")
        errorFile.write(e)
        errorFile.close()
        print(e)


# Gets relevant information from the table to display to the User a list of previous matches
def get_vals():
    query = """SELECT matchID,date,aiLevel,Result FROM matches"""
    result = execute_read_query(connection,query)
    return result


# Gets the match data for a match with a given key and returns the converted result
def get_data(key):
    query = """
    SELECT matchData
    FROM matches
    WHERE matchID = {matchKey}""".format(matchKey=key)
    result = execute_read_query(connection,query)[0][0]
                                                  
    result = dataToBoards(result)
    return result


# Converts the board states to data to be stored and stores it in the table
def insert_data(matchData, mode):
    lastBoard = matchData[-1]
    if lastBoard.count("2") != lastBoard.count("1"):
        winner = "Black" if lastBoard.count("2")>lastBoard.count("1") else "White"
    else:
        winner = "Draw"

    data = boardsToData(matchData)
    
    insert_vals = """
    INSERT INTO
        `matches` (`date`,`aiLevel`,`result`,`matchData`)
    VALUES
        ('{date}','{gameMode}','{win}','{matchInfo}');
        """.format(date=datetime.datetime.now().ctime(),gameMode=mode,win=winner,matchInfo=data)
    execute_query(connection,insert_vals)
    
create_database_query = "CREATE DATABASE IF NOT EXISTS othello"
create_database(connection,create_database_query)    # Creating the database if it does not already exist in the SQL

create_table = """
CREATE TABLE IF NOT EXISTS matches (
    matchID INT AUTO_INCREMENT,
    date TEXT,
    aiLevel TEXT,
    result TEXT,
    matchData TEXT,
    PRIMARY KEY (matchID)
) ENGINE = InnoDB
"""
execute_query(connection,create_table) # Creating the table if it does not already exist with matchID as the primary key






