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
        self.gridnames = [x for x in os.listdir("./test_grids") if x.endswith(".jpg") or x.endswith(".jpeg")]
        self.expected = json.load(open("test_grids/expected.json", "r"))

    # We test the number of detected circles
    def test_detect_circles(self):
        for gn in self.gridnames:
            img = cv2.imread(f"test_grids/{gn}")
            reco = grid_recognizer.Grid(img)
            reco.detect_circles()
            self.assertEqual(len(reco.circles), \
                self.expected["expected"][gn]["circles_nb"])
        



if __name__ == '__main__':
    unittest.main()