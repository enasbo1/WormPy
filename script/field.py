from engine.collider import Collider, PolygonBox, CircleBox
from engine.worker import MonoBehavior, PygIO, pyg
import backwork.direction as direct

class Field(MonoBehavior):
    skinPoints = (
        (0, 0),
        (500, 0),
        (800, 200),
        (1000, 150),
        (1300, 300),
        (1500, 250),
        (1700, 400),
        (1800, 600),
        (1700, 800),
        (1500, 900),
        (1400, 1050),
        (1200, 1100),
        (1000, 1000),
        (800, 1100),
        (600, 950),
        (400, 900),
        (300, 700),
        (200, 750),
        (100, 600),
        (50, 400),
        (0, 350)
    )


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
