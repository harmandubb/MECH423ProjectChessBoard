import numpy as np 
from cv2 import cv2 as cv 
import glob
from Camera import camera


if __name__=='__main__':

    mtx, dist = camera.cameraCalibration()

    frames = glob.glob('Test_Images/greenphysicaltest8.jpg')

    for frame in frames:
        frame = cv.imread(frame)
        #dst = camera.undistortFrame(frame,mtx,dist)
        #corners = camera.chessboardCornerDetection(dst)
        corners = camera.chessboardCornerDetection(frame)



# # cap = cv.VideoCapture(0)
# # if not cap.isOpened():
# #     print("Cannot open camera")
# #     exit()


# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     # if frame is read correctly ret is True
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break

#     # Our operations on the frame come here
#     gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

#     chessboardCornerDetection(frame)
#     # Display the resulting frame
#     cv.imshow('frame', frame)
#     if cv.waitKey(1) == ord('q'):
#         break

# # When everything done, release the capture
# cap.release()
# cv.destroyAllWindows()


    