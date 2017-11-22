from enum import Enum, auto
from textwrap import dedent


class Side(Enum):
    L = 1
    R = 2
    U = 4
    D = 8
    F = 16
    B = 32


side_colors = {
    Side.L: 'O',
    Side.R: 'R',
    Side.U: 'W',
    Side.D: 'Y',
    Side.F: 'G',
    Side.B: 'B',
}


# def cubie(sides_mask):
#     return ''.join(s.name for s in Side if s.value & sides_mask)


class Cubie(object):
    def __init__(self, faces):
        # faces: Key is absolute location, value is face color there
        self.faces = {face: face for face in faces}

    def __getattr__(self, item):
        return self.faces[Side[item]]

    def __repr__(self):
        return ''.join(sorted(f.name for f in self.faces.values()))

    @staticmethod
    def is_valid(cubie_name):
        if ('L' in cubie_name and 'R' in cubie_name) or \
                ('U' in cubie_name and 'D' in cubie_name) or \
                ('F' in cubie_name and 'B' in cubie_name):
            return False
        return 1 <= len(cubie_name) <= 3 and set(cubie_name) - set("LRUDFB") == set()


class Cube(object):
    def __init__(self):
        self.cubies = set()
        for LR in ('L', 'R', ''):
            for UD in ('U', 'D', ''):
                for FB in ('F', 'B', ''):
                    faces = ''.join((LR, UD, FB))
                    if faces:
                        self.cubies.add(Cubie({Side[f] for f in faces}))

    def face(self, face):
        if isinstance(face, str):
            face = Side[face]
        elif isinstance(face, int):
            face = Side(face)
        return {c for c in self.cubies if face in c.faces}

    def __getitem__(self, item):
        """Get a cubie by name"""
        if not Cubie.is_valid(item):
            raise KeyError
        return [c for c in self.cubies if set(c.faces) == set(Side[face] for face in item)][0]

    _ASCII_BASE = dedent('''\
            X X X /
          X X X / X
        X X X / X X
        X X X|X X X
        X X X|X X
        X X X|X''').replace('X', '{}')

    def ascii(self):
        """ASCII-art representation"""
        sides = [self['LUB'].U, self['UB'].U, self['RUB'].U,
                 self['LU'].U, self['U'].U, self['RU'].U, self['URB'].R,
                 self['LUF'].U, self['UF'].U, self['RUF'].U, self['RU'].R, self['RB'].R,
                 self['LUF'].F, self['UF'].F, self['RUF'].F, self['RUF'].R, self['R'].R, self['RDB'].R,
                 self['LF'].F, self['F'].F, self['RF'].F, self['RF'].R, self['RD'].R,
                 self['LDF'].F, self['DF'].F, self['RDF'].F, self['RDF'].R]
        print(self._ASCII_BASE.format(*[side_colors[s] for s in sides]))

    def do(self, algorithm):
        algorithm = [Rotation(step) for step in algorithm.split()]
        for rotation in algorithm:
            face = self.face(rotation.face)
            for cubie in face:
                cubie.faces = {rotation.seq.get(k, k): v for k, v in cubie.faces.items()}


class Rotation(object):
    CYLCES = {
        Side.L: 'FDBU',
        Side.R: 'FUBD',
        Side.U: 'FLBR',
        Side.D: 'FRBL',
        Side.F: 'URDL',
        Side.B: 'ULDR'
    }

    def __init__(self, name):
        if isinstance(name, Rotation):
            self.face = name.face
            self.seq = name.seq
        elif isinstance(name, str):
            self.face = Side[name[0]]
            seq = self.CYLCES[self.face]
            turns = 1
            if len(name) > 1:
                if name[1] == '2':
                    turns = 2
                elif name[1] == "'":
                    turns = 3
            self.seq = {seq[i]: seq[(i + turns) % 4] for i in range(4)}
            self.seq = {Side[k]: Side[v] for k, v in self.seq.items()}

    def __repr__(self):
        return f"Rotation: {self.face}/{self.seq}"


if __name__ == '__main__':
    cube = Cube()
    cube.ascii()
    cube.do("L R F' B' U2 D2")
    cube.ascii()
