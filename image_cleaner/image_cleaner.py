import cv2
import numpy as np

src = cv2.imread("Grids/hashi4.png")
image = cv2.resize(src, (784,784))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.medianBlur(gray, 5)

minDist = 50
param1 = 50
param2 = 20
minRadius = 20
maxRadius = 70

circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, minDist=minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        center = (i[0], i[1])
        # circle center
        cv2.circle(image, center, 1, (0, 100, 100), 3)
        # circle outline
        radius = i[2]
        cv2.circle(image, center, radius, (255, 0, 255), 3)

cv2.imshow("Detected Circles", image)
cv2.waitKey(0)