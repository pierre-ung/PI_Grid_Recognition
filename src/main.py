import cv2
import grid_recognizer as recognizer
from flask import Flask, request
from flask_restful import Resource, Api, reqparse


# REST API
app = Flask(__name__)

#Add route
@app.route('/grid_pic', methods=['POST'])
def create_structure():
    photo = request.values['photo'] 
    print(photo)
    return 

#
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=50000)
#
#reco = recognizer.Grid("grids/hashi0.png", 800)
#circles = reco.detect_circles()
#
##cv2.imshow("Base", reco.img)
##cv2.imshow("Without shadows", reco.no_shadow_img)d
##cv2.imshow("Binnary", reco.binary_img)
##cv2.imshow("Blurred", reco.blurred_img)
##cv2.imshow("circles", reco.circles_img)
#
#try:
#    reco.set_circles_coordinates()
#except recognizer.UknwCircleCoordsException as e:
#    print(f"{e.circle} \n Coordinates cannot be determined")
#    exit()
#
#cv2.imshow("boxes", reco.boxes_img)
#cv2.waitKey(0)       
#
#if(circles): # Circle(s) have been detected
#    for circle in reco.circles:
#        cv2.imshow(f"{circle.position}", circle.image)
#        cv2.waitKey(0)
#
#