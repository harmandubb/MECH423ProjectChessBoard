from Camera import camera
from Chess import chess

import matplotlib.pyplot as plt

import glob

if __name__ == "__main__":
    ch = chess()

    # camera.captureImage()

    frame = "CurrentBoard.jpg"
    visionBoard = camera.getVisionBoard(frame)

    print(visionBoard)

    plt.show()
     
    

