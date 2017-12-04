"""Solving OLL involves nothing more than the placement of the U faces of the 8 cubies on the U face."""
from time import sleep

from cube import Side, Cube, Rotation
from solve import simplify_algorithm
from solve.oll_cases import cases


class OLLSolver(object):
    """Solver for OLL step"""

    def __init__(self, cube):
        # Verify cube is at F2L cube state
        f2l_cubies = filter(lambda c: Side.U not in c.faces.values(), cube.cubies)
        f2l_cubies = list(f2l_cubies)
        if not all(all(k == v for k, v in cubie.faces.items()) for cubie in f2l_cubies):
            raise ValueError('Cube is not at F2L state')
        self.cube = cube

    def solve(self):
        # Get list of how many clockwise twists/flips each cubie needs, starting with LUB and working clockwise
        u_cycle = Rotation('U').seq
        cubies = [self.cube['U' + loc] for loc in ('LB', 'B', 'RB', 'R', 'RF', 'F', 'LF', 'L')]

        def count_rotations(cubie):
            u_loc = {v: k for k, v in cubie.faces.items()}[Side.U]
            if u_loc == Side.U:
                return 0
            elif u_cycle[u_loc] in cubie.faces:
                return 2
            else:
                return 1

        states = tuple(count_rotations(c) for c in cubies)
        prefix = ''
        while states not in cases:
            prefix += 'U '
            states = tuple(states[-2:]+states[:-2])
        return simplify_algorithm([Rotation(step) for step in (prefix+cases[states]).split()])


if __name__ == '__main__':
    # from solve.cross import CrossSolver
    # from solve.f2l import F2LSolver

    scramble = "F' U' B2 U2 L2 D' B L' U B L2 D B L F' R' B' R' F2 D F' R D' L2 U'"

    my_cube = Cube(scramble)
    my_cube.ascii()

    # cross_solve = CrossSolver(my_cube).solve()
    cross_solve = "B2 L2 D R' D' B' R"
    my_cube.do(cross_solve)
    # print('Cross solved:', ' '.join(r.name for r in cross_solve))
    # my_cube.ascii()

    # f2l_solve = F2LSolver(cube).solve()
    f2l_solve = "L' U' L U2 R U2 R2 F R F' U' B' U B U2 B' U' B B U' B' U' R' U R"
    my_cube.do(f2l_solve)
    # print('F2L solved', ' '.join(r.name for r in f2l_solve))
    print('Post-F2L:')
    my_cube.ascii()

    sleep(1)

    print('Full prep:', ' '.join(s.name for s in simplify_algorithm(
        [Rotation(s) for s in scramble.split()] +
        [Rotation(s) for s in cross_solve.split()] +
        [Rotation(s) for s in f2l_solve.split()]
    )))

    oll_solve = OLLSolver(my_cube).solve()
    my_cube.do(oll_solve)
    print('OLL solved', oll_solve)
    my_cube.ascii()
