from engine.collider import Collider, PolygonBox
from engine.physicsBody import PhysicsBody, LinearForceField, collision_walk
from engine.worker import MonoBehavior, PygIO, pyg
import backwork.direction as direct
from script.wormElement import Winded


class FallingPhysicsObject(MonoBehavior):
    skinPoints = ((0.,25.),(10.,20.),(10.,0.),(0.,-5.),(-10.,0.),(-10.,20.))
    floored = False;
    def onCreate(self):
        self.physicBody = PhysicsBody(self, onCollide = self.onCollide, forces = [LinearForceField((0,100), Winded.wind)])
        self.collider = Collider(self.worker, PolygonBox(self.skinPoints), active=False)

        self.physicBody.addSpeed((150,-50))

    def update(self):
        pass

    def show(self, pygIO:PygIO):
        color = '#118811';

        if 'global_collision' in self.collider.mark:
            color = '#111188';
        if 'hole_collision' in self.collider.mark:
            color = '#881111';
        if 'hole_noCollision' in self.collider.mark:
            color = '#888811';
        self.collider.show_collider(pygIO, color=color, position=self.physicBody.get_extrapolate());

    def fixedUpdate(self):
        self.collider.move_to(self.physicBody.get_position())
        if self.floored:
            self.physicBody.addSpeed(direct.fact_vect(self.physicBody.velocity,-0.05))
        self.floored = False;
        pos = self.physicBody.get_position()
        if pos[1]>500:
            self.physicBody.teleport((pos[0], -500))

    def onCollide(self,physicsBody, collisionVector:tuple[float, float]):
        if collision_walk(physicsBody, collisionVector):
            self.floored = True;

