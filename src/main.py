import cv2
import grid_recognizer as recognizer

reco = recognizer.Grid("grids/hashi1.png", 1000)
circles = reco.detect_circles()
if(circles): # Circle(s) have been detected
    for circle in reco.circles:
        print(str(circle))

#cv2.imshow("Base", reco.img)
#cv2.imshow("Without shadows", reco.no_shadow_img)d
#cv2.imshow("Binnary", reco.binary_img)
#cv2.imshow("Blurred", reco.blurred_img)
cv2.imshow("circles", reco.circles_img)



reco.crop_on_circles()

reco.set_circles_coordinates()


cv2.imshow("boxes", reco.boxes_img)

cv2.waitKey(0)       