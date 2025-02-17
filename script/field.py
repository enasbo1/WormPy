from random import randint

from engine.collider import Collider, PolygonBox
from engine.worker import MonoBehavior, PygIO
import backwork.direction as direct
import numpy as np


class Field(MonoBehavior):
    skinPoints: tuple[tuple[float, float], ...]

    def horseshoe_contour(self, center=(0, -100), inner_radius=400, depth=300, num_points=9):
        outer_radius = inner_radius + depth
        points = []

        # Arc intérieur (demi-cercle intérieur)
        for theta in np.linspace(0, np.pi, num_points):
            x = center[0] + inner_radius * np.cos(theta)
            y = (center[1] + inner_radius * np.sin(theta) * 0.5) + randint(-40, 20)
            points.append((int(x), int(y)))

        # Arc supérieur (demi-cercle extérieur)
        for theta in np.linspace(np.pi, 0, num_points // 2):
            x = center[0] + outer_radius * np.cos(theta)
            y = center[1] + outer_radius * np.sin(theta) * 0.5 + randint(-40, 40)
            points.append((int(x), int(y)))

        points.reverse()
        self.skinPoints = direct.change_ref(0, 100, tuple(points))
        self.collider = Collider(self.worker, PolygonBox(self.skinPoints))

    def onCreate(self):
        pass

    def update(self):
        pass

    def show(self, pygIO: PygIO):
        self.collider.show_collider(pygIO)

    def fixedUpdate(self):
        pass
