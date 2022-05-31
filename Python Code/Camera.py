import numpy as np 
import cv2 as cv 
import glob
from skimage import data, io, filters, color
from scipy import interpolate, ndimage
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans 

class camera: 
    # Class atributes 
    chessBoardSideLength = 44

    def __init__(self):
        pass 

    @classmethod
    def cameraCalibration(cls):
        r"""Finds the intrinsic camera parameters and distortion coefficients of the camera and saves it to a .npz file called Camera parameters.npz

        Find the intrinic camera parameters and the disotrition coefficient of the camera with preloaded images of a chess board. 

        Returns
        -------
        mtx : ndarray
            matrix holding instrinsic camera parameters
        dist : array
            array holding distorition coefficients

        Notes
        -----
        The camera calibration uses open cv functions for the calibration. 

        """
        # frameSize = (1920,1080)
        chessboardSize = (7,7)
        # termination criteria
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((chessboardSize[0]*chessboardSize[1],3), np.float32)
        objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)*camera.chessBoardSideLength #44 mm is the sidelength of squares
        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.
        images = glob.glob('Calibration_Images/*.jpg')

        for fname in images:
            img = cv.imread(fname)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv.findChessboardCornersSB(gray, chessboardSize, None)
            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
                corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
                imgpoints.append(corners)
                # Draw and display the corners
                cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
                #cv.imshow('img', img)
                #imS = cv.resize(img, (960, 540))  
                #cv.imshow('img', img)
                #cv.waitKey(10)

        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        np.savez("Camera_parameters", mtx=mtx,dist=dist)

        return mtx, dist
        
    @classmethod    
    def loadCameraParameters(cls):
        r"""Loads camera parameters including instrinic parameters and distortion coeffieicents 

        The system will try to access a camera parameter file that is created by the camera calibration function. 
        The camera parameters that are loaded are the instrinict parameters and the distortion coefficients

        Returns
        -------
        mtx : ndarray
            matrix holding instrinsic camera parameters
        dist : array
            array holding distorition coefficients

        Other Parameters
        ----------------
        only_seldom_used_keyword : int, optional
            Infrequently used parameters can be described under this optional
            section to prevent cluttering the Parameters section.
        **kwargs : dict
            Other infrequently used keyword arguments. Note that all keyword
            arguments appearing after the first parameter specified under the
            Other Parameters section, should also be described under this
            section.

        Raises
        ------
        FileNotFoundError
            Camera calibration file is not found in the immediate directory.
        """

        try: 
            npzfile = np.load("Camera_parameters.npz")

            mtx = npzfile(['mtx'])
            dist = npzfile(['dist'])

            return mtx, dist

        except (FileNotFoundError):
            print("File is not present in immediate directory")
            
    @classmethod
    def undistortFrame(cls,frame,mtx,dist):         
        h,  w = frame.shape[:2]

        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

        # undistort
        dst = cv.undistort(frame, mtx, dist, None, newcameramtx)

        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]

        return dst

    
        
    @classmethod
    def thresholdCorners(cls, frame):
        lower_color_bounds = (0,0,0)
        upper_color_bounds = (50,50,50)

        mask = cv.inRange(frame,lower_color_bounds,upper_color_bounds)
        
        rough_image = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)

        cv.imshow("rough_image", rough_image)

        blur_image = cv.medianBlur(rough_image, 5)

        cv.imshow("blur_image", blur_image)


        return mask


    @classmethod
    def chessboardCornerDetection(cls,frame):
        scale = 3
        frame = cv.resize(frame, (0,0), fx = scale, fy = scale)
        numCorners = 16
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        mask = camera.thresholdCorners(frame)

        corners = cv.goodFeaturesToTrack(mask,numCorners, 0.001, 300)
        corners = np.int0(corners)

        for corner in corners:
            x,y = corner.ravel()
            cv.circle(frame, (x,y),25, (0,0,255), -1)


        cv.imshow('Corners', frame)
        cv.waitKey()

        return corners

    @classmethod
    def kernelCorners(cls, gray):
        num_corners = 16

        scaled = np.zeros(gray.shape)

        for i in range (gray.shape[0]):
            for j in range (gray.shape[1]):
                scaled[i,j] = np.interp(gray[i,j],[0,1], [-1,1])

        #kernels are described with the square color on the top left 
        white_kernel = np.ones((7,7))
        white_kernel[0:4,4:7] = -1
        white_kernel[4:7,0:4] = -1

        black_kernel = -1*np.ones((7,7))
        black_kernel[0:4,4:7] = 1
        black_kernel[4:7,0:4] = 1

        black_squares = convolve2d(scaled,black_kernel, mode='same')
        white_squares = convolve2d(scaled,white_kernel, mode='same')
        
        plt.figure(2)
        plt.imshow(black_squares, cmap='gray')
        plt.title("Black Kernel mapped")

        #cluster to isolate one point to be taken as a corner 
        corner_intensity = np.zeros(black_squares.shape)

        for i in range(black_squares.shape[0]):
            for j in range(black_squares.shape[1]):
                if (abs(black_squares[i][j]) > 3.4):
                    corner_intensity[i][j] = black_squares[i][j]

        plt.figure(4)
        plt.imshow(corner_intensity)
        plt.title("Corner Intensity")


        corner_points = np.argwhere(corner_intensity)

        plt.figure(7)
        plt.scatter(corner_points[:,1], corner_points[:,0])
        plt.title("conerpoints visulization")
        
        Kmean = KMeans(n_clusters=num_corners).fit(corner_points)


        plt.figure(5)
        plt.scatter(corner_points[:,1], corner_points[:,0], c=Kmean.labels_)
        print(Kmean.cluster_centers_)
        plt.title("Visualization of clustering")

        plt.figure(6)
        plt.imshow(gray)
        plt.scatter(Kmean.cluster_centers_[:,1], Kmean.cluster_centers_[:,0], c='red')
        
        plt.show()
       


        
