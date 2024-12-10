import pygame as pyg

class PygIO:
    def __init__(self):
        pyg.init()
        self.screen = pyg.display.set_mode((1280, 720))
        self.clock = pyg.time.Clock()
        self.running = True

    def update(self):
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                self.running = False
        pyg.display.flip()

    def getKeys(self):
        return pyg.key.get_pressed()

    def end(self):
        pyg.quit()