import cv2
import grid_recognizer as recognizer

reco = recognizer.Grid("grids/hashi5.png", 800)
circles = reco.detect_circles()

#cv2.imshow("Base", reco.img)
#cv2.imshow("Without shadows", reco.no_shadow_img)d
#cv2.imshow("Binnary", reco.binary_img)
#cv2.imshow("Blurred", reco.blurred_img)
cv2.imshow("circles", reco.circles_img)

reco.set_circles_coordinates()

if(circles): # Circle(s) have been detected
    for circle in reco.circles:
        print("---------------------")
        print(str(circle))
        print("---------------------")

cv2.imshow("boxes", reco.boxes_img)

cv2.waitKey(0)       