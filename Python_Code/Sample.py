from Camera import camera
from Chess import chess

import matplotlib.pyplot as plt

import glob

if __name__ == "__main__":
    frames = glob.glob("Side_images/*.jpg")

    ch = chess()


    for frame in frames: 
        corners, pieces = camera.getCornerAndPiecePlacementOfSideBoard(frame, plots=False)
        # currentState = ch.getCurrentState(corners,pieces)
    
        # print(currentState)
    plt.show()
