from enum import Enum
from textwrap import dedent
from time import sleep

DEBUG = False


class Side(Enum):
    INTERIOR = ' '
    FRONT = 'F'
    BACK = 'B'
    LEFT = 'L'
    RIGHT = 'R'
    UP = 'U'
    DOWN = 'D'

    def __str__(self):
        return self.value

    @classmethod
    def from_s(cls, string):
        try:
            return [s for s in Side if s.value == string][0]
        except IndexError:
            raise ValueError(f"'{string}' is not a valid {cls.__name__}")


side_colors = {
    Side.LEFT: 'O',
    Side.RIGHT: 'R',
    Side.UP: 'W',
    Side.DOWN: 'Y',
    Side.FRONT: 'G',
    Side.BACK: 'B',
    Side.INTERIOR: 'X'
}


class Rotation(Enum):
    X = 1  # R rotation
    Y = 2  # U rotation
    Z = 3  # F rotation
    Xi = -X
    Yi = -Y
    Zi = -Z


class RubiksCube(object):
    def __init__(self):
        # Access is XYZ: (LR, UD, FB)
        self.cubies = [
            [
                [Cubie(*([Side.INTERIOR] * 6))
                 for _ in range(3)]
                for _ in range(3)]
            for _ in range(3)]
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    cubie = self.cubies[x][y][z]
                    if x == 0:
                        cubie.L = Side.LEFT
                    if x == 2:
                        cubie.R = Side.RIGHT
                    if y == 0:
                        cubie.U = Side.UP
                    if y == 2:
                        cubie.D = Side.DOWN
                    if z == 0:
                        cubie.F = Side.FRONT
                    if z == 2:
                        cubie.B = Side.BACK

    @staticmethod
    def cubie_tuple(name):
        # Validate first
        if not 1 <= len(name) <= 3:
            return None
        if not set(name) < set('LRUDFB'):
            return None
        if 'L' in name and 'R' in name:
            return None
        if 'U' in name and 'D' in name:
            return None
        if 'F' in name and 'B' in name:
            return None
        x = y = z = 1
        if 'L' in name:
            x = 0
        elif 'R' in name:
            x = 2
        if 'U' in name:
            y = 0
        elif 'D' in name:
            y = 2
        if 'F' in name:
            z = 0
        elif 'B' in name:
            z = 2
        return x, y, z

    def __getattr__(self, item):
        coords = self.cubie_tuple(item)
        if coords is None:
            return super().__getattribute__(item)
        else:
            return self.cubies[coords[0]][coords[1]][coords[2]]

    _ASCII_BASE = dedent('''\
            X X X /
          X X X / X
        X X X / X X
        X X X|X X X
        X X X|X X
        X X X|X''').replace('X', '{}')

    def ascii(self):
        """ASCII-art representation"""
        sides = [self.LUB.U, self.UB.U, self.RUB.U,
                 self.LU.U, self.U.U, self.RU.U, self.URB.R,
                 self.LUF.U, self.UF.U, self.RUF.U, self.RU.R, self.RB.R,
                 self.LUF.F, self.UF.F, self.RUF.F, self.RUF.R, self.R.R, self.RDB.R,
                 self.LF.F, self.F.F, self.RF.F, self.RF.R, self.RD.R,
                 self.LDF.F, self.DF.F, self.RDF.F, self.RDF.R]
        print(self._ASCII_BASE.format(*[side_colors[s] for s in sides]))

    def ascii_detail(self):
        for fb in range(3):
            for ud in range(3):
                for lr in range(3):
                    print(self.cubies[lr][ud][fb], end=' ')
                print()
            print()

    def rotate(self, side):
        if side == Side.LEFT:
            face = ['LUF', 'LU', 'LUB', 'LB', 'LDB', 'LD', 'LDF', 'LF']
            axis = Rotation.Xi
        elif side == Side.RIGHT:
            face = ['RUF', 'RU', 'RUB', 'RB', 'RDB', 'RD', 'RDF', 'RF']
            axis = Rotation.X
        elif side == Side.UP:
            face = ['ULB', 'UB', 'URB', 'UR', 'URF', 'UF', 'ULF', 'UL']
            axis = Rotation.Y
        elif side == Side.DOWN:
            face = ['DLB', 'DB', 'DRB', 'DR', 'DRF', 'DF', 'DLF', 'DL']
            axis = Rotation.Yi
        elif side == Side.FRONT:
            face = ['FUL', 'FU', 'FUR', 'FR', 'FDR', 'FD', 'FDL', 'FL']
            axis = Rotation.Z
        elif side == Side.BACK:
            face = ['BUL', 'BU', 'BUR', 'BR', 'BDR', 'BD', 'BDL', 'BL']
            axis = Rotation.Zi
        else:
            raise NotImplemented

        # Rotate individual cubies
        cubies = [getattr(self, cubie) for cubie in face]
        for cubie in face:
            getattr(self, cubie).rotate(axis)
        # Put cubies in their new locations
        coords = [self.cubie_tuple(cubie) for cubie in face]
        if axis.name.endswith('i'):
            coords = [coords[i - 2] for i in range(len(coords))]
        else:
            coords = [coords[i - 6] for i in range(len(coords))]
        for cubie, coord in zip(cubies, coords):
            x, y, z = coord
            self.cubies[x][y][z] = cubie

    def execute(self, algorithm):
        steps = algorithm.split()
        for s in steps:
            if DEBUG:
                print(s)
            times = 1
            if len(s) == 2:
                times = {'2': 2, "'": 3}[s[-1]]
            side = Side.from_s(s[0])
            for _ in range(times):
                self.rotate(side)
            if DEBUG:
                self.ascii()
                print()
            sleep(0.05)
            verify(self)


