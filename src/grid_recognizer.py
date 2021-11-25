import cv2
import numpy as np
import hashi_circle as hc
"""
A class to recognize and store a grid structure (without digit recognition)

Attributes
----------

circles : HashiCircle
    A list of recognized circles in the grid

Methods
-------

    detect_circles : bool
        Compute detected circles in the instance circles list. 
        Returns true if cirlcles were detected, false otherwize

"""
class Grid:
    def __init__(self, grid_path, resize_width):
        self.__img = cv2.imread(grid_path)
        self.__px_width = resize_width
        self.__prepare_image()
        self.circles = []

    def __prepare_image(self):
        self.__img = cv2.resize(self.__img, (self.__px_width, self.__px_width))
        self.__binary_img = self.__compute_binary_img()
        self.__blurred_img = cv2.medianBlur(self.__binary_img, 5)
        

    def __compute_binary_img(self):
        # Get a grayscale copy of the image
        grayscale = cv2.cvtColor(self.__img, cv2.COLOR_BGR2GRAY)

        # Remove possible shadows from the grayscale image
        dilated_img = cv2.dilate(grayscale, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(grayscale, bg_img)
        
        # return the image with pixels set to black (0) or white (255) 
        return cv2.threshold(diff_img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

    def detect_circles(self, minDist = 50, param1 = 50, param2 = 20, minRadius = 20, maxRadius = 70):
        # Detect circles (center / radius)
        circles = cv2.HoughCircles(self.__blurred_img, cv2.HOUGH_GRADIENT, 1, minDist=minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
        # Add circles to the list of circles
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for circle in circles[0]:
                # Add circle to the circles list
                self.circles.append(hc.HashiCircle(circle[0], circle[1], circle[2]))
            return True
        return False    

