import time
from engine.pygio import PygIO

class Worker:
    def __init__(self, game):
        self.pygIO = PygIO();
        self.activeMBList:MonoBehavior = [game];
        self.gameMaster = game;
        game.worker = self;
        self.deltaTime = 0;
        self._grapTimeMark = time.time();
        self._physTimeMark = 0;
        self.physStepDuration = 0.03;
        self.keysInput = None

    def start(self):
        self.gameMaster.start();

    def end(self):
        self.pygIO.end();

    def mainLoop(self):
        self.deltaTime = time.time() - self._grapTimeMark;
        self._grapTimeMark = time.time();

        for i in self.activeMBList:
            i.update();
        for i in self.activeMBList:
            i.show(self.pygIO);

        self.pygIO.update();

        if self._physTimeMark - time.time() >  self.physStepDuration:
            self.deltaTime = self.physStepDuration;
            self.keysInput = self.pygIO.getKeys()
            for i in self.activeMBList:
                    i.fixedUpdate();

class MonoBehavior:
    def __init__(self, worker:Worker):
        self.worker = worker
        worker.activeMBList.append(self)
        self.onCreate()

    def onCreate(self):
        pass


    def update(self):
        pass

    def show(self, pygIO:PygIO):
        pass

    def fixedUpdate(self):
        pass

class GameMaster(MonoBehavior):
    def __init__(self):
        self.worker = None;

    def start(self):
        pass