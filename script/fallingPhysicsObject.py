from engine.collider import Collider, PolygonBox
from engine.physicsBody import PhysicsBody, LinearForceField, collision_walk
from engine.worker import MonoBehavior, PygIO, pyg
import backwork.direction as direct


class FallingPhysicsObject(MonoBehavior):
    polygonSkinPoints = ((0., 25.), (10., 20.), (10., 0.), (0., -5.), (-10., 0.), (-10., 20.))
    floored = False;

    def onCreate(self):
        self.physicBody = PhysicsBody(self, onCollide=self.onCollide, forces=[LinearForceField((0, 100))], position=self.position)
        self.collider = Collider(self.worker, PolygonBox(self.polygonSkinPoints))
        self.physicBody.addSpeed((150, -15))
        print(self, self.collider, self.collider.box_holes)

    def update(self):
        pass

    def show(self, pygIO: PygIO):
        self.collider.show_collider(pygIO, color='#118811', position=self.physicBody.get_extrapolate());

    def fixedUpdate(self):
        self.collider.move_to(self.physicBody.get_position())
        if self.floored:
            self.physicBody.addSpeed(direct.fact_vect(self.physicBody.velocity, -0.05))
        self.floored = False;

    def onCollide(self, physicsBody, collisionVector: tuple[float, float]):
        if collision_walk(physicsBody, collisionVector):
            self.floored = True;
        print("colide");