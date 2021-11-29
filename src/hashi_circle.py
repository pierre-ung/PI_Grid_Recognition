"""
A class to represent recognized circles.

Attributes
----------
center_x : int
    The X coordinate of the circle center 

center_y : int
    The Y coordinate of the circle center 

radius : int
    The circle radius

position : (int, int)
    The position of the circle in the game grid (e.g: top left box is (0,0), the one at its right is (1, 0))
    (-1, -1) means that the position is unknown
"""

class HashiCircle:
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.position = (-1, -1)

    def __str__(self):
        return "center_coords: {0}\nradius: {1}\nposition: {2}".format((self.center_x, self.center_y), self.radius, self.position)

    def is_betweenX(self, firstCoord, secondCoord):
        return firstCoord <= self.center_x  <= secondCoord

    def is_betweenY(self, firstCoord, secondCoord):
        return firstCoord <= self.center_y <= secondCoord