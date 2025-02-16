from engine.worker import GameMaster, PygIO
from script.field import Field
from script.player import PlayerObject


class WormGame(GameMaster):
    players: list[PlayerObject] = []
    currentPlayerIndex = 0
    waitTime = 0
    waitTimeLimit = 2
    turn = 0
    waterHeight = 275
    waterY = 0

    def onCreate(self):
        pass

    def start(self):
        Field(self.worker).collider.move_to((-1000,-100))
        # for i in range(50):
        #     n = FallingPhysicsObject(self.worker).physicBody;
        #     n.teleport((700-(20*i), -100 + randint(-50, 50)));
        #     n.addSpeed((0, randint(-50,150)))
        # hole = CircleBox(100,100,75)
        # self.worker.set_hole(hole)

        for i in ("#008800", "#880000"):
            test = PlayerObject(self.worker)
            test.color = i
            test.addWorm()
            test.addWorm()
            self.players.append(test)

    def update(self):
        pass

    def show(self, pygIO: PygIO):
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
                    # End player turn if he killed his worm
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
            print(self.turn)
            self.currentPlayerIndex = 0

            if self.turn > 2:
                self.waterHeight += 5
