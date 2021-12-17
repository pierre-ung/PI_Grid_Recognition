import cv2
import numpy as np
from numpy.core.fromnumeric import mean
import hashi_circle as hc
import json
import hashitools as ht

class NoCircleException(Exception):
    pass

class UknwCircleCoordsException(Exception):
    def __init__(self, circle, message="The following circle coordinates cannot be determined. Could be because of a bad drawing."):
        self.circle = circle
        self.message = message + " " + str(self.circle)
        super().__init__(self.message)

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
        Crop the binary image to only keep circles inside the grid, set the instance top left / bottom right coordinates
"""
class Grid:
    def __init__(self, img, resize_width=800):
        # Grid images
        self.binary_img = None
        self.blurred_img = None
        self.no_shadow_img = None
        self.cropped_img = None
        self.boxes_img = None
        self.bot_right = None
        self.top_left = None

        # Game dimensions
        self.width = None
        self.height = None

        # Grid preparation 
        self.img = img
        self.__px_width = resize_width
        self.__prepare_image()
        self.circles_img = self.img.copy()
        self.circles = []

        # JSON structure
        self.json = None

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
        detected_circles = cv2.HoughCircles(self.blurred_img, cv2.HOUGH_GRADIENT, 1, minDist=minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
        # Add circles to the list of circles
        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))
            # Draw circles on the grid (optional)
            for i in detected_circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv2.circle(self.circles_img, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = i[2]
                cv2.circle(self.circles_img, center, radius, (255, 0, 255), 3)
            # Set the circle list
            for circle in detected_circles[0]:
                # Add circle to the circles list
                self.circles.append(hc.HashiCircle(circle[0], circle[1], circle[2], self.binary_img))
            
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
        self.top_left = (minX, minY)
        self.bot_right = (maxX, maxY)
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
        x_lines = [self.top_left[0]]
        y_lines = [self.top_left[1]]

        # Iteration counter
        it = 0
        # Set x lines coordinates
        line = x_lines[0]
        while(line+box_size < self.bot_right[0]):
            line = x_lines[it] + box_size
            right_border_coords = []
            left_border_coords = []
            for c in self.circles:
                if(c.is_betweenX(x_lines[it], x_lines[it] + box_size)):
                    right_border_coords.append(c.center_x + c.radius)
                    left_border_coords.append(c.center_x - c.radius)
            if len(right_border_coords) > 0:
                x_lines[it] = min(left_border_coords)
                line = max(right_border_coords)
            x_lines.append(line)
            it += 1
            
        # Iteration counter
        it = 0
        # Set y lines coordinates
        line = y_lines[0]
        while(line+box_size < self.bot_right[1]):
            line = y_lines[it] + box_size
            bot_border_coords = []
            top_border_coords = []
            for c in self.circles:
                if(c.is_betweenY(y_lines[it], y_lines[it] + box_size)):
                    bot_border_coords.append(c.center_y + c.radius)
                    top_border_coords.append(c.center_y - c.radius)
            if len(bot_border_coords) > 0:
                y_lines[it] = min(top_border_coords)
                line = max(bot_border_coords)
            y_lines.append(line)
            it += 1

        ## Draw boxes (optional)
        self.boxes_img = self.img.copy()
        for x in x_lines:
            start = (x, y_lines[0])
            stop = (x, y_lines[-1])
            cv2.line(self.boxes_img, start, stop, (255,0,0), 3)

        for y in y_lines:
            start = (x_lines[0], y)
            stop = (x_lines[-1], y)
            cv2.line(self.boxes_img, start, stop, (255,0,0), 3)
        
        ## Set circles positions
        positionsX = []
        positionsY = []
        for i in range(1, len(x_lines)):
            for j in range(1, len(y_lines)):
                for c in self.circles:
                    if c.is_between(x_lines[i-1], x_lines[i], y_lines[j-1], y_lines[j]):
                        c.position = (i-1, j-1) 
                        positionsX.append(i-1)
                        positionsY.append(j-1)
                        break
        
        ## Set game width / height
        self.width = max(max(positionsX), max(positionsY)) + 1
        self.height = self.width # We assume we only have square grids

        # Check if all circles have coordinates:
        for c in self.circles:
            if(c.position == (-1, -1)):
                raise(UknwCircleCoordsException(c))

    def generate_json(self):
        jsonG = {}
        jsonG["grid"] = {}
        jsonG["grid"]["dimensions"] = self.width
        jsonG["grid"]["circles"] = [None]*len(self.circles)
        for i in range(len(self.circles)):
            c = self.circles[i]
            jsonG["grid"]["circles"][i] = {}
            jsonG["grid"]["circles"][i]["circle"] = {}
            jsonG["grid"]["circles"][i]["circle"]["index"] = c.position[0] + c.position[1]*self.width
            jsonG["grid"]["circles"][i]["circle"]["img"] = ht.cv_to_b64_str(c.image)
        self.json = json.dumps(jsonG) 
        return self.json