from engine.physicsBody import PhysicsBody, LinearForceField, collision_walk
from engine.collider import Collider, PolygonBox, CircleBox
from engine.worker import MonoBehavior, PygIO, pyg
import backwork.direction as direct


class Worm(MonoBehavior):
    skinPoints = ((0., 25.), (10., 20.), (10., 0.), (0., -5.), (-10., 0.), (-10., 20.))
    color = '#880000'
    floored = False

    def onCreate(self):
        self.physicBody = PhysicsBody(self, onCollide=self.onCollide, forces=[LinearForceField((0, 100))])
        self.collider = Collider(self.worker, PolygonBox(self.skinPoints), active=False)
        self.physicBody.addSpeed((150, -15))

    def update(self):
        pass

    def show(self, pygIO:PygIO):

        #if 'global_collision' in self.collider.mark:
        #    color = '#111188'
        #if 'hole_collision' in self.collider.mark:
        #    color = '#881111'
        #if 'hole_noCollision' in self.collider.mark:
        #    color = '#888811'

        self.collider.show_collider(pygIO, color=self.color, position=self.physicBody.get_extrapolate())

    def fixedUpdate(self):
        self.collider.move_to(self.physicBody.get_position())

        if self.floored:
            self.physicBody.addSpeed(direct.fact_vect(self.physicBody.velocity, -0.05))
        self.floored = False

    def onCollide(self, physicsBody, collisionVector: tuple[float, float]):
        if collision_walk(physicsBody, collisionVector):
            self.floored = True


    def to_speed_x(self, acc:float, speed_cap:float):
        if abs(self.physicBody.velocity[0])<abs(speed_cap):
            self.physicBody.addSpeed((acc*self.worker.deltaTime,0));

    def playTurn(self, controls:tuple[int,int,int,int]):
        if self.worker.keysInput[controls[0]] and self.floored:  # up
            self.physicBody.addSpeed((0, -100))
            pass
        if self.worker.keysInput[controls[2]]:  # left
            self.to_speed_x(-40, -100);
            pass
        if self.worker.keysInput[controls[3]]:  # right
            self.to_speed_x(40, 100);
            pass