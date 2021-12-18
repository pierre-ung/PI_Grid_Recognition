import unittest
import os 
import sys
import json
import cv2
# Import files
sys.path.append("../")
import grid_recognizer


class StructureRecoTest(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.gridnames = [x for x in os.listdir("test_grids") if x.endswith(".jpg") or x.endswith(".jpeg")]
        self.expected = json.load(open("test_grids/expected_results.json", "r"))

    # Test if the number of detected circles is correct
    def test_detect_circles(self):
        for gn in self.gridnames:
            img = cv2.imread(f"test_grids/{gn}")
            reco = grid_recognizer.Grid(img)
            reco.detect_circles()
            self.assertEqual(len(reco.circles), \
                len(self.expected["expected"][gn]["circles_index"]))
    
    # Test if circles coordinates are  
    def test_circles_position(self):
        for gn in self.gridnames:
            img = cv2.imread(f"test_grids/{gn}")
            reco = grid_recognizer.Grid(img)
            reco.detect_circles()
            reco.set_circles_coordinates()
            # circles positions -> index
            index = []
            for c in reco.circles:
                if(c.position != (-1,-1)):
                    index.append(c.position[0] + c.position[1]*reco.width)
                else:
                    index.append(-1)

            try:
                reco.set_circles_coordinates()
            except reco.UknwCircleCoordsException as e:
                self.assertIn(-1, reco.circles)

            # check if every expected coordinates are ok
            self.assertCountEqual(index, self.expected["expected"][gn]["circles_index"])
    


        



if __name__ == '__main__':
    unittest.main()
