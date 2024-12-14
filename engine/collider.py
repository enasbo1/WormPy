import backwork.direction as direct
import backwork.jarvis as jarvis
import backwork.contact as contact
from engine.pygio import PygIO


class Box:
    def __init__(self, x, y):
        self.type = 'point';
        self._coords = (x, y);
        self._relative_coords = (x, y);

    def box(self, ref:tuple[float, float] = (0 ,0)):
        n = direct.change_ref(ref[0], ref[1], (self._coords,))[0];
        return [self.type, n[0], n[1]];

    def move_to(self, position:tuple[float, float])->None:
        self._coords = direct.change_ref(position[0], position[1], (self._relative_coords,));

    def hit(self, element,  move:tuple[float, float] = (0,0))->bool|tuple[float, float]:
        return False;

    def draw(self, pygIO:PygIO, color:str = "#000000", position:tuple[float,float]=None)->None:
        if position is None:
            pygIO.draw_cross(self._coords, 10, color);
        else:
            pygIO.draw_cross(direct.change_ref(position[0], position[1], (self._relative_coords,))[0], 10, color);


class CircleBox(Box):
    def __init__(self, x, y, r):
        self.type = 'circle';
        self._coords:tuple[float, float] = (x, y);
        self.relative_coords:tuple[float, float] = (x, y);
        self.r = r;

    def box(self, ref:tuple[float, float] = (0 ,0))->tuple:
        n = direct.change_ref(ref[0], ref[1], (self._coords,))[0];
        return self.type, n[0], n[1], self.r

    def draw(self, pygIO:PygIO, color:str = "#000000",position:tuple[float,float]=None)->None:
        if position is None:
            pygIO.draw_circle(self._coords[0], self._coords[1], self.r, color);
        else:
            pygIO.draw_circle(self._relative_coords[0]+position[0], self._relative_coords[1]+position[1], self.r, color);


    def hit(self, element:Box,  move:tuple[float, float] = (0,0))->bool|tuple[float, float]:
        if element.type == 'point':
            p0 = element._coords;
            p1 = direct.sum_vectors(p0, move)
            n = contact.seg_in_circle(self._coords+(self.r,), p0, p1)
            if n is None:
                return False;
            pi = direct.sum_vectors(p0, direct.multiply_vector(direct.vector(p0,p1), n));
            return direct.vector(self._coords, pi);

        if element.type == 'circle':
            if direct.norme2(direct.vector(self._coords, element._coords)) < ((element.r+self.r)**2):
                return direct.vector(self._coords, element._coords);
            return False;
        if element.type == 'poly':
            circle = self._coords+(self.r,)
            for i in range(len(element._coords)):
                if contact.seg_in_circle(circle , element._coords[i], element._coords[(i+1)%len(element._coords)]):
                    return direct.rotate(direct.vector(element._coords[(i + 1) % len(element._coords)], element._coords[i]));
            return False;

    def _out(self, p:tuple[float, float], move:tuple[float, float]):
        p0 = p;
        p1 = direct.sum_vectors(p0, move)
        n = contact.outBorderIn(self._coords+(self.r,), p0, p1)
        if n == 1:
            return direct.vector(direct.moy_vector(p0, p1), self._coords);
        else:
            return 1*(n==2)

    def out(self, element:Box, move:tuple[float, float] = (0,0))->int|tuple[float, float]:
        if element.type == 'point':
            return self._out(element._coords, move)

        if element.type == 'circle':
            vect = direct.vector(element._coords, self._coords)
            dist2 = direct.norme2(vect);
            if dist2>(self.r + element.r)**2:
                return 0;
            if dist2>(self.r-element.r)**2:
                return 1;
            return vect

        if element.type == 'poly':
            h = 2
            for i in range(len(element._coords)):
                n = self._out(element._coords[i], move);
                if (n!=0) & (n!=1):
                    return n;
                if h!=2:
                    if h!=n:
                        return direct.vector(direct.moy_vector(
                            direct.moy_vector(
                                element[i-1],
                                direct.sum_vectors(element[i-1], move)
                            ),
                            direct.moy_vector(
                                element[i],
                                direct.sum_vectors(element[i], move)
                            )
                        ), self._coords)
                h=n


