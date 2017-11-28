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
    def make_cube():
        from solve import simplify_algorithm
        from cube import Rotation

        scramble = [Rotation(step) for step in "R2 U R U' B U' L F' L' D2".split()]
        cross_solve = [Rotation(step) for step in "D' B2 D' F B".split()]
        setup = simplify_algorithm(scramble + cross_solve)

        print('Scrambling:', ' '.join(map(str, setup)))
        return Cube(setup)


    cube = make_cube()
    solution = F2LSolver(cube).solve()
    print(' '.join(str(step) for step in solution))
    cube.do(solution)
    cube.ascii()
