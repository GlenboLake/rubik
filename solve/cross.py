from textwrap import dedent

from cube import Cube, Side, Rotation


def print_cross(cube):
    cross = dedent("""\
      X
      X
    XXXXX
      X
      X
    """).replace('X', '{}')
    print(cross.format(*(face.name for face in
                       (cube['BD'].B, cube['BD'].D, cube['LD'].L, cube['DL'].D, cube['D'].D, cube['DR'].D, cube['DR'].R,
                        cube['DF'].D, cube['DF'].F))))


class CrossSolver(object):
    """Solver for the white cross"""

    def __init__(self, cube):
        self.cube = cube.copy()
        self.cube.cubies = {c for c in self.cube.cubies if len(c.faces) == 2 and Side.D in c.faces.values()}

    @staticmethod
    def cross_state(cube):
        """Cross state is the location of the four edge cubies. Use frozensets to make this immutable and comparable"""
        # The four cubies we need have two faces and one of them is D
        cubies = {c for c in cube.cubies if len(c.faces) == 2 and Side.D in c.faces.values()}
        # Represent each cubie as a frozenset and then return a frozenset of those.
        return frozenset(frozenset(c.faces.items()) for c in cubies)

    def successors(self, path, cube=None):
        if cube is None:
            cube = self.cube.copy()
        else:
            cube = cube.copy()
        cube.do(path)
        turns = [s.name + r for s in Side for r in ("", "2", "'")]
        if path:
            turns = [t for t in turns if t[0] != path[-1][0]]
        return {self.cross_state(cube.copy().do(turn)): path + [turn] for turn in turns}

    def solve(self):
        solved_cube = Cube()
        goals = {self.cross_state(solved_cube): []}
        for i in range(3):
            for state, path in tuple(filter(lambda kv: len(kv[1]) == i, goals.items())):
                successors = self.successors(path, solved_cube)
                goals.update({s: p for s, p in successors.items() if s not in goals})
        # Reverse algorithms in goals
        goals = {k: [Rotation(r).reverse().name for r in v[::-1]] for k, v in goals.items()}
        goals_set = set(goals)
        start_state = self.cross_state(self.cube)
        paths = new_paths = {start_state: []}
        while not (goals_set & set(new_paths)):
            next_paths = {}
            for state, path in new_paths.items():
                successors = self.successors(path)
                next_paths.update({s: p for s, p in successors.items() if s not in paths})
            paths.update(next_paths)
            new_paths = next_paths
        state = (goals_set & set(paths)).pop()
        return ' '.join(paths[state] + goals[state])


if __name__ == '__main__':
    scramble = "R2 U R U' B U' L F' L' D2"
    my_cube = Cube()
    my_cube.do(scramble)

    print(CrossSolver(my_cube).solve())
