from doctest import master

import backwork.direction as direct
from backwork.direction import norme2, unit_vect, fact_vect, vector


def stop_movement(physicsBody, collisionVector:tuple[float, float]):
    physicsBody.movement[0] = 0;
    physicsBody.movement[1] = 0;
    physicsBody.velocity[0] = 0;
    physicsBody.velocity[1] = 0;

def collision_slide(physicsBody, collisionVector:tuple[float, float]):
    m_correct = direct.scalar(collisionVector, physicsBody.movement);
    v_correct = direct.scalar(collisionVector, physicsBody.velocity);
    for i in (0,1):
        if m_correct>0:
            physicsBody.movement[i] -= m_correct * collisionVector[i];
        if v_correct>0:
            physicsBody.velocity[i] -= v_correct * collisionVector[i];

def collision_walk(physicsBody, collisionVector:tuple[float, float])->bool:
    floored = collisionVector[1] > 0.5;
    if floored:
        physicsBody.movement[1] = 0;
        physicsBody.velocity[1] = 0;
    collision_slide(physicsBody, collisionVector);
    return floored;



class Force:
    def __init__(self):
        pass

    def applyForce(self, body):
        pass

class LinearForceField(Force):
    def __init__(self, forceVector:tuple[float, float]):
        self.forceVector = forceVector

    def applyForce(self, body):
        body.velocity[0] += self.forceVector[0]*body.worker.deltaTime
        body.velocity[1] += self.forceVector[1]*body.worker.deltaTime


class SpeedLimitForce(Force):
    def __init__(self, value:float):
        self.value = value

    def applyForce(self, body):
        if norme2(body.velocity)>(self.value**2):
            body.setSpeed(fact_vect(unit_vect(body.velocity), self.value));

class PhysicsBody:
    def __init__(self, master, onCollide = collision_slide, forces:list[Force]=[LinearForceField((0,18))]):
        self.master = master
        self.worker = master.worker;
        self.worker.activePBList.append(self);
        self.position:list[float, float] = [0., 0.]
        self.movement = [0., 0.]
        self.velocity = [0., 0.]
        self.movement_ref:tuple(float,float) = (0., 0.);
        self.velocity_ref:tuple(float,float) = (0., 0.);
        self.forces:list = forces;
        self.on_collide = onCollide

    def instantPush(self, move:tuple[float, float]):
        self.movement[0] += move[0]
        self.movement[1] += move[1]

    def addSpeed(self, move:tuple[float, float]):
        self.velocity[0] += move[0]
        self.velocity[1] += move[1]

    def setSpeed(self, value:tuple[float, float]):
        self.velocity[0] = value[0];
        self.velocity[1] = value[1];

    def teleport(self, pos:tuple[float,float]):
        self.position[0] = pos[0];
        self.position[1] = pos[1];

    def get_position(self)->tuple[float, float]:
        return tuple(self.position)

    def get_extrapolate(self)->tuple[float, float]:
        delta = self.worker.extrapolatePhysicsDelta
        return tuple(self.position[i]+((self.movement[i]+self.velocity[i])*delta) for i in (0,1))

    def _move(self):
        self.position[0] += self.movement[0];
        self.position[1] += self.movement[1];
        self.movement[0] = 0;
        self.movement[1] = 0;

    def applyPhysicStep(self):
        for i in self.forces:
            i.applyForce(self);
        self.movement[0] += self.velocity[0]*self.worker.deltaTime;
        self.movement[1] += self.velocity[1]*self.worker.deltaTime;
        self.movement_ref = tuple(self.movement);
        self.velocity_ref = tuple(self.velocity);

        if self.master.collider is None:
            self._move();
        else:
            colider = self.master.collider
            mark = tuple();
            col = tuple()
            for i in self.worker.activeCollider:
                if i!=self.master.collider:
                    col += i.get_collision(self.master.collider.global_box, move=tuple(self.movement))
                    self.master.collider.mark += i.mark
            for j,c in enumerate(col):
                if (j==0) or (not c in col[:j-1]):
                    self.on_collide(self, c);
            self._move();
