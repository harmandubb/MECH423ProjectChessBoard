import numpy as np 
# import cv2 as cv 
import glob
from Camera import camera
from skimage import io, data, filters
import matplotlib.pyplot as plt
from Chess import chess
from Website import chessAPI, BrowerControl

import time



if __name__=='__main__':
    winner = False #implement logic that switches the winner to be true and ending the loop
    chAPI = chessAPI()
    ch = chess()

    browerControl = BrowerControl()

    playerColor = chAPI.getPlayerColor()
    print(playerColor)

    ch.setBoardState(camera.getVisionBoard())

    print(ch.getBoardState())


    while(not winner):
        # Check what the current game conditions are 
        chAPI.requestGameInfo()

        #IF it is our turn
        if(playerColor == chAPI.getCurrentToMove()):
            #Actions to do if it is currently our turn to move
            #   - Need to check how the board has been changed from the opponent
            currentBoard = chAPI.getBoardState()
            print(currentBoard)
            #   - Figure out how the chess.com board has changed
            #   - Update the physcial board based on the update 
            ch.conductOpponentMove(currentBoard)
            #   -update the chessboard state in software
            ch.setBoardState(currentBoard)

            #   - Wait on the player to make a physcial chess board move. 
            #           -This is checked using a timer or using an interupt from the serial microcontroller
            #           - TODO: Figure out if a interupt can occur at this point. 

            # ch.waitForPlayerToMove() #This function waits for the micorporcessor to transmit a code show that the player has moved

            #For Testing Purposes 
            ch.waitForKeyStroke() 

            visionBoard = camera.getVisionBoard()

            print(visionBoard)
            # # The player has moved so now we need to convert the move into software code
            # camera.captureImage() 

            # #   - Use Computer vision to see what the chess board move is
            # frame = "CurrentBoard.jpg"
            # corners, pieces = camera.getCornerAndPiecePlacement(frame)
            # visionBoard = ch.getCurrentState(corners,pieces)

            # Determine the coordinates that would dictate how to move in selenium 
            coordinates = ch.getDiffCoordinates(visionBoard)

            origin = coordinates[0]
            dest = coordinates[1]
            #   - Once a change is detected on the board we need to update the chess board via selieum
            browerControl.inputMove(chAPI.gameURL, origin, dest)
            # once chess.com has been updated the locally stored chess setup can be updated

            ch.setBoardState(visionBoard)

        #If it is the other person's turn
        else: 
            #Action to do if we are not to move yet:
            #   - periodically check updated infromation
            sleeperTimer = 10*60 # minutes
            time.sleep(sleeperTimer)