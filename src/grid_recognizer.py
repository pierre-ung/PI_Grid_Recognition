import cv2
import numpy as np
from numpy.core.fromnumeric import mean
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

    crop_circle : cv2 image
        Crop the binary image to only keep circles inside the grid
"""
class Grid:
    def __init__(self, grid_path, resize_width):
        self.binary_img = None
        self.blurred_img = None
        self.no_shadow_img = None
        self.cropped_img = None
        self.boxes_img = None

        self.img = cv2.imread(grid_path)
        self.__px_width = resize_width
        self.__prepare_image()
        self.circles_img = self.img.copy()
        self.circles = []

    def __prepare_image(self):
        self.img = cv2.resize(self.img, (self.__px_width, self.__px_width))
        self.binary_img = self.__compute_binary_img()
        self.blurred_img = cv2.medianBlur(self.binary_img, 1)
        

    def __compute_binary_img(self):
        # Get a grayscale copy of the image
        grayscale = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        # Remove possible shadows from the grayscale image
        dilated_img = cv2.dilate(grayscale, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(grayscale, bg_img)
        self.no_shadow_img = diff_img
        # return the image with pixels set to black (0) or white (255) 
        return cv2.threshold(diff_img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

    def detect_circles(self, minDist = 50, param1 = 50, param2 = 20, minRadius = 20, maxRadius = 70):
        # Empty circles list
        self.circles = []
        # Detect circles (center / radius)
        circles = cv2.HoughCircles(self.blurred_img, cv2.HOUGH_GRADIENT, 1, minDist=minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
        # Add circles to the list of circles
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv2.circle(self.circles_img, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = i[2]
                cv2.circle(self.circles_img, center, radius, (255, 0, 255), 3)
            for circle in circles[0]:
                # Add circle to the circles list
                self.circles.append(hc.HashiCircle(circle[0], circle[1], circle[2]))
            return True
        return False    


    def crop_on_circles(self):
        minX = self.img.shape[0]
        minY = self.img.shape[1]
        maxX = 0
        maxY = 0
        for c in self.circles:
            xmin = c.center_x - c.radius
            ymin = c.center_y - c.radius
            xmax = c.center_x + c.radius
            ymax = c.center_y + c.radius
            if xmin < minX:
                minX = xmin
            if ymin < minY:
                minY = ymin
            if xmax > maxX:
                maxX = xmax
            if ymax > maxY:
                maxY = ymax
        self.cropped_img = self.binary_img[minY:maxY, minX:maxX]
        return self.cropped_img
        
    def get_mean_circles_diameter(self):
        sumc = 0
        for c in self.circles:
            sumc += c.radius*2
        return sumc / len(self.circles)
    
    def set_circles_coordinates(self):
        if(self.cropped_img is None):
            self.crop_on_circles()            
        box_size = int(self.get_mean_circles_diameter())
        x_lines = []
        y_lines = []

        # Set x lines coordinates
        for i in range (0, self.cropped_img.shape[0], box_size+9):
            x_lines.append(i)

        # Set y lines coordinates
        for i in range (0, self.cropped_img.shape[1], box_size):
            y_lines.append(i)

        print(x_lines)
        print(self.cropped_img.shape[0])
        print(box_size)
        
        # Draw boxes
        self.boxes_img = self.cropped_img.copy()
        # Draw columns
        for i in x_lines:
            start = (0, i)
            stop = (self.boxes_img.shape[1], i)
            cv2.line(self.boxes_img, start, stop, (0,0,0), 1)