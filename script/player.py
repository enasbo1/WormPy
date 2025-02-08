from engine.worker import MonoBehavior
from script.wormElement import Worm
from engine.pygio import pyg


class PlayerObject(MonoBehavior):
    name = "default"
    color = '#880000'
    currentWormIndex = 0
    playTime = 0
    playTimeLimit = 5
    controls: tuple[int, int, int, int]
    worms: list[Worm]

    def onCreate(self):
        # controls: up, down, left, right
        self.controls: tuple[int, int, int, int] = (pyg.K_UP, pyg.K_DOWN, pyg.K_LEFT, pyg.K_RIGHT)
        self.worms: list[Worm] = []

    def set_control(self, controls: tuple[int, int, int, int] = (pyg.K_UP, pyg.K_DOWN, pyg.K_LEFT, pyg.K_RIGHT)):
        self.controls = controls

    def addWorm(self) -> Worm:
        newWorm = Worm(self.worker)
        newWorm.color = self.color
        self.worms.append(newWorm)
        return newWorm
    def playerTurn(self) -> bool:


        # check if it's still the player turn and he still had a worm
        if not (len(self.worms) > 0) or self.playTime >= self.playTimeLimit:
            self.playTime = 0
            self.currentWormIndex += 1
            return True

        # select player next worm
        if self.currentWormIndex >= len(self.worms):
            self.currentWormIndex = 0

        self.worms[self.currentWormIndex].playTurn(self.controls)
        self.playTime += self.worker.deltaTime

        return False
