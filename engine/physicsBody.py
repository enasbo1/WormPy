def stop_movement(physicsBody, collisionVector:tuple[float, float]):
    physicsBody.movement[0] = 0;
    physicsBody.movement[1] = 0;
    physicsBody.velocity[0] = 0;
    physicsBody.velocity[1] = 0;

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


class PhysicsBody:
    def __init__(self, master, onCollide = stop_movement, forces:list[Force]=[LinearForceField((0,18))]):
        self.master = master
        self.worker = master.worker;
        self.worker.activePBList.append(self);
        self.position:list[float, float] = [0., 0.]
        self.movement = [0., 0.]
        self.velocity = [0., 0.]
        self.forces:list = forces;
        self.on_collide = onCollide

    def instantPush(self, move:tuple[float, float]):
        self.movement[0] += move[0]
        self.movement[1] += move[1]

    def addSpeed(self, move:tuple[float, float]):
        self.velocity[0] += move[0]
        self.velocity[1] += move[1]

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

        if self.master.collider is None:
            self._move();
        else:
            for i in self.worker.activeCollider:
                if i!=self.master.collider:
                    col = i.get_collision(self.master.collider.global_box, move=tuple(self.movement))
                    if col is not None:
                        self.on_collide(self, col);
            self._move();
