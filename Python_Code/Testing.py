import unittest 
from Chess import chess
from Camera import camera

class TestingSerialCommunication(unittest.TestCase): 

    def test_calculateOpponentMove(self): 

        ch = chess()
        
        frame = "Fools_Mate/board1.jpg"

        corners, pieces = camera.getCornerAndPiecePlacement(frame)

        startBoardState = ch.getCurrentState(corners, pieces)

        ch.setBoardState(startBoardState)

        frame2 = "Fools_Mate/board2.jpg"

        corners, pieces = camera.getCornerAndPiecePlacement(frame2)

        curBoardState = ch.getCurrentState(corners, pieces)

        UARTCommands = ch.calculateOpponentMove(curBoardState)

        actualCommands = []

        # moving to pawn place
        actualCommands.extend(ch.moveToNECorner(False))
        for i in range(2):
            actualCommands.extend(ch.moveHalfToUP(False))
        for j in range(8):
            actualCommands.extend(ch.moveHalfToRight(False))
        actualCommands.extend(ch.moveToCenter(False))

        # moving pawn to new position 
        actualCommands.extend(ch.moveToNECorner(True))
        for i in range(2):
            actualCommands.extend(ch.moveHalfToUP(True))
        actualCommands.extend(ch.moveToCenter(True))

        
        # print("Actual Commands {}".format(actualCommands))
        # print("Actual Commands length: {}".format(len(actualCommands)))
        # print("UARTCommands -:{}".format(UARTCommands))
        # print("UARTCommands length: {}".format(len(UARTCommands)))


        self.assertEqual(UARTCommands, actualCommands, "It should be 10")


if __name__ == '__main__':  
    unittest.main()  

