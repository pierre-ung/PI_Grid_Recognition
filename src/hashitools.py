import cv2
import base64
import numpy as np

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


'''
Encode a cv image to a base64 string
@param cv_img : cv2 image
    The image to encode
@return The base64 string corresponding to cv_img 
'''
def cv_to_b64_str(cv_img):
    b64_str = base64.b64encode(cv2.imencode('.jpg', cv_img)[1]).decode()
    return b64_str

