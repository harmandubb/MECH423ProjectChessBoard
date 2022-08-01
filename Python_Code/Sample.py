from Camera import camera
from Chess import chess

import matplotlib.pyplot as plt

import glob

if __name__ == "__main__":
    ch = chess()

    # camera.captureImage()

    frame = "CurrentBoard.jpg"
    corners, pieces = camera.getCornerAndPiecePlacement(frame)

    plt.show()
     
    

