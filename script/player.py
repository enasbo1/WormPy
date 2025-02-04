from engine.collider import Collider, PolygonBox, CircleBox
from engine.physicsBody import PhysicsBody, LinearForceField, collision_walk
from engine.worker import MonoBehavior, PygIO, pyg
from script.wormElement import Worm

class PlayerObject(MonoBehavior):
    name = "default"
    pointer = 0
    worms:list[Worm] = []

    def playerTurn(self):
        # check if player still have worm
        if not (len(self.worms) > 0):
            return

        # select worm
        if self.pointer > len(self.worms):
            self.pointer = 0
        currentWorm = self.pointer

        # control worm for x time && no final action
        timeLimit = 10
        currentTime = 0
        finalAction = False
        while currentTime < timeLimit and finalAction != True:
            currentTime += self.worker.deltaTime
            # control worm and select tool

        # prepare player to use next worm
        self.pointer += 1
        pass