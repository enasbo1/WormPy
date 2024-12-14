from engine.collider import Collider, PolygonBox
from engine.physicsBody import PhysicsBody, LinearForceField
from engine.worker import MonoBehavior, PygIO, pyg
import backwork.direction as direct

class FallingPhysicsObject(MonoBehavior):
    skinPoints = ((0.,25.),(10.,20.),(10.,0.),(0.,-5.),(-10.,0.),(-10.,20.))

    def onCreate(self):
        self.physicBody = PhysicsBody(self, forces = [LinearForceField((0,25))]);
        self.collider = Collider(self.worker, PolygonBox(self.skinPoints));
        self.physicBody.addSpeed((0,-100))

    def update(self):
        pass

    def show(self, pygIO:PygIO):
        self.collider.show_collider(pygIO, color='#118811', position=self.physicBody.get_extrapolate());

    def fixedUpdate(self):
        self.collider.move_to(self.physicBody.get_position())
