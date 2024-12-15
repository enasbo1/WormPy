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
        Field(self.worker).collider.move_to((350,100));
        FallingPhysicsObject(self.worker);

    def update(self):
        pass

    def show(self, pygIO:PygIO):
        pass

    def fixedUpdate(self):
        pass