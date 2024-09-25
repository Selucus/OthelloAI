import OthelloDatabase as DB
from bardapi import Bard
import os
import time


def main():
    
    options = [str(x) for x in range(1,5)]
    answer = 0
    
    # Get a valid choice for the user decision on which functionality to use.
    while answer not in options:
        if answer == 0:
            print("Welcome to the Othello AI. Please decide on what you wish to do.\n1: Play against the AI\n2: Review a past match\n3: Play against another player\n4: Information about the AI")
        else:
            print("Not a valid selection. Please choose a valid choice or type 0 to see your options again")
        
        answer = input()
            

    
    if answer == "1": # Play Othello against AI
        import OthelloAI   # Load Othello game against AI
        summary = OthelloAI.summary()
        DB.insert_data(summary[0],summary[1]) # Insert the match data into the database
        
    elif answer == "2": # Review a past match
        pastMatches = DB.get_vals() # Fetch past matches from the database
        matchKeys = []
        for item in pastMatches:
            print(item) # Display match details to the user
            matchKeys.append(str(item[0]))    # Display to the user all the possible past matches
        
        key = -1
        print("Enter the key of the match you want to review")
        key = input()
        while key not in matchKeys:    # Get a valid matchKey from the user
            print("Does not exist")
            key = input()

        matchData = DB.get_data(key)   # Retrieve the matchdata of the match chosen
        import OthelloReview    # Load the review system
        OthelloReview.review(matchData)    # Pass the matchdata to the review system
        
        
        
    elif answer == "3": # Play against another Player
        import OthelloPVP # Load Othello game against another player locally
        summary = OthelloPVP.summary()
        DB.insert_data(summary[0],summary[1]) # Insert the match data into the database
    elif answer == "4": # Information about the AI

        print("""This AI works using an algorithm called MiniMax.\n
This means that the algorithm assumes that you are a perfect player and will try to
minimise the maximum score you can get in any position.\n
It calculates a numerical score to show who has the advantage with a positive number meaning
a white advantage and negative meaning black advantage.\n
The bigger the number, the bigger the advantage.\n
If you have any further questions, you can ask the ChatBot Assistant, would you like to do this?""")
        askAI = input("y/n\n")
        if askAI == "y":
            setupMessage = """You are now a chatbot being used within a python program.
This program is a recreation of the board game Othello and uses an AI that uses the MiniMax algorithm.
Your role is to answer any questions from the user about the rules of the game or about how the AI system for the game works.
All your responses must be within this context."""

            # Setup the API for communication using the API key
            bard = Bard(token='ABTWhQFF04Ke1XokYQhDzo-Odg_QDKVir1FMsfChLh8oHA8eWD9gkGg_cR2lTLho-Dl4KsDQ.')

            # Send the LLM a message detailing the environment it is being used in to help it respond appropriately
            temp = bard.get_answer(setupMessage) 
            print(temp['content'])
            message = input("Please enter your question or type \'exit\' to quit\n")
            while message != "exit":
                if message:
                    try:
                        time.sleep(2.2)
                        # Make an API call to the BardAPI using the message to customise the response
                        response = bard.get_answer(message) 
                        print(response["content"])
                        
                    except Exception as e: # If an error occurs, write the error details to a log file
                        print("Unfortunately the ChatBot Assistant is not currently active, sorry for the inconvenience")
                        errorFile = open("errorLog.txt","w+")
                        errorFile.write(e)
                        errorFile.close()
                        break
                message = input("")
                    

                    
    
    print("Would you like to play again? (y)")
    response = input()
    if response == "y" or response == "Y":
        main()
    else:
        print("Thank you for playing")
    
main()
