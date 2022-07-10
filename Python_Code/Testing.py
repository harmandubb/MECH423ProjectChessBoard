import unittest 
from Chess import chess
from Camera import camera

class TestingSerialCommunication(unittest.TestCase): 

    def test_moveCalculation(self): 

        ch = chess()

        frame = "Fools_Mate\board1.jpg"

        corners, pieces = camera.getCornerAndPiecePlacement(frame)

        startBoardState = ch.getCurrentState(corners, pieces)

        ch.setBoardState(startBoardState)

        frame2 = "Fools_Mate\board2.jpg"

        corners, pieces = camera.getCornerAndPiecePlacement(frame2)

        curBoardState = ch.getCurrentState(corners, pieces)

        UARTCommands = ch.conductOpponentMove(curBoardState)

        actualCommands = [

        ]

        self.assertEqual(UARTCommands, actualCommands, "It should be 10")


if __name__ == '__main__':  
    unittest.main()  

