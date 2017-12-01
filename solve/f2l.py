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
        pairs = ((Side.L, Side.F), (Side.R, Side.F), (Side.L, Side.B), (Side.R, Side.B))
        for pair in pairs:
            edge, corner = sorted(filter(lambda cubie: set(pair) <= set(cubie.faces.values()), self.cube.cubies),
                                  key=lambda cubie: len(cubie.faces))
            yield _F2LPair(edge, corner)

    def solve(self):
        # print(self.cube.cubies)
        solution = []
        skips = 1
        while skips:
            skips = 0
            for pair in self._get_pairs():
                pair_solution = get_case_solution(pair)
                if pair_solution is None:
                    skips += 1
                else:
                    self.cube.do(pair_solution)
                    solution.extend(pair_solution)
        return solution


if __name__ == '__main__':
    def make_cube():
        from solve import simplify_algorithm
        from cube import Rotation

        scramble = [Rotation(step) for step in "R2 U R U' B U' L F' L' D2".split()]
        cross_solve = [Rotation(step) for step in "D' B2 D' F B".split()]
        setup = simplify_algorithm(scramble + cross_solve)

        print('Scrambling:', ' '.join(map(str, setup)))
        return Cube(setup)


    my_cube = make_cube()
    f2l_solution = F2LSolver(my_cube).solve()
    print(' '.join(str(step) for step in f2l_solution))
    my_cube.do(f2l_solution)
    my_cube.ascii()
