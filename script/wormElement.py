from engine.worker import MonoBehavior, PygIO, pyg

class Worm(MonoBehavior):
    y = None
    x = None

    def onCreate(self):
        self.x = 0
        self.y = 0

    def update(self):
        pass

    def show(self, pygIO:PygIO):
        pygIO.draw_circle(self.x, self.y,8,'#880000', width = 2);
        pygIO.draw_poly(((10, 10), (40, 50), (70, 10), (50, 30), (30, 20)), "#111111")

    def fixedUpdate(self):
        self.x += self.worker.deltaTime*10;
