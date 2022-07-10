from cv2 import threshold
import numpy as np 
import cv2 as cv 
import glob
from skimage import data, io, filters, color, feature, transform, measure, draw
from scipy import interpolate, ndimage
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans 
import sympy as sym
import math
import itertools

class camera: 
    # Class atributes 
    chessBoardSideLength = 44
    chessBoardSquares = 9

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
                if (abs(black_squares[i][j]) > 3.7):
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

    @classmethod 
    def edgeDetector(cls,gray, plots):
       

        blurred = filters.gaussian(gray, sigma=1)

        canny = feature.canny(blurred,  sigma=0.75)

        if (plots):
            plt.figure(1)
            plt.imshow(gray, cmap="gray")
            plt.title("Raw grayscale image")

            plt.figure(2)
            plt.imshow(blurred)
            plt.title("Gaussian blurred image")

            plt.figure(3)
            plt.imshow(canny)
            plt.title("Canny Edge Detection Output")


        return canny


    @classmethod 
    def cannyCorners(cls, canny, boardSquares, gray, plots):

        houghPeaks = 2*int((math.sqrt(boardSquares) )+1)

        if plots:

            print("Hough Peaks: {0}".format(houghPeaks))

            

            plt.figure(3)
            plt.imshow(canny)
            plt.title("Canny Edge detection")

        tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 360, endpoint=False)

        h, theta, d = transform.hough_line(canny, theta=tested_angles)


        if plots:

            plt.figure(4)
            plt.imshow(np.log(1+h), cmap="gray", aspect=1 / 10)
            plt.title("Hough space")
            plt.xlabel("Angles (degrees)")
            plt.ylabel('Distance (pixels)')

        acc, theta, d = transform.hough_line_peaks(h,theta,d, num_peaks=houghPeaks, min_distance=30, min_angle=1, threshold=10)

        if plots:
            plt.figure(5)
            plt.imshow(gray, cmap="gray")
            plt.title("Detected lines")

        vertical_lines = np.zeros(int(math.sqrt(boardSquares)+1))
        horizontal_lines = np.zeros(int(math.sqrt(boardSquares)+1))
        verticalLineCounter = 0
        horizontalLineCounter = 0

        for vote, angle, dist in zip(acc, theta, d):
            (x0,y0) = dist*np.array([np.cos(angle), np.sin(angle)])

            m = np.tan(angle+np.pi/2)

            if plots:
                print("Line Coordinates: ({0},{1})".format(x0,y0))
                print("Slope: {0}".format(m))

            if (((m < 1) and (m >= 0)) or ((m > -1) and (m <= 0))):
                m = 0
                horizontal_lines[horizontalLineCounter] = y0
                horizontalLineCounter = horizontalLineCounter + 1 
            elif ((m >50) or (m <-50)):
                m = 1e16 
                vertical_lines[verticalLineCounter] = x0
                verticalLineCounter = verticalLineCounter + 1
            if plots:
                plt.axline((x0,y0),slope=m) 

        if plots:
            print("Vertical Lines: {0}".format(vertical_lines))
            print("Horizontal Lines: {0}".format(horizontal_lines))

        # Begin to find the corners from the line intersections 
        corners = [(vertical,horizontal) for vertical,horizontal in itertools.product(vertical_lines,horizontal_lines)]
  
        return corners 

    @classmethod
    def threshold_hsv(cls, im_hsv, hlow, hhigh, slow, shigh, vlow, vhigh):
        im_hue = im_hsv[:,:,0]
        im_sat = im_hsv[:,:,1]
        im_val = im_hsv[:,:,2]

        h_mask = (im_hue >= hlow) & (im_hue <= hhigh)
        s_mask = (im_sat >= slow) & (im_sat <= shigh)
        v_mask = (im_val >= vlow) & (im_val <= vhigh)

        return h_mask & s_mask & v_mask

    @classmethod 
    def findBoard(cls,frame, gray):

        

        # plt.figure(1)
        # plt.imshow(frame)
        # plt.title("Raw image")

        # lower_test = 0.30
        # upper_test = 0.5

        # perimeter = (frame > lower_test) & (frame < upper_test)

        #Pink
        hlow = 0.85
        hhigh = 0.95
        slow = 0.55
        shigh = 1
        vlow = 0.35
        vhigh = 0.8

        # #green
        # hlow = 0.15
        # hhigh = 0.25
        # slow = 0.40
        # shigh = 1
        # vlow = 0.40
        # vhigh = 0.8

        hsv_image = color.rgb2hsv(frame)

        # print(hsv_image)

        perimeter = camera.threshold_hsv(hsv_image, hlow, hhigh, slow, shigh, vlow, vhigh)

    
        # plt.figure(2)
        # plt.imshow(perimeter)
        # plt.title("Threshold Mask")


        mask = np.logical_not(perimeter)

        # plt.figure(3)
        # plt.imshow(mask)
        # plt.title("Masked to be used in on frame")

        masked = np.copy(gray)

        masked[mask] = 0

        # plt.figure(4)
        # plt.imshow(masked, cmap="gray")
        # plt.title("Masked Image")

        contours = measure.find_contours(mask, fully_connected='high')

        # plt.figure(5)
        # plt.imshow(frame, cmap="gray")
        # plt.title("contours")

        max_area_index = 0
        max_area = 0
        index = 0

        for contour in contours: 
            contour_cv = np.expand_dims(contour.astype(np.float32), 1)
            contour_cv = cv.UMat(contour_cv)
            area = cv.contourArea(contour_cv)

            if max_area < area:
                max_area = area
                max_area_index = index

            index = index + 1   
            
        #     plt.plot(contour[:, 1], contour[:, 0], linewidth=2)


        # plt.figure(6)
        # plt.plot(contours[max_area_index][:, 1], contours[max_area_index][:, 0])
        # plt.title("Chessboard contour found")

        x = contours[max_area_index][:, 1]
        y = contours[max_area_index][:, 0]

        bottom_right = (x[np.argmax(x+y)],y[np.argmax(x+y)])
        bottom_left = (x[np.argmax(x-y)],y[np.argmax(x-y)])
        top_right = (x[np.argmin(x-y)],y[np.argmin(x-y)])
        top_left = (x[np.argmin(x+y)],y[np.argmin(x+y)])

        src_corners = np.array([top_left,
                                bottom_left,
                                bottom_right, 
                                top_right,
                                ])

        # plt.scatter(src_corners[:,0],src_corners[:,1], color="r")
        # plt.imshow(frame, cmap="gray")

        np.reshape(src_corners,(4,2))


        return src_corners


    @classmethod 
    def transformBoard(cls, frame, src_corners, plots):
        perimeter_thickness = 110

        width = 800
        height = 800 

        top_left = src_corners[0]
        bottom_right = src_corners[2]

        dst_corners = np.array([[0,0],
                                [width-1,0],
                                [width-1, height-1],
                                [0, height-1]
                                ])

        tform = transform.estimate_transform('projective',src_corners,dst_corners)

        tf_img_warp = transform.warp(frame, tform.inverse, mode='edge')



        cropped = tf_img_warp[perimeter_thickness:width-(perimeter_thickness), perimeter_thickness:height-(perimeter_thickness)]

        

        if plots:
            plt.figure(1)
            plt.imshow(frame, cmap="gray")
            plt.title("Gray Image")

            plt.figure(2)
            plt.imshow(tf_img_warp, cmap="gray")
            plt.title("Transformed chess board")

            plt.figure(3)
            plt.imshow(cropped,cmap="gray")
            plt.title("Cropped Imaged")


        return cropped

    
    @classmethod 
    def cleanupCorners(cls, frame, corners, plots):

        x = []
        y = []

        for coordinates in corners:
            x.append(coordinates[0])
            y.append(coordinates[1])

        if plots:
            plt.figure(1)
            plt.clf()
            plt.imshow(frame, cmap="gray")
            plt.title("Identified Corners")
            plt.scatter(x,y, c='r')

    @classmethod
    def identifyPieces(cls, frame, canny, num_pieces, plots=False):
        
        # Detect two radii
        smallBoardMax = 90
        smallBoardMin = 60 

        fullBoardMax = 30
        fullBoardMin = 15

        hough_radii = np.arange(fullBoardMin, fullBoardMax, 1)
        hough_res = transform.hough_circle(canny, hough_radii)

       


        # Select the most prominent 3 circles
        smallBoardMinDist = 120

        fullBoardMinDist = 50


        accums, cx, cy, radii = transform.hough_circle_peaks(hough_res, hough_radii, num_peaks= num_pieces - 1,
                                           total_num_peaks=num_pieces, min_xdistance=fullBoardMinDist, min_ydistance=fullBoardMinDist)

        fig, ax = plt.subplots(ncols=1, nrows=1)
        image = color.gray2rgb(frame)
        for center_y, center_x, radius in zip(cy, cx, radii):
            circy, circx = draw.circle_perimeter(center_y, center_x, radius)

            if plots:
                plt.scatter(circx,circy, c="r")

        if plots:
            ax.imshow(image)

        pieces = []

        for cord in zip(cx,cy):
            pieces.append(cord)

        if plots:

            plt.figure(1)
            plt.clf()
            plt.imshow(canny)
            plt.title("Canny Edge detection")

            print(type(hough_res))

            print(np.max(hough_res))

            plt.figure(2)
            plt.imshow(hough_res)
            plt.title("Circle Hough transform")

        return pieces

    @classmethod
    def getCornerAndPiecePlacement(cls,frame):
        gray = np.flip(io.imread(frame, as_gray=True),1)

        rgb_image = np.flip(io.imread(frame),1)

        src_corners = camera.findBoard(rgb_image, gray)

        cropped = camera.transformBoard(gray,src_corners, False)

        canny = camera.edgeDetector(cropped, False)

        corners = camera.cannyCorners(canny,64, cropped,False)

        camera.cleanupCorners(cropped, corners, False)

        #detect the pieces

        pieces = camera.identifyPieces(cropped, canny,32)


        return corners, pieces