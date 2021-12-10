import cv2
import base64
import numpy as np
import grid_recognizer as recognizer
from flask import Flask, request, abort, jsonify
from werkzeug.exceptions import HTTPException
from flask_restful import Resource, Api, reqparse

'''
Convert a base64 image to a cv2 image
@param b64 : str
    The base64 str to decode
@return The cv2 image corresponding 
'''
def b64_to_cv(b64):
    im_bytes = base64.b64decode(b64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img


########## REST API ##########
app = Flask(__name__)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500 #HTTP error code for bad precondition 
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(code=code, error=str(e)), code


'''
Main API route
Returns a JSON describing the grid 
'''
@app.route('/grid_pic', methods=['POST'])
def create_structure():
    # Decode the base64 img (-> cv2 image)
    b64 = request.values['photo_b64'] 
    img = b64_to_cv(b64)
    
    # Recognizer
    ## Creation
    reco = recognizer.Grid(img, 800)
    ## Circle detection
    circles = reco.detect_circles()
    ## Set circle game coordinates
    try:
        reco.set_circles_coordinates()
    except recognizer.UknwCircleCoordsException as e:
        ### Return error code in case of failure
        abort(412, e)
    

    return reco.json



###########################################
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=50000)

###########################################
#
#reco = recognizer.Grid("grids/hashi0.png", 800)
#circles = reco.detect_circles()
#
#try:
#    reco.set_circles_coordinates()
#except recognizer.UknwCircleCoordsException as e:
#    print(f"{e.circle} \n Coordinates cannot be determined")
#    exit()