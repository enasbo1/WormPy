from engine.worker import GameMaster, PygIO
from script.field import Field
from script.player import PlayerObject
from script.wormElement import Worm
import os


class WormGame(GameMaster):
    currentPlayerIndex = 0
    gameOver = False
    fieldDepth = 300
    fieldHeight = 0
    fieldPoints = 25
    fieldWidth = 400
    players: list[PlayerObject] = []
    playerColors = ["#222288", "#882222"]
    playerTimeLimit = 10
    turn = 0
    waitTime = 0
    waitTimeLimit = 2
    waterHeightCurrent = 0
    waterHeightTarget = 100
    waterRisePerTurn = 20
    waterRisingTurn = 2
    waterY = 0
    wormList: list[Worm] = []
    wormFriction = 0.10
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
                        self.playerColors = lineData[1].split(",")

                    if lineData[0] == 'WORMS_PER_PLAYER':
                        self.wormPerPlayer = int(lineData[1])

                    if lineData[0] == 'PLAYER_TIME_LIMIT':
                        self.playerTimeLimit = int(lineData[1])

                    if lineData[0] == 'WAIT_TIME_LIMIT':
                        self.waitTimeLimit = int(lineData[1])

                    if lineData[0] == 'WORM_FRICTION':
                        self.wormFriction = float(lineData[1])

                    if lineData[0] == 'WATER_HEIGHT_START':
                        self.waterHeightTarget = int(lineData[1])

                    if lineData[0] == 'WATER_RISING_TURN':
                        self.waterRisingTurn = int(lineData[1])

                    if lineData[0] == 'WATER_RISE_PER_TURN':
                        self.waterRisePerTurn = int(lineData[1])

                    if lineData[0] == 'FIELD_WIDTH':
                        self.fieldWidth = int(lineData[1])

                    if lineData[0] == 'FIELD_DEPTH':
                        self.fieldDepth = int(lineData[1])

                    if lineData[0] == 'FIELD_HEIGHT':
                        self.fieldHeight = -int(lineData[1])

                    if lineData[0] == 'FIELD_POINTS':
                        self.fieldPoints = int(lineData[1])

    def start(self):
        self.readConfig()

        a = Field(self.worker)
        a.horseshoe_contour(inner_radius=self.fieldWidth, depth=self.fieldDepth, num_points=self.fieldPoints)
        a.collider.move_to((0, self.fieldHeight))

        for color in self.playerColors:
            player = PlayerObject(self.worker)
            player.color = color.strip()
            player.playTimeLimit = self.playerTimeLimit
            for j in range(self.wormPerPlayer):
                self.wormList.append(player.addWorm(self.wormFriction).init(self.wormList))
                self.wormList.append(player.addWorm(self.wormFriction).init(self.wormList))
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

        circlePos = (-pygIO.width // 2 + 50, -pygIO.height // 2 + 50)
        pygIO.draw_circle(circlePos[0], circlePos[1], 30 + (45 * passing), "#888888")
        pygIO.draw_circle(circlePos[0], circlePos[1], 30, color)
        pygIO.draw_text(circlePos[0], circlePos[1]+2, str(self.turn), 65, "#000000")

        # Water
        self.waterY = (pygIO.height // 2) - self.waterHeightCurrent
        pygIO.draw_rect(-pygIO.width // 2, self.waterY, pygIO.width, self.waterHeightCurrent, '#005599')

        # Victory screen
        if self.waitTime >= self.waitTimeLimit:
            if self.gameOver:
                pygIO.draw_rect(-110, -50, 220, 100, "#000000")
                if len(current.worms) > 0:
                    pygIO.draw_rect(-93, -26, 52, 52, "#FFFFFF")
                    pygIO.draw_rect(-92, -25, 50, 50, current.color)
                    pygIO.draw_text(40, 0, 'win', 90, "#FFFFFF")
                else:
                    pygIO.draw_text(0, 0, 'draw', 90, "#FFFFFF")
        pass

    def fixedUpdate(self):
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

        if self.waitTime >= self.waitTimeLimit:
            if self.gameOver:
                return

            # Player/Worm Turns
            if self.getCurrent().playerTurn():
                self.nextPlayer()

        # Water rise anim
        if self.waterHeightCurrent < self.waterHeightTarget:
            self.waterHeightCurrent += 1
            return

        self.waitTime += self.worker.deltaTime

    def getCurrent(self):
        return self.players[self.currentPlayerIndex]

    def nextPlayer(self):
        self.waitTime = 0
        self.currentPlayerIndex += 1
        self.checkNextTurn()

        playerAlive = len(self.players)
        while not len(self.getCurrent().worms) > 0 and playerAlive > 0:
            self.currentPlayerIndex += 1
            self.checkNextTurn()
            playerAlive -= 1

        if playerAlive <= 1:
            self.gameOver = True

    def checkNextTurn(self):
        if self.currentPlayerIndex >= len(self.players):
            self.turn += 1
            self.currentPlayerIndex = 0

            if self.turn >= self.waterRisingTurn:
                self.waterHeightTarget += self.waterRisePerTurn
