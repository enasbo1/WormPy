from random import random, randint

from engine.physicsBody import PhysicsBody, SpeedLimitForce
from engine.pygio import PygIO
from engine.worker import MonoBehavior
from script.wormElement import Winded


class Leaf(MonoBehavior):
    timer = 0;
    def onCreate(self):
        self.physicBody = PhysicsBody(self, forces=[Winded.wind, SpeedLimitForce(120)])

    def fixedUpdate(self):
        self.timer -= self.worker.deltaTime;
        if self.timer<0:
            self.physicBody.teleport(self.worker.pygIO.getRandomScreenPosition());
            self.physicBody.setSpeed((randint(-5,5), randint(-5,5)));
            self.timer = randint(10,25)/10;

    def show(self, pygIO:PygIO):
        pos = self.physicBody.get_position()
        pygIO.draw_circle(pos[0], pos[1], 5, color='#999999')