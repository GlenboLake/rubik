from cube import Rotation, Side


def rotate_algorithm(algorithm, count):
    """Rotate an algorithm about the Y axis"""
    map = {'R': 'F', 'F': 'L', 'L': 'B', 'B': 'R', 'U': 'U', 'D': 'D'}

    def map_rotation(rotation):
        new_base = map[rotation.name[0]]
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


if __name__ == '__main__':
    print("R + R2 =", _combine_rotations('R', 'R2'))
    print("R + R' =", _combine_rotations('R', "R'"))

    print("L U' L'?", ' '.join(r.name for r in rotate_algorithm([Rotation(step) for step in "R U' R'".split()], 2)))
    print("B U B?", ' '.join(r.name for r in rotate_algorithm([Rotation(step) for step in "R U R".split()], 1)))
