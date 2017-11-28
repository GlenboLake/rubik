from collections import namedtuple

from cube import Cube, Side
from solve.f2l_cases import get_case_solution

_F2LPair = namedtuple('_F2LPair', 'edge,corner')


class F2LSolver(object):
    def __init__(self, cube):
        self.cube = cube.copy()
        corners = {c for c in self.cube.cubies if len(c.faces) == 3 and Side.D in c.faces.values()}
        edges = {c for c in self.cube.cubies if
                 len(c.faces) == 2 and Side.D not in c.faces.values() and Side.U not in c.faces.values()}
        self.cube.cubies = corners | edges

    def _get_pairs(self):
        edges = filter(lambda cubie: len(cubie.faces) == 2, self.cube.cubies)
        pairs = {_F2LPair(edge, next(
            filter(lambda cubie: set(edge.faces.values()) < set(cubie.faces.values()), self.cube.cubies))) for edge in
                 edges}
        for pair in pairs:
            yield pair

    def solve(self):
        # print(self.cube.cubies)
        solution = []
        for pair in self._get_pairs(): # Fix this.
            pair_solution = get_case_solution(pair)
            self.cube.do(pair_solution)
            solution.extend(pair_solution)
        return solution


if __name__ == '__main__':
    scramble = "F' U' B2 U2 L2 D' B L' U B L2 D B L F' R' B' R' F2 D F' R D' L2 U'"
    cross_solve = "B D R' D' B' R2 L2"

    algo = "L U L'"

    Cube(algo).ascii()
    print(algo)
    solution = F2LSolver(Cube(algo)).solve()
    print(' '.join(str(step) for step in solution))

    algo = "B U B'"

    Cube(algo).ascii()
    print(algo)
    solution = F2LSolver(Cube(algo)).solve()
    print(' '.join(str(step) for step in solution))

    print("Expect R U' R:\n      ", ' '.join(str(step) for step in F2LSolver(Cube("R U R'")).solve()))
    print("Expect R U' R' U R U' R' U2 R U' R':\n      ",
          ' '.join(str(step) for step in F2LSolver(Cube("R U R' U2 R U R' U' R U R'")).solve()))
