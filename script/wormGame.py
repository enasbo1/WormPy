from engine.worker import GameMaster, PygIO
from script.field import Field
from script.player import PlayerObject
from script.wormElement import Worm
import os


class WormGame(GameMaster):
    currentPlayerIndex = 0
    players: list[PlayerObject] = []
    playerTimeLimit = 10
    turn = 0
    waitTime = 0
    waitTimeLimit = 2
    waterHeight = 100
    waterRisingTurn = 2
    waterY = 0
    wormList: list[Worm] = []
    wormColors = ["#222288", "#882222"]
    wormPerPlayer = 2

    def onCreate(self):
        self.worker.show_over = self.show_over

    def readConfig(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "..", "config.txt")
        with open(config_path, "r") as config:
            for line in config:
                lineData = line.rstrip().split("=")
                if len(lineData) > 1:
                    if lineData[0] == 'PLAYER_COLORS':
                        self.wormColors = lineData[1].split(",")

                    if lineData[0] == 'WORMS_PER_PLAYER':
                        self.wormPerPlayer = int(lineData[1])

                    if lineData[0] == 'PLAYER_TIME_LIMIT':
                        self.playerTimeLimit = int(lineData[1])

                    if lineData[0] == 'WAIT_TIME_LIMIT':
                        self.waitTimeLimit = int(lineData[1])

                    if lineData[0] == 'WATER_HEIGHT_START':
                        self.waterHeight = int(lineData[1])

                    if lineData[0] == 'WATER_RISING_TURN':
                        self.waterRisingTurn = int(lineData[1])

    def start(self):
        Field(self.worker).collider.move_to((0,0))
        # for i in range(50):
        #     n = FallingPhysicsObject(self.worker).physicBody;
        #     n.teleport((700-(20*i), -100 + randint(-50, 50)));
        #     n.addSpeed((0, randint(-50,150)))
        # hole = CircleBox(100,100,75)
        # self.worker.set_hole(hole)

        self.readConfig()

        for i in self.wormColors:
            player = PlayerObject(self.worker)
            player.color = i
            player.playTimeLimit = self.playerTimeLimit
            for j in range(self.wormPerPlayer):
                self.wormList.append(player.addWorm().init(self.wormList))
                self.wormList.append(player.addWorm().init(self.wormList))
            self.players.append(player)

    def update(self):
        pass

    def show_over(self, pygIO: PygIO):
        current = self.getCurrent()
        color = current.color
        passing = 0
        if self.waitTime < self.waitTimeLimit:
            color = '#777777'
            passing = (self.waitTimeLimit-self.waitTime)/self.waitTimeLimit
        else:
            passing = (current.playTimeLimit-current.playTime)/current.playTimeLimit

        pygIO.draw_circle(-pygIO.width // 2 + 50, -pygIO.height // 2 + 50, 30 + (45 * passing), "#888888")
        pygIO.draw_circle(-pygIO.width // 2 + 50, -pygIO.height // 2 + 50, 30, color)

        # Water
        self.waterY = (pygIO.height // 2) - self.waterHeight
        pygIO.draw_rect(-pygIO.width // 2, self.waterY, pygIO.width, self.waterHeight, '#005599')
        pass

    def fixedUpdate(self):
        # Player/Worm Turns
        if self.waitTime >= self.waitTimeLimit:
            if self.getCurrent().playerTurn():
                self.nextPlayer()

        # Remove dead worms
        for player in self.players:
            for worm in player.worms:
                pos = worm.physicBody.get_extrapolate()
                if pos[1] >= self.waterY:
                    worm.health = 0
                if not worm.isAlive():
                    if player.playTime > 0:
                        player.playTime = player.playTimeLimit
                    player.worms.remove(worm)
                    del worm

        self.waitTime += self.worker.deltaTime

    def getCurrent(self):
        return self.players[self.currentPlayerIndex]

    def nextPlayer(self):
        self.waitTime = 0
        self.currentPlayerIndex += 1
        if self.currentPlayerIndex >= len(self.players):
            self.turn += 1
            self.currentPlayerIndex = 0

            if self.turn > self.waterRisingTurn:
                self.waterHeight += 5
