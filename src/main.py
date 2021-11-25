
import grid_recognizer as recognizer

reco = recognizer.Grid("grids/hashi1.png", 784)
if(reco.detect_circles()): # Circle(s) have been detected
    for circle in reco.circles:
        print(str(circle))