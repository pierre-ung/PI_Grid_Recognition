from logging import shutdown
import numpy as np
import grid_recognizer as recognizer
from flask import Flask, request, abort, jsonify, Response
from werkzeug.exceptions import HTTPException
import sys
import hashitools as ht


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
@app.route('/grid', methods=['POST'])
def create_structure():
    # Decode the base64 img (-> cv2 image)
    b64 = request.values['photo_b64'] 
    img = ht.b64_to_cv(b64)
    
    # Recognizer
    ## Creation
    reco = recognizer.Grid(img, resize_width=1200)
    ## Circle detection
    reco.detect_circles()
    ## Set circle game coordinates
    try:
        reco.set_circles_coordinates()
    except recognizer.UknwCircleCoordsException as e:
        ### Return error code in case of failure
        abort(412, e)
    
    # Generate json file describing the grid 
    reco.generate_json()
    return Response(reco.json, mimetype='application/json')

###########################################
if __name__ == "__main__":
    if(len(sys.argv) > 1 and sys.argv[1] == "build-only"):
        exit(0)
    app.run(host="0.0.0.0", port=50001)
    