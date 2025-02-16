from engine.physicsBody import LinearForceField
from script.explosiveObject import ExplosiveObject


class Grenade(ExplosiveObject):
    def onInit(self):
        self.physicBody.forces.append(LinearForceField((0,100)));