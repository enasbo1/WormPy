import pygame as pyg
import backwork.direction as direct
from pygame.draw import circle



class PygIO:
    def __init__(self):
        pyg.init()
        self.screen = pyg.display.set_mode()
        self.inputKeys = pyg.key.get_pressed()
        n = pyg.display.Info();
        self.width = n.current_w;
        self.height = n.current_h;
        self.clock = pyg.time.Clock();
        self.running = True;
        self.screen_color = '#81A4B5';
        self.draw = pyg.draw;

    def prepare_update(self):
        n = pyg.display.Info();
        self.width = n.current_w;
        self.height = n.current_h;
        self.screen.fill(self.screen_color);

    def update(self):
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                self.running = False
        if self.inputKeys[pyg.K_ESCAPE]:
            self.running = False;
        pyg.display.flip()

    def getKeys(self):
        self.inputKeys = pyg.key.get_pressed()
        return self.inputKeys;

    def end(self):
        pyg.quit()

    def draw_circle(self, x, y, r, color):
        self.draw.circle(self.screen, color, (x+(self.width//2), y + (self.height//2)), r)

    def draw_rect(self, x1, y1, x2, y2, color):
        self.draw.rect(self.screen, color, (x1+(self.width//2), y1 + (self.height//2), x2+(self.width//2), y2 + (self.height//2)))

    def draw_poly(self, coords, color):
        coords = direct.change_ref(self.width//2, self.height//2, coords);
        self.draw.polygon(self.screen, color, coords);