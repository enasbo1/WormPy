from engine.worker import MonoBehavior, PygIO, pyg
import backwork.direction as direct

class Worm(MonoBehavior):
    y = None
    x = None

    def onCreate(self):
        print('hello world')
        print(self.worker)
        self.x = 0
        self.y = 0

    def update(self):
        pass

    def show(self, pygIO:PygIO):
        pygIO.draw_poly(direct.change_ref (self.x, self.y ,((10,10),(10,-10),(-10,-15), (-10,15))),'#000000')

    def fixedUpdate(self):
        self.x += self.worker.deltaTime;
