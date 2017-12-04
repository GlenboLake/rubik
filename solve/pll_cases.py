def cycles_to_seq(*cycles):
    """Index cases by tuples of cubes' positions.

    A cycle (1,3,5) means that cubie 1 belongs in the 3 spot, 3
    in the 5 spot, and 5 in the 1 spot. Cubie indexes are:

    0 1 2
    7   3
    6 5 4
    """
    perm = {}
    for cycle in cycles:
        perm.update({cycle[i]: cycle[(i + 1) % len(cycle)] for i in range(len(cycle))})
    seq = [perm.get(i, i) for i in range(8)]
    return tuple(seq)


cases = {
    # Solved case
    tuple(range(8)): "",

    # -- Permutations of edges only
    # H
    cycles_to_seq((1, 5), (3, 7)): "L R U2 L' R' F' B' U2 F B",
    # U: a
    cycles_to_seq((1, 7, 3)): "B2 U' L' R B2 L R' U' B2",  # Actually B2 U' M U2 M' U' B2
    # U: b
    cycles_to_seq((1, 3, 7)): "B2 U L' R B2 L R' U B2",  # Actually B2 U M U2 M' U B2
    # Z
    cycles_to_seq((1, 7), (3, 5)): "L2 R2 U F2 B2 D' F' B U2 D2 F' B",  # Actually M2' D S2 D' S' M2' S

    # -- Permutations of corners only
    # A: a
    cycles_to_seq((0, 2, 4)): "R' F R' B2 R F' R' B2 R2",
    # A: b
    cycles_to_seq((2, 6, 4)): "R B' R F2 R' B R F2 R2",
    # E
    cycles_to_seq((0, 2), (4, 6)): "B F L B' R B L' B' F' L F R' F' L'",  # (y) l L U R' D R U' R' r' F r D' L' U'

    # -- Permutations of edges and corners
    # F
    cycles_to_seq((0, 2), (3, 7)): "L B2 F' D2 B R' B' D2 F2 L' F' L B2 L'",
    # G: a
    cycles_to_seq((0, 4, 6), (1, 7, 5)): "B2 D L' U L' U' L D' B2 R' U R",  # (y2) F2' D (R' U R' U' R) D' F2 L' U L
    # G: b
    cycles_to_seq((0, 6, 4), (1, 5, 7)): "R' U' R B2 D L' U L U' L D' B2",  # R' U' R (y) R2 u (R' U R U' R) u' R2
    # G: c
    cycles_to_seq((1, 3, 5), (2, 6, 4)): "B2 D' R U' R U R' D B2 L U' L'",  # (y) R2' u' (R U' R U R') u R2 (y) R U' R'
    # G: d
    cycles_to_seq((1, 5, 3), (2, 4, 6)): "L U L' B2 D' R U' R' U R' D B2",  # (y2) R U R' (y') R2 u' (R U' R' U R') u R2
    # J: a
    cycles_to_seq((0, 6), (5, 7)): "B2 R' U' R B2 L' D L' D' L2",
    # J: b
    cycles_to_seq((2, 4), (3, 5)): "B2 L U L' B2 R D' R D R2",
    # N: a
    cycles_to_seq((2, 6), (3, 7)): "U R U' L U2 R' U L' R U' L U2 R' U L'",
    # N: b
    cycles_to_seq((0, 4), (3, 7)): "U' L' U R' U2 L U' R L' U R' U2 L U' R",
    # R: a
    cycles_to_seq((1, 3), (4, 6)): "R U2 R' U2 R B' R' U' R U R B R2 U",
    # R: b
    cycles_to_seq((0, 2), (3, 5)): "R' U2 R U2 R' F R U R' U' R' F' R2 U'",
    # T
    cycles_to_seq((0, 2), (1, 5)): "U R2 U' R2 D B2 L2 U L2 D' B2",
    # V
    cycles_to_seq((0, 4), (1, 3)): "R' U' R' U' B' R' B2 U' B' U B' R B R",
    # Y
    cycles_to_seq((0, 4), (1, 7)): "R' U' R F2 R' U R U F2 U' F2 U' F2",
}
_update = {}
for case, algo in cases.items():
    _update[tuple(map(lambda x: (x + 2) % 8, case))] = algo + ' U'
    _update[tuple(map(lambda x: (x + 4) % 8, case))] = algo + ' U2'
    _update[tuple(map(lambda x: (x + 6) % 8, case))] = algo + " U'"
cases.update(_update)
