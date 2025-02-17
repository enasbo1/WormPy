from random import randint

from engine.physicsBody import PhysicsBody, LinearForceField, collision_walk, SpeedLimitForce
from engine.collider import Collider, PolygonBox
from engine.worker import MonoBehavior, PygIO
import backwork.direction as direct
from script.grenade import Grenade
from script.missile import Missile


class Worm(MonoBehavior):
    skinPoints = ((0., 25.), (10., 20.), (10., 0.), (0., -5.), (-10., 0.), (-10., 20.))
    color = '#880000'
    wormList: list[MonoBehavior]
    health = 200
    healthMax = 200
    healthWidth = 75
    floored = False
    friction = 0.1
    indicator = False
    cooldown = 0

    def init(self, wormList: list[MonoBehavior]) -> MonoBehavior:
        self.wormList = wormList
        return self

    def onCreate(self):
        self.physicBody = PhysicsBody(self, onCollide=self.onCollide, forces=[LinearForceField((0, 100)),SpeedLimitForce(500)])
        self.collider = Collider(self.worker, PolygonBox(self.skinPoints), active=False)
        self.physicBody.teleport((randint(-400, 400), -500))
        self.physicBody.addSpeed((0, 400))

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
            self.physicBody.addSpeed(direct.fact_vect(self.physicBody.velocity, -self.friction))
        self.floored = False

    def onCollide(self, physicsBody, collisionVector: tuple[float, float]):
        if direct.scalar(collisionVector, physicsBody.movement) > 8:
            self.health -= 10
        if collision_walk(physicsBody, collisionVector):
            self.floored = True

    def to_speed_x(self, acc: float, speed_cap: float):
        if abs(self.physicBody.velocity[0]) < abs(speed_cap):
            self.physicBody.addSpeed((acc*self.worker.deltaTime, 0))

    def playTurn(self, controls: tuple[int, int, int, int]) -> bool:
        self.cooldown -= self.worker.deltaTime
        if self.worker.keysInput[controls[0]] and self.floored:  # up
            self.physicBody.addSpeed((0, -100))
            return True

        if self.worker.keysInput[controls[2]]:  # left
            self.to_speed_x(-48*(1+self.floored), -100)
            return True

        if self.worker.keysInput[controls[3]]:  # right
            self.to_speed_x(48*(1+self.floored), 100)
            return True

        if self.worker.keysInput[controls[1]] and self.cooldown < 0:
            gr = Grenade(self.worker).init(self.wormList).physicBody
            pos = self.physicBody.get_position()
            gr.teleport(pos)
            gr.addSpeed(direct.vector(pos,direct.vector((self.worker.pygIO.width//2, self.worker.pygIO.height//2), self.worker.mouse.get_pos())))
            self.cooldown = 1.5
            return False

        if self.worker.mouse.get_pressed()[0] and self.cooldown < 0:
            gr = Missile(self.worker).init(self.wormList).physicBody
            pos = self.physicBody.get_position()
            gr.teleport(pos)
            gr.addSpeed(direct.vector(pos,direct.vector((self.worker.pygIO.width//2, self.worker.pygIO.height//2), self.worker.mouse.get_pos())))
            self.cooldown = 1.5
            return False

        return True

    def isAlive(self) -> bool:
        if self.health > 0:
            return True

        self.destroy()
        return False
