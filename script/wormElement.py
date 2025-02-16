from engine.physicsBody import PhysicsBody, LinearForceField, collision_walk
from engine.collider import Collider, PolygonBox
from engine.worker import MonoBehavior, PygIO
import backwork.direction as direct


class Worm(MonoBehavior):
    skinPoints = ((0., 25.), (10., 20.), (10., 0.), (0., -5.), (-10., 0.), (-10., 20.))
    color = '#880000'
    health = 200
    healthMax = 200
    healthWidth = 75
    floored = False
    indicator = False

    def onCreate(self):
        self.physicBody = PhysicsBody(self, onCollide=self.onCollide, forces=[LinearForceField((0, 100))])
        self.collider = Collider(self.worker, PolygonBox(self.skinPoints), active=False)
        self.physicBody.addSpeed((150, -15))

    def update(self):
        pass

    def show(self, pygIO: PygIO):
        # Display worm health
        pos = self.physicBody.get_extrapolate()
        healthDisplay = (self.health / self.healthMax) * self.healthWidth
        pygIO.draw_rect(pos[0] - (self.healthWidth / 2), pos[1] - 30, healthDisplay, 10, '#008800')

        # Display indicator
        if self.indicator:
            pygIO.draw_circle(pos[0], pos[1] - 30, 7.5, '#777777')

        # Display worm

        self.collider.show_collider(pygIO, color=self.color, position=pos)

    def fixedUpdate(self):
        self.collider.move_to(self.physicBody.get_position())

        if self.floored:
            self.physicBody.addSpeed(direct.fact_vect(self.physicBody.velocity, -0.05))
        self.floored = False

    def onCollide(self, physicsBody, collisionVector: tuple[float, float]):
        if collision_walk(physicsBody, collisionVector):
            self.floored = True

    def to_speed_x(self, acc: float, speed_cap: float):
        if abs(self.physicBody.velocity[0]) < abs(speed_cap):
            self.physicBody.addSpeed((acc*self.worker.deltaTime, 0))

    def playTurn(self, controls: tuple[int, int, int, int]):
        if self.worker.keysInput[controls[0]] and self.floored:  # up
            self.physicBody.addSpeed((0, -100))
            pass
        if self.worker.keysInput[controls[2]]:  # left
            self.to_speed_x(-40, -100)
            pass
        if self.worker.keysInput[controls[3]]:  # right
            self.to_speed_x(40, 100)
            pass

    def isAlive(self) -> bool:
        if self.health > 0:
            return True

        # del self.physicBody
        # del self.collider
        self.destroy()

        return False
