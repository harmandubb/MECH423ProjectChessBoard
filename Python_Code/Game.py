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


    while(not winner):
        # if it is our turn
        if(playerColor == chAPI.getCurrentToMove()):
            #Actions to do if it is currently our turn to move
            #   - Need to check how the board has been changed from the opponent
            currentBoard = chAPI.getBoardState()
            #   - Figure out how the chess.com board has changed
            diffState = ch.compareBoardStates(currentBoard)
            #   - Update the physcial board based on the update 
            #   - TODO: Pull in the C# code to update the board 

            #   -update the chessboard state in software
            ch.setBoardState(currentBoard)

            #   - Wait on the player to make a physcial chess board move. 
            #           -This is checked by using the computer vision code or using an interupt from the serial microcontroller
            #           - TODO: Figure out if a interupt can occur at this point. 

            #   - Once a change is detected on the board we need to update the chess board via selieum
        
        #If it is the other person's turn
        else: 
            #Action to do if we are not to move yet:
            #   - periodically check updated infromation
            sleeperTimer = 10 # minutes
            time.sleep(sleeperTimer*60)

            chAPI.requestGameInfo()
            chAPI.findOpponentGame(gamesData)


    # Below is the vision testing code to be integrated

    # NUMSTARTPIECES = 32

    # frames = sorted(glob.glob('Fools_Mate/*.jpg'))

    # ch = chess(NUMSTARTPIECES)

    # turnCounter = 0


    # for frame in frames:
    #     #Debuggin be able to see what the algorthum is seeing
    #     currentState = ch.getBoardState


    #     gray = np.flip(io.imread(frame, as_gray=True),1)
    #     rgg_image = np.flip(io.imread(frame),1)

    #     src_corners = camera.findBoard(rgg_image, gray)

    #     cropped = camera.transformBoard(gray,src_corners, False)

    #     canny = camera.edgeDetector(cropped, False)

    #     corners = camera.cannyCorners(canny,64, cropped,False)

    #     camera.cleanupCorners(cropped, corners, False)

    #     #detect the pieces

    #     pieces = camera.identifyPieces(cropped, canny,32)

    #     currentPieces = len(pieces)

    #     currentState = ch.getCurrentState(corners, pieces)

    #     if (turnCounter > 0):

    #         diffState = ch.compareBoardStates(currentState)

    #         ch.convertStateToMove(diffState)

    #     ch.setBoardState(currentState)

    #     ch.stockfishMess()

    #     turnCounter = turnCounter + 1

    #     plt.show()
        