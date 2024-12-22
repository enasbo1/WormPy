from engine.collider import Collider, PolygonBox, CircleBox
from engine.worker import MonoBehavior, PygIO, pyg
import backwork.direction as direct

class Field(MonoBehavior):
    skinPoints = ((0.,0.),
                  (100.,-50.),
                  (200.,-50.),
                  (150.,50.),
                  (50.,100.),
                  (-50.,100.),
                  (-150.,50.),
                  (-200.,-50.),
                  (-100.,-50)
                  )

    def onCreate(self):
        self.skinPoints = direct.change_ref(0,100,self.skinPoints)
        self.collider = Collider(self.worker, PolygonBox(self.skinPoints));
        self.collider.move_to(position=(50,0))
        hole = CircleBox(100,100,75)
        self.collider.set_hole(hole)

    def update(self):
        pass

    def show(self, pygIO:PygIO):
        self.collider.show_collider(pygIO)

    def fixedUpdate(self):
        pass
