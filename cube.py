from enum import Enum, auto
from textwrap import dedent


class Side(Enum):
    L = auto()
    R = auto()
    U = auto()
    D = auto()
    F = auto()
    B = auto()


side_colors = {
    Side.L: 'R',
    Side.R: 'O',
    Side.U: 'Y',
    Side.D: 'W',
    Side.F: 'G',
    Side.B: 'B',
}


class Cubie(object):
    def __init__(self, faces):
        # faces: Key is absolute location, value is face color there
        self.faces = {face: face for face in faces}

    def __getattr__(self, item):
        return self.faces[Side[item]]

    def __repr__(self):
        pos = ''.join(face.name for face, face_home in sorted(self.faces.items(), key=lambda pair: pair[1].value))
        home = ''.join(face.name for face in sorted(self.faces.values(), key=lambda f: f.value))
        return f'{pos} -> {home}'

    def copy(self):
        c = Cubie([])
        c.faces = {k: v for k, v in self.faces.items()}
        return c

    @staticmethod
    def is_valid(cubie_name):
        if ('L' in cubie_name and 'R' in cubie_name) or \
                ('U' in cubie_name and 'D' in cubie_name) or \
                ('F' in cubie_name and 'B' in cubie_name):
            return False
        return 1 <= len(cubie_name) <= 3 and set(cubie_name) - set("LRUDFB") == set()


class Cube(object):
    def __init__(self, scramble=None):
        self.cubies = set()
        for LR in ('L', 'R', ''):
            for UD in ('U', 'D', ''):
                for FB in ('F', 'B', ''):
                    faces = ''.join((LR, UD, FB))
                    if faces:
                        self.cubies.add(Cubie({Side[f] for f in faces}))
        if scramble:
            self.do(scramble)

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
        if isinstance(algorithm, str):
            algorithm = [Rotation(step) for step in algorithm.split()]
        for rotation in algorithm:
            if isinstance(rotation, str):
                rotation = Rotation(rotation)
            face = self.face(rotation.face)
            for cubie in face:
                cubie.faces = {rotation.seq.get(k, k): v for k, v in cubie.faces.items()}
        return self

    def copy(self):
        cube = Cube()
        cube.cubies = {c.copy() for c in self.cubies}
        return cube


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
        if name is None:
            self.name = "No-op"
            self.face = None
            self.seq = {}
        elif isinstance(name, Rotation):
            self.name = name.name
            self.face = name.face
            self.seq = name.seq
        elif isinstance(name, str):
            self.name = name
            self.face = Side[name[0]]
            seq = self.CYLCES[self.face]
            turns = 1
            if len(name) > 1:
                if name[1] == '2':
                    turns = 2
                elif name[1] == "'":
                    turns = 3
                else:
                    raise ValueError(f'{name} is not a valid rotation name')
            if len(name) > 2:
                raise ValueError(f'{name} is not a valid rotation name')
            self.seq = {seq[i]: seq[(i + turns) % 4] for i in range(4)}
            self.seq = {Side[k]: Side[v] for k, v in self.seq.items()}

    def reverse(self):
        seq = self.CYLCES[self.face]
        seq = {seq[i]: seq[(i + 1) % 4] for i in range(4)}
        seq = {Side[k]: Side[v] for k, v in seq.items()}
        base_seq = seq
        turns = 1
        while seq != self.seq:
            turns += 1
            seq = {k: base_seq[v] for k, v in seq.items()}

        suffix = {1: '', 2: '2', 3: "'"}[(-turns) % 4]
        return Rotation(self.face.name + suffix)

    def __repr__(self):
        return f"Rotation: {self.face}/{self.seq}"

    def __str__(self):
        return self.name

    def __bool__(self):
        return bool(self.face)


if __name__ == '__main__':
    cube = Cube()
    cube.do('R U')
    cube.ascii()
    print(cube['RUF'])
    rots = [Rotation(r).reverse() for r in "R' U2 U D".split()]
    print(rots)
