from cube import Side, Rotation
from solve import simplify_algorithm
from solve.pll_cases import cases


def _cubie_set(cubie):
    """Take a cubie name and convert it to a frozenset"""
    return frozenset(Side[side] if isinstance(side, str) else side for side in cubie)


_names = tuple(map(_cubie_set, ('LUB', 'UB', 'RUB', 'RU', 'RUF', 'UF', 'LUF', 'LU')))
_positions = {item: index for index, item in enumerate(_names)}


class PLLSolver(object):
    def __init__(self, cube):
        self.cube = cube

    def solve(self):
        u_cubies = set(filter(lambda cubie: Side.U in cubie.faces and len(cubie.faces) > 1, self.cube.cubies))
        positions = {
            _positions[_cubie_set(cubie.faces)]: _positions[_cubie_set(cubie.faces.values())]
            for cubie in u_cubies
        }
        positions = tuple(positions[i] for i in range(len(positions)))
        prefix = ''
        while positions not in cases:
            prefix += 'U '
            positions = tuple(positions[-2:] + positions[:-2])
            if not simplify_algorithm([Rotation(s) for s in prefix.split()]):
                raise NotImplementedError(f"Case not handled: {positions}")
        return prefix + cases[positions]


if __name__ == '__main__':
    from cube import Cube

    print(PLLSolver(Cube("R' U R U' R2 F' U' F U R F R' F' R2 U'")).solve())

    scramble = "F' U' B2 U2 L2 D' B L' U B L2 D B L F' R' B' R' F2 D F' R D' L2 U'"

    my_cube = Cube(scramble)
    print('Scramble:')
    my_cube.ascii()

    cross_solve = "B2 L2 D R' D' B' R"
    f2l_solve = "L' U' L U2 R U2 R2 F R F' U' B' U B U2 B' U' B B U' B' U' R' U R"
    oll_solve = "U R U2 R2 U' R U' R' U2 F R F'"

    my_cube.do(cross_solve)
    my_cube.do(f2l_solve)
    my_cube.do(oll_solve)

    print('OLL:')
    my_cube.ascii()

    pll_solution = PLLSolver(my_cube).solve()
    print('PLL Solved:', pll_solution)
    my_cube.do(pll_solution)
    my_cube.ascii()
