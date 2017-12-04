from collections import namedtuple
from itertools import permutations

from cube import Cube, Side
from solve import simplify_algorithm
from solve.f2l_cases import get_case_solution

_F2LPair = namedtuple('_F2LPair', 'edge,corner')


class F2LSolver(object):
    _slots = ((Side.L, Side.F), (Side.R, Side.F), (Side.L, Side.B), (Side.R, Side.B))

    def __init__(self, cube):
        self.cube = cube.copy()
        corners = {c for c in self.cube.cubies if len(c.faces) == 3 and Side.D in c.faces.values()}
        edges = {c for c in self.cube.cubies if
                 len(c.faces) == 2 and Side.D not in c.faces.values() and Side.U not in c.faces.values()}
        self.cube.cubies = corners | edges

    def _unsolved_slots(self):
        return {frozenset(pair.edge.faces.values()) for pair in self._get_pairs() if get_case_solution(pair) != []}

    def _get_pairs(self, cube=None, slots=None):
        if cube is None:
            cube = self.cube
        for pair in slots or self._slots:
            edge, corner = sorted(filter(lambda cubie: set(pair) <= set(cubie.faces.values()), cube.cubies),
                                  key=lambda cubie: len(cubie.faces))
            yield _F2LPair(edge, corner)

    def solve(self):
        unsolved = self._unsolved_slots()
        if not unsolved:
            return []
        best_seq, best_htm = None, 100  # Worst case scenario is actually ~HTM11 for each pair, so we'll never see 100
        for order in permutations(unsolved):
            cube = self.cube.copy()
            solution = []
            for pair in self._get_pairs(cube, order):
                pair_solution = get_case_solution(pair)
                if pair_solution is None:
                    solution = []
                    break
                cube.do(pair_solution)
                solution.extend(pair_solution)
            solution = simplify_algorithm(solution)
            if solution and len(solution) < best_htm:
                best_seq, best_htm = solution, len(solution)
        return best_seq


if __name__ == '__main__':
    def make_cube():
        from solve import simplify_algorithm
        from cube import Rotation

        scramble = [Rotation(step) for step in "R2 U R U' B U' L F' L' D2".split()]
        cross_solve = [Rotation(step) for step in "D' B2 D' F B".split()]
        setup = simplify_algorithm(scramble + cross_solve)

        print('Scrambling:', ' '.join(map(str, setup)))
        return Cube(setup)


    solution = F2LSolver(make_cube()).solve()
    print(' '.join(s.name for s in solution))
