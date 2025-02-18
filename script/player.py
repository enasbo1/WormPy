from engine.worker import MonoBehavior
from script.wormElement import Worm
from engine.pygio import pyg


class PlayerObject(MonoBehavior):
    name = "default"
    color = '#880000'
    currentWormIndex = 0
    playTime = 0
    playTimeLimit = 10
    controls: tuple[int, int, int, int]
    worms: list[Worm]

    def onCreate(self):
        # Controls: up, down, left, right
        self.controls: tuple[int, int, int, int] = (pyg.K_UP, pyg.K_DOWN, pyg.K_LEFT, pyg.K_RIGHT)
        self.worms = []

    def set_control(self, controls: tuple[int, int, int, int] = (pyg.K_UP, pyg.K_DOWN, pyg.K_LEFT, pyg.K_RIGHT)):
        self.controls = controls

    def addWorm(self, friction: float) -> Worm:
        newWorm = Worm(self.worker)
        newWorm.color = self.color
        newWorm.friction = friction
        self.worms.append(newWorm)
        return newWorm

    def playerTurn(self) -> bool:
        # Check if the player still had a worm
        if not (len(self.worms) > 0):
            return True

        if self.currentWormIndex >= len(self.worms):
            self.currentWormIndex = 0

        # Check if it's still the player turn
        if self.playTime >= self.playTimeLimit or not self.worms[self.currentWormIndex].playTurn(self.controls):
            self.worms[self.currentWormIndex].indicator = False
            self.playTime = 0
            self.currentWormIndex += 1
            self.currentWormIndex %= len(self.worms)
            return True

        self.worms[self.currentWormIndex].indicator = True
        self.playTime += self.worker.deltaTime

        return False
