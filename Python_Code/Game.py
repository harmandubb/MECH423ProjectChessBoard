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
            #   - Update the physcial board based on the update 
            diffState = ch.conductOpponentMove(currentBoard)
            #   -update the chessboard state in software
            ch.setBoardState(currentBoard)

            #   - Wait on the player to make a physcial chess board move. 
            #           -This is checked using a timer or using an interupt from the serial microcontroller
            #           - TODO: Figure out if a interupt can occur at this point. 

            # Take picture of the board 
            camera.captureImage() 

            #   - Use Computer vision to see what the chess board move is
            frame = "CurrentBoard.jpg"
            corners, pieces = camera.getCornerAndPiecePlacement(frame)
            visionBoard = ch.getCurrentState(corners,pieces)

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
            sleeperTimer = 10 # minutes
            time.sleep(sleeperTimer*60)

            chAPI.updateGame()


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
        