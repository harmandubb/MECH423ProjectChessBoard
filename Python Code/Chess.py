import numpy as np 
# import cv2 as cv 
import glob
from Camera import camera
from skimage import io, data, filters
import math
import matplotlib.pyplot as plt


class chess: 
    chessBoardSquares = 9
    chessBoardSideSquares = int(math.sqrt(chessBoardSquares))
    numPiecesPresent = 9

    def __init__(self):
        self.chessBoardSquares = 9
        self.numPiecesPresent  = 9
        self.chessBoardSideSquares = int(math.sqrt(self.chessBoardSquares))
        
        #change chess board initialization for the full board implementation
        self.board = np.ones((self.chessBoardSideSquares, self.chessBoardSideSquares))

    def getCurrentState(self, corners, pieces):
        #Sorting corner points known order

        currentBoard = np.zeros([self.chessBoardSideSquares, self.chessBoardSideSquares])

        
        corners.sort(key=lambda k: [k[1], k[0]])
        pieces.sort(key=lambda k: [k[1], k[0]])

        copy_pieces = pieces

        print("Corners: {0}".format(corners))
        print("Pieces:{0}".format(pieces))

        identifiedPieces = 0
        row = 0
        col = 0


        for i in range(self.chessBoardSquares):
            if(i%self.chessBoardSideSquares == 0 and i != 0):
                row = row + 1
                col = 0

            upperLeft = corners[i+row]
            print("First Index: {0}".format(i+row))
            lowerRight = corners[i+self.chessBoardSideSquares + 2+row] 
            print("Secound Index: {0}".format(i+self.chessBoardSideSquares + 2+row))

            print("Upper left: {0}".format(upperLeft))
            print("Lower reft: {0}".format(lowerRight))

            for piece in copy_pieces:
                x = piece[0]
                y = piece[1]

                print("PieceCoordinates {0}, {1}".format(x,y))
                if(upperLeft[0] <= x <= lowerRight[0]):
                    if(upperLeft[1] <= y <= lowerRight[1]):
                        
                        identifiedPieces = identifiedPieces + 1
                        print("Piece is present {0}".format(identifiedPieces))

                        currentBoard[row][col] = 1

                        copy_pieces.remove(piece)
                        break

            col = col + 1 


            
            # print("Current Pieces: {0}".format(currentPiece))

        return currentBoard


        