class Cubie(object):
    def __init__(self, front, back, left, right, up, down):
        self.id = '...'
        self.F = front
        self.B = back
        self.L = left
        self.R = right
        self.U = up
        self.D = down

    def __repr__(self):
        return f'{self.L}{self.R}{self.U}{self.D}{self.F}{self.B}'.replace(' ', '_') or 'C'

    def rotate(self, axis):
        if axis == Rotation.X:
            self.U, self.B, self.D, self.F = self.F, self.U, self.B, self.D
        elif axis == Rotation.Xi:
            for _ in range(3):
                self.rotate(Rotation.X)
        elif axis == Rotation.Y:
            self.F, self.L, self.B, self.R = self.R, self.F, self.L, self.B
        elif axis == Rotation.Yi:
            for _ in range(3):
                self.rotate(Rotation.Y)
        elif axis == Rotation.Z:
            self.U, self.L, self.D, self.R = self.L, self.D, self.R, self.U
        elif axis == Rotation.Zi:
            for _ in range(3):
                self.rotate(Rotation.Z)


def verify(cube):
    for x in range(3):
        for y in range(3):
            for z in range(3):
                cubie = cube.cubies[x][y][z]
                if x == 0:
                    assert cubie.L != Side.INTERIOR
                else:
                    assert cubie.L == Side.INTERIOR
                if x == 2:
                    assert cubie.R != Side.INTERIOR
                else:
                    assert cubie.R == Side.INTERIOR
                if y == 0:
                    assert cubie.U != Side.INTERIOR
                else:
                    assert cubie.U == Side.INTERIOR;
                if y == 2:
                    assert cubie.D != Side.INTERIOR
                else:
                    assert cubie.D == Side.INTERIOR;
                if z == 0:
                    assert cubie.F != Side.INTERIOR
                else:
                    assert cubie.F == Side.INTERIOR;
                if z == 2:
                    assert cubie.B != Side.INTERIOR
                else:
                    assert cubie.B == Side.INTERIOR;


if __name__ == '__main__':
    for side in Side:
        cube = RubiksCube()
        cube.execute(side.value)
        # cube.execute("R U B' R B R2 U' R' F R F'")
        # cube.execute("R D B L B' R U' F L2 B2 L U' R' F L D2 R2 D' B' R D' R D F' U")

        # cube.ascii_detail()
