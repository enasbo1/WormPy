from engine.worker import GameMaster, PygIO
from script.fallingPhysicsObject import FallingPhysicsObject
from script.field import Field
from script.wormElement import Worm
from script.player import PlayerObject


class WormGame(GameMaster):
    players = []

    def onCreate(self):
        pass

    def start(self):
        # declaration order set depth
        Field(self.worker)
        Field(self.worker).collider.move_to((400, 100))
        # worms = [Worm(self.worker), Worm(self.worker)]

        test = PlayerObject(self.worker)
        test.worms.append(Worm(self.worker))

        self.players.append(test)
        FallingPhysicsObject(self.worker, position=[0, -20])

    def update(self):
        pass

    def show(self, pygIO: PygIO):
        pass

    def fixedUpdate(self):
        for player in self.players:
            # print(player.worms)
            pass

