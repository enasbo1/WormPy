from backwork.direction import norme2, vector
from engine.collider import Collider, PolygonBox, CircleBox
from engine.physicsBody import PhysicsBody
from engine.pygio import PygIO
from engine.worker import MonoBehavior
import backwork.direction as direct


class ExplosiveObject(MonoBehavior):
    pass


class ExplosiveObject(MonoBehavior):
    skinPoints: tuple[tuple[float, float]] = ((0,10),(10,0), (0,-10),(-10,0))
    floored = False;
    explosionRadius:int;
    explosionDamage:float;

    worms:list[MonoBehavior] = [];

    def onInit(self):
        pass

    def init(self, worms:list[MonoBehavior], explosionRadius:int = 100, explosionDamage:float = 20)->ExplosiveObject:
        self.physicBody:PhysicsBody = PhysicsBody(self, onCollide = self.onCollide, forces = []);
        self.collider:Collider = Collider(self.worker, PolygonBox(self.skinPoints), active=False)
        self.worms:list[MonoBehavior] = worms
        self.explosionDamage = explosionDamage
        self.explosionRadius = explosionRadius
        self.onInit();
        return self;

    def show(self, pygIO:PygIO):
        pos = self.physicBody.get_extrapolate()
        self.collider.show_collider(pygIO, position=pos);

    def onCreate(self):
        pass

    def onCollide(self, physicsBody, coll:tuple[float, float]):
        pos = self.physicBody.get_position()
        R2  = self.explosionRadius**2
        self.worker.set_hole(CircleBox(pos[0], pos[1], self.explosionRadius))
        for i in self.worms:
            p = i.physicBody
            dir = vector(pos, p.get_position());
            n = norme2(dir)
            if 10<n<R2:
                p.addSpeed(direct.multiply_vector(dir, 10000/n))
                i.health -= self.explosionDamage;
        self.destroy();

    def fixedUpdate(self):
        self.collider.move_to(self.physicBody.get_position())