from random import randint

from engine.collider import CircleBox
from engine.worker import GameMaster, PygIO
from script.fallingPhysicsObject import FallingPhysicsObject
from script.field import Field
from script.wormElement import Worm

class WormGame(GameMaster):
    def onCreate(self):
        pass

    def start(self):
        Worm(self.worker);
        Field(self.worker);
        Field(self.worker).collider.move_to((400,100));
        for i in range(50):
            n = FallingPhysicsObject(self.worker).physicBody;
            n.teleport((700-(20*i), -100 + randint(-50, 50)));
            n.addSpeed((0, randint(-50,150)))
        hole = CircleBox(100,100,75)
        self.worker.set_hole(hole)

    def update(self):
        pass

    def show(self, pygIO:PygIO):
        pass

    def fixedUpdate(self):
        pass