from engine.worker import MonoBehavior, PygIO, pyg

class Worm(MonoBehavior):
    def onCreate(self):
        print('hello world')
        print(self.worker)

    def update(self):
        pass

    def show(self, pygIO:PygIO):
        pass

    def fixedUpdate(self):
        if self.worker.keysInput[pyg.K_SPACE]:
            print('coucou');
