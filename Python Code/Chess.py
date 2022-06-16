import numpy as np 
# import cv2 as cv 
import glob
from Camera import camera
from skimage import io, data, filters
import math
import matplotlib.pyplot as plt


class chess: 

    def __init__(self):
        self.chessBoardSquares = 9
        self.chessBoardSideSquares = int(math.sqrt(self.chessBoardSquares))
        
        #change chess board initialization for the full board implementation
        self.board = np.ones((self.chessBoardSideSquares, self.chessBoardSideSquares))


        