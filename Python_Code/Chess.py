import time
import numpy as np 
from enum import Enum
import math

import glob
from Camera import camera
from skimage import io, data, filters
import matplotlib.pyplot as plt


import serial 
import serial.tools.list_ports


class Direction(Enum):
    UP = 51
    RIGHT = 48 
    DOWN = 49
    LEFT = 50  

class chess: 
    chessBoardSquares = 8*8
    chessBoardSideSquares = int(math.sqrt(chessBoardSquares))
    numPiecesPresent = 4*8

    def __init__(self, numPieces=32, chessBoardSquares=64, baudrate=9600):

        #Board Parameters
        self.chessBoardSquares = chessBoardSquares
        self.numPiecesPresent  = numPieces
        self.chessBoardSideSquares = int(math.sqrt(self.chessBoardSquares))
        #change chess board initialization for the full board implementation
        self.board = np.zeros((self.chessBoardSideSquares, self.chessBoardSideSquares))

        # Solenoid 
        self.solenoidLocation = (0,0)

        # ChessIO
        self.ser = serial.Serial()
        self.ser.baudrate = baudrate

        ports = serial.tools.list_ports.comports()

        for port, desc, hwid in ports: 
            # print(port)
            # print(desc)
            if ("MSP430" in desc):
                self.ser.port = port
                print("MSP430 is on COMport {}".format(self.ser.port))

        self.aAsciValue = (97).to_bytes(2,'big')

        self.ser.open()
        
        self.ser.write(str.encode("READY"))

        self.ser.close()

    def getCurrentState(self, corners, pieces):
        #Sorting corner points known order

        currentBoard = np.zeros([self.chessBoardSideSquares, self.chessBoardSideSquares])

        corners.sort(key=lambda k: [k[1], k[0]])
        pieces.sort(key=lambda k: [k[1], k[0]])

        copy_pieces = pieces

        # print("Corners: {0}".format(corners))
        # print("Pieces:{0}".format(pieces))

        identifiedPieces = 0
        row = 0
        col = 0

        for i in range(self.chessBoardSquares):
            if(i%self.chessBoardSideSquares == 0 and i != 0):
                row = row + 1
                col = 0

            upperLeft = corners[i+row]
            # print("First Index: {0}".format(i+row))
            # print("Secound Index: {0}".format(i+self.chessBoardSideSquares + 2+row))
            lowerRight = corners[i+self.chessBoardSideSquares + 2+row] 
        
            # print("Upper left: {0}".format(upperLeft))
            # print("Lower reft: {0}".format(lowerRight))

            for piece in copy_pieces:
                x = piece[0]
                y = piece[1]

                # print("PieceCoordinates {0}, {1}".format(x,y))
                if(upperLeft[0] <= x <= lowerRight[0]):
                    if(upperLeft[1] <= y <= lowerRight[1]):
                        
                        identifiedPieces = identifiedPieces + 1
                        # print("Piece is present {0}".format(identifiedPieces))

                        currentBoard[row][col] = 1

                        copy_pieces.remove(piece)
                        break

            col = col + 1 

        return currentBoard

    def setBoardState(self,curBoard):
        self.board = curBoard

    def getBoardState(self):
        return self.board

    def getDiffBoardState(self, currentBoardState):
        diffState = currentBoardState - self.board

        print(diffState)

        return diffState

    def convertDiffStateToCoordinates(self, diffState):
        origin = np.where(diffState == -1)
        dest = np.where(diffState == 1)

        coordinates = [origin, dest]

        return coordinates

    def convertStateToMove(self, diffState):
        origin = np.where(diffState == -1)
        dest = np.where(diffState == 1)

        chessNotationOrigin = str(chr(ord("a") + origin[1][0])) + str(self.chessBoardSideSquares - origin[0][0])

        chessNotationDest = str(chr(ord("a") + dest[1][0])) + str(self.chessBoardSideSquares - dest[0][0])

        # print("origin: {}".format(chessNotationOrigin))

        # print("Destination: {}".format(chessNotationDest))

        move = (chessNotationOrigin, chessNotationDest)

        return move

    def piecePresent(self, location):
        if(self.board(location) == 1):
            present = True
        else:
            presnet = False
        
        return present

    # ---------------------------Solenoid----------------------------    

    def setSolenoidLocation(self, newLocation) -> None:
        self.solenoidLocation = newLocation
    
    def getSolenoidLocation(self):
        return self.solenoidLocation

    # ---------------------------CHESSIO----------------------------
    def getRelativeCoordinates(self, origin, dest):
        relativeCoordinates = (dest[1] - origin[1], dest[0] - origin[0])

        return relativeCoordinates

    def conductOpponentMove(self, opponentMoveBoard):
        diffState = self.getDiffBoardState(opponentMoveBoard)
        coordinates = self.convertDiffStateToCoordinates(diffState)
        UARTCommands = self.moveCalculation(coordinates[0], coordinates[1])
        self.sendMovementCommands(UARTCommands)


    def moveToNECorner(self, solenoidOn):
        commands = [
            bytearray([self.aAsciValue, solenoidOn.to_bytes(2,'big'), Direction.UP.to_bytes(2,'big')]),
            bytearray([self.aAsciValue, solenoidOn.to_bytes(2,'big'), Direction.RIGHT.to_bytes(2,'big')])
        ]

        return commands
    
    def moveToCenter(self, solenoidOn):
        commands = [
            bytearray([self.aAsciValue, solenoidOn.to_bytes(2,'big'), Direction.DOWN.to_bytes(2,'big')]),
            bytearray([self.aAsciValue, solenoidOn.to_bytes(2,'big'), Direction.LEFT.to_bytes(2,'big')])
        ]

        return commands

    def moveHalfToLeft(self,solenoidOn):
        commands = [
            bytearray([self.aAsciValue, solenoidOn.to_bytes(2,'big'), Direction.LEFT.to_bytes(2,'big')]),
        ]

        return commands

    def moveHalfToRight(self,solenoidOn):
        commands = [
            bytearray([self.aAsciValue, solenoidOn.to_bytes(2,'big'), Direction.RIGHT.to_bytes(2,'big')]),
        ]

        return commands

    def moveHalfToUP(self,solenoidOn):
        commands = [
            bytearray([self.aAsciValue, solenoidOn.to_bytes(2,'big'), Direction.UP.to_bytes(2,'big')]),
        ]

        return commands

    def moveHalfToDown(self,solenoidOn):
        commands = [
            bytearray([self.aAsciValue, solenoidOn.to_bytes(2,'big'), Direction.DOWN.to_bytes(2,'big')]),
        ]

        return commands

    def moveCalculation(self,origin, dest):
        UARTCommands = []
        solenoidOn = True

        # Determine if we need to move a piece out of the way
        if(chess.isPiecePresent(dest)):
            solenoidOn = False
            # eliminate the piece at the destination
            UARTCommands.extend(self.moveToNECorner(solenoidOn))
            UARTCommands.extend(self.moveToDestination(solenoidOn, dest))
            UARTCommands.extend(self.moveToCenter(solenoidOn))

            self.setSolenoidLocation(dest)

            # eliminate the piece
            solenoidOn = True
            UARTCommands.extend(self.moveToNECorner(solenoidOn))
            UARTCommands.extend(self.pieceElimination(dest))   #add the code to move to the edge of the board

            solenoidOn = False

            UARTCommands.extend(self.moveToCenter(solenoidOn))

            
            # Update the solenoid location 
            self.setSolenoidLocation((dest[0], 0)) #Can make this dropping of the piece more smarter once the initial system is made better

        # need to move solenoid to origin location 

        solenoidOn = False

        UARTCommands.extend(self.moveToNECorner(solenoidOn))
        UARTCommands.extend(self.moveToDestination(solenoidOn,origin))
        UARTCommands.extend(self.moveToCenter(solenoidOn))

        self.setSolenoidLocation(origin)

        # Conduct the player's move 
        solenoidOn = True 
        moveRelativeCoordinate = self.getRelativeCoordinates(self.getSolenoidLocation(),dest)
        UARTCommands.extend(self.moveToNECorner(solenoidOn))
        UARTCommands.extend(self.moveToDestination(solenoidOn,dest))
        UARTCommands.extend(self.moveToCenter(solenoidOn))

        #setting solenoid location 
        self.setSolenoidLocation(dest)

        solenoidOn = False

        return UARTCommands

    def moveToDestination(self, solenoidOn, dest):
        relativeDestCoordinates = self.getRelativeCoordinates(self.getSolenoidLocation, dest)

        commands = []

        if (relativeDestCoordinates[1] > 0):
            UPDOWN = Direction.UP
        else:
            UPDOWN = Direction.DOWN

        if(relativeDestCoordinates[0] > 0):
            RIGHTLEFT = Direction.RIGHT
        else:
            RIGHTLEFT = Direction.LEFT

        # move up and down first 
        for i in range(math.abs(relativeDestCoordinates[1])):
            # need two half steps to move one square
            for j in range(2):
                temp = bytearray([self.aAsciValue, solenoidOn.to_byte(2,'big'), UPDOWN.to_byte(2,'big')])
                commands.extend(temp) 

        # move left and right
        for i in range(math.abs(relativeDestCoordinates[0])):
            # need two half steps to move one square
            temp = bytearray([self.aAsciValue, solenoidOn.to_byte(2,"big"), RIGHTLEFT.to_byte(2,"big")])
            commands.extend(temp)


        return commands

    def pieceElimination(self,pieceLocation):
        # creating a simple eliminatino algorithum that jsut tosses pieces to the left side of the board: 
        # algorithum assumes the piece is already on the NE corner of a square

        # move to the square that is on the edge of the board
        solenoidOn = True
        edgeOfBoard = pieceLocation()
        edgeOfBoard[1] = 0  #this takes us to the NE edge of the square

        commands = []

        commands.extend(self.moveToDestination(solenoidOn, edgeOfBoard))

        # need to move the appropiate amount off the board
        # If on the left you would need to move I square over to the left
        for i in range(3):
            commands.extend(self.moveHalfToLeft(solenoidOn))

        #turn off the solenoid to come back to the board
        solenoidOn = False
        for i in range(3):
            commands.extend(self.moveHalfToRight(solenoidOn))
        
        #this bring us back to the NE of the edge square

        #leave the implementation to center the solenoid to the main code

    def sendMovementCommands(self, UARTCommands):
        sleepTimer = 1 #sec

        while(len(UARTCommands) > 0):
            if(not self.ser.is_open()):
                self.ser.open()

            byte = UARTCommands.pop(0)

            print(byte)
            self.ser.write(byte)

            time.sleep(sleepTimer)
        
        self.ser.close()

    def move(self, ):
        self.moveCalculatoin()
            
ch = chess()