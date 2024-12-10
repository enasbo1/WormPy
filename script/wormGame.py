from engine.worker import GameMaster, PygIO
from script.wormElement import Worm

class WormGame(GameMaster):
    def onCreate(self):
        pass

    def start(self):
        Worm(self.worker);

    def update(self):
        pass

    def show(self, pygIO:PygIO):
        pass

    def fixedUpdate(self):
        pass