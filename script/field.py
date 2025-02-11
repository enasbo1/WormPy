from random import randint

from engine.collider import Collider, PolygonBox, CircleBox
from engine.worker import MonoBehavior, PygIO, pyg
import backwork.direction as direct
import numpy as np


def horseshoe_contour(center=(0, -100), inner_radius=400, outer_radius=700, num_points=25):
    points = []

    # Arc intérieur (demi-cercle intérieur)
    for theta in np.linspace(0, np.pi, num_points):
        x = center[0] + inner_radius * np.cos(theta)
        y = (center[1] + inner_radius * np.sin(theta) *0.5) + randint(-40,20)
        points.append((int(x), int(y)))

    # Arc supérieur (demi-cercle extérieur)
    for theta in np.linspace(np.pi, 0, num_points//3):
        x = center[0] + outer_radius * np.cos(theta)
        y = center[1] + outer_radius * np.sin(theta) * 0.5 + randint(-40,40)
        points.append((int(x), int(y)))

    points.reverse()
    return tuple(points)

class Field(MonoBehavior):
    skinPoints = horseshoe_contour();

    def onCreate(self):
        self.skinPoints = direct.change_ref(0,100,self.skinPoints)
        self.collider = Collider(self.worker, PolygonBox(self.skinPoints));
        self.collider.move_to(position=(50,0))

    def update(self):
        pass

    def show(self, pygIO:PygIO):
        self.collider.show_collider(pygIO)

    def fixedUpdate(self):
        pass
