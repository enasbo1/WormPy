import time

from engine.collider import Collider
from engine.physicsBody import PhysicsBody
from engine.pygio import PygIO, pyg

class Worker:
    def __init__(self, game):
        self.pygIO = PygIO();
        self.activeMBList:list[MonoBehavior] = [game];
        self.activePBList:list[PhysicsBody] = [];
        self.activeCollider:list[Collider] = [];
        self.gameMaster = game;
        game.worker = self;
        self.deltaTime = 0;
        self._grapTimeMark = time.time();
        self._physTimeMark = 0;
        self.extrapolatePhysicsDelta = 0;
        self.physStepDuration = 0.03;
        self.keysInput:pyg.ScancodeWrapper = None
        game.onCreate();

    def start(self):
        self.gameMaster.start();

    def end(self):
        self.pygIO.end();

    def mainLoop(self):
        self.deltaTime = time.time() - self._grapTimeMark;
        self.extrapolatePhysicsDelta = time.time() - self._physTimeMark;
        self._grapTimeMark = time.time();

        for i in self.activeMBList:
            i.update();

        self.pygIO.prepare_update()

        for i in self.activeMBList:
            i.show(self.pygIO);

        self.pygIO.update();

        if (time.time() - self._physTimeMark) >  self.physStepDuration:
            self.deltaTime = self.physStepDuration;
            self._physTimeMark = time.time();
            self.keysInput = self.pygIO.getKeys()
            for i in self.activeMBList:
                i.fixedUpdate();
            for i in self.activePBList:
                i.applyPhysicStep();

class MonoBehavior:
    def __init__(self, worker:Worker):
        self.worker = worker
        worker.activeMBList.append(self)
        self.physicBody:PhysicsBody = None;
        self.collider:Collider = None;
        self.onCreate()

    def onCreate(self):
        pass


    def update(self):
        pass

    def show(self, pygIO:PygIO):
        pass

    def fixedUpdate(self):
        pass

    def destroy(self):
        self.worker.activeMBList.remove(self);

class GameMaster(MonoBehavior):
    def __init__(self):
        self.worker = None;

    def start(self):
        pass