class PolygonBox(Box):
    def __init__(self, coords: tuple[tuple[float, float]]):
        self.type = 'poly';
        self._coords:tuple[tuple[float, float]] = coords;
        self._relative_coords:tuple[tuple[float, float]] = coords;
        self.contour = jarvis.jarvis(coords);
        self._relative_contour = jarvis.jarvis(coords);

    def move_to(self, position:tuple[float, float])->None:
        self._coords = direct.change_ref(position[0], position[1], self._relative_coords);
        self.contour = direct.change_ref(position[0], position[1], self._relative_contour);

    def set_change(self, coords: tuple[tuple[float, float]]):
        self._coords = coords;
        self.contour = jarvis.jarvis(coords);

    def draw(self, pygIO:PygIO, color:str = "#000000", position:tuple[float, float] = None)->None:
        if position is None:
            pygIO.draw_poly(self._coords, color);
        else:
            pygIO.draw_poly(direct.change_ref(position[0], position[1], self._relative_coords), color);


    def box(self, ref:tuple[float, float] = (0 ,0)):
        n = direct.change_ref(ref[0], ref[1], self._coords);
        return [self.type]+[i for i in n]

    def hit(self, element:Box,  move:tuple[float, float] = (0,0))->bool|tuple[float, float]:
        if element.type == 'point':
            p0 = element._coords;
            p1 = direct.sum_vectors(p0, move);
            for i in range(len(self._coords)):
                if contact.cross(p0, p1 , self._coords[i], self._coords[(i+1)%len(self._coords)]) is not None:
                    return direct.rotate(direct.vector(self._coords[i], self._coords[(i+1) % len(self._coords)]));
            return False;

        if element.type == 'circle':
            circle = (element._coords[0], element._coords[1], element.r);
            for i in range(len(self._coords)):
                if contact.seg_in_circle(circle , self._coords[i], self._coords[(i + 1) % len(self._coords)]) is not None:
                    return direct.rotate(direct.vector(self._coords[i], self._coords[(i + 1) % len(self._coords)]));
            return False;

        if element.type == 'poly':
            for p0 in element._coords:
                p1 = direct.sum_vectors(move, p0);
                for i in range(len(self._coords)):
                    if contact.cross(p0, p1 , self._coords[i], self._coords[(i+1)%len(self._coords)]) is not None:
                        return direct.rotate(direct.vector(self._coords[i], self._coords[(i+1) % len(self._coords)]));
            for p0 in self._coords:
                p1 = direct.vector(move, p0);
                for i in range(len(element._coords)):
                    if contact.cross(p0, p1 , element._coords[i], element._coords[(i+1)%len(element._coords)]) is not None:
                        return direct.rotate(direct.vector(element._coords[(i+1) % len(element._coords)], element._coords[i]));
            return False;


class Collider:
    def __init__(self, worker, global_box: Box|None, box_holes: list[CircleBox] = list(), active=True):
        self.global_box:Box = global_box
        self.box_holes = box_holes
        self.worker = worker
        self._active = active
        if active:
            worker.activeCollider.append(self)

    def move_to(self, position:tuple[float, float] = (0, 0)):
        self.global_box.move_to(position);
        for i in self.box_holes:
            i.move_to(position);


    def get_collision(self, box:Box, move:tuple[float, float] = (0,0))->None|tuple[float, float]:
        n = self.global_box.hit(box, move=move);
        if n:
            for hole in self.box_holes:
                h = hole.out(box, move=move);
                if h==1:
                    return None;
                if h!=0:
                    return direct.unit_vect(h);
            return direct.unit_vect(n);
        return None;

    def set_hole(self, hole:CircleBox):
        if hole.hit(self.global_box):
            self.box_holes.append(hole);

    def show_collider(self, pygIO:PygIO, color:str = "#000000", background_color:str = None, position:tuple[float,float]=None):
        if background_color is None:
            background_color = pygIO.screen_color;
        if self.global_box is not None:
            self.global_box.draw(pygIO, color, position);
            for i in self.box_holes:
                i.draw(pygIO, background_color, position);


    def set_active(self):
        if not self._active:
            self._active = True
            self.worker.activeCollider.append(self);

    def set_unActive(self):
        if self._active:
            self._active = False
            self.worker.activeCollider.remove(self);