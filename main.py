import engine.worker as worker;
import script.wormGame as wg;

god = worker.Worker(wg.WormGame());
god.start();

while god.pygIO.running:
    god.mainLoop();

god.end()