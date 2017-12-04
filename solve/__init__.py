from cube import Rotation, Cube


def rotate_algorithm(algorithm, count):
    """Rotate an algorithm about the Y axis"""
    mapping = {'R': 'F', 'F': 'L', 'L': 'B', 'B': 'R', 'U': 'U', 'D': 'D'}

    def map_rotation(rotation):
        new_base = mapping[rotation.name[0]]
        name = new_base + rotation.name[1:]
        return Rotation(name)

    for _ in range(count):
        algorithm = [map_rotation(step) for step in algorithm]
    return algorithm


def _combine_rotations(r1, r2):
    if isinstance(r1, str):
        r1 = Rotation(r1)
    if isinstance(r2, str):
        r2 = Rotation(r2)
    if r1.face != r2.face:
        raise ValueError("Cannot combine rotations from different faces")
    base_seq = Rotation(r1.face.name).seq
    seq = {k: r2.seq[v] for k, v in r1.seq.items()}
    count_seq = {k: k for k in seq}
    quarter_turns = 0
    while count_seq != seq:
        count_seq = {k: base_seq[v] for k, v in count_seq.items()}
        quarter_turns += 1
    if quarter_turns == 0:
        return Rotation(None)
    modifier = {
        1: '', 2: '2', 3: "'"
    }[quarter_turns]
    rot = Rotation(r1)
    rot.seq = seq
    rot.name = rot.name[0] + modifier
    return rot


def algorithm_to_str(algorithm):
    return ' '.join(step.name for step in algorithm)


def simplify_algorithm(algorithm):
    """Remove repeated or reverse turns"""
    if not algorithm:
        return algorithm
    simple = [algorithm[0]]
    for step in algorithm[1:]:
        if simple[-1].face == step.face:
            simple[-1] = _combine_rotations(simple[-1], step)
        else:
            simple.append(step)
    return [s for s in simple if s]


def solve(cube):
    from solve.cross import CrossSolver
    from solve.f2l import F2LSolver
    from solve.oll import OLLSolver
    from solve.pll import PLLSolver

    cross = CrossSolver(cube).solve()
    cube.do(cross)
    print('Found cross solution:', algorithm_to_str(cross))

    f2l = F2LSolver(cube).solve()
    cube.do(f2l)
    print('Found F2L solution:', algorithm_to_str(f2l))

    oll = OLLSolver(cube).solve()
    cube.do(oll)
    print('Found OLL solution:', algorithm_to_str(oll))

    pll = PLLSolver(cube).solve()
    cube.do(pll)
    print('Found PLL solution:', algorithm_to_str(pll))


if __name__ == '__main__':
    scramble = "L' U' R' D R F' R F2 L U"
    print('Scrambling:', scramble)

    cube = Cube(scramble)
    solve(cube)
    cube.ascii()
