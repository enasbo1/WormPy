from engine.collider import Collider, PolygonBox
from engine.physicsBody import PhysicsBody
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
        self.collider.move_to(position=(150,0))

    def update(self):
        pass

    def show(self, pygIO:PygIO):
        self.collider.show_collider(pygIO)

    def fixedUpdate(self):
        pass