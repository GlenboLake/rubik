from cube import Side, Rotation
from solve import simplify_algorithm, rotate_algorithm


def get_case_solution(pair):
    permuter = Rotation('U')
    permuter.seq[Side.U] = Side.U
    permuter.seq[Side.D] = Side.D
    edge, corner = pair.edge.copy(), pair.corner.copy()
    if all(k == v for k, v in edge.faces.items()) and all(k == v for k, v in corner.faces.items()):
        return []
    algorithm = []

    if Side.U not in edge.faces and set(edge.faces) != set(edge.faces.values()):
        # The edge is not in the U layer, but it's also not in its own slot. Come back to this pair.
        return None
    if Side.D in corner.faces and set(corner.faces) != set(corner.faces.values()):
        # The corner is in the D layer, but it's also not in its own slot. Come back to this pair.
        return None

    # There are two types of transformation to be used. The transform rotation is the number of y turns to do in order
    # to simplify the case down to the RF edge pair, which simplifies algorithm lookup. The alignment rotation is the
    # number of U turns to prepend to the algorithm.
    transform_rotations = 0
    while not set(edge.faces.values()) == {Side.R, Side.F}:
        edge.faces = {permuter.seq[k]: permuter.seq[v] for k, v in edge.faces.items()}
        corner.faces = {permuter.seq[k]: permuter.seq[v] for k, v in corner.faces.items()}
        transform_rotations -= 1
    transform_rotations %= 4
    # How many U turns are needed to align? If the corner is in the U face, then in needs to be in the RUF position.
    # Otherwise, the edge needs to be lined up so that the side lines up (UF->RF or RU->RF)
    if Side.U in corner.faces:
        while not set(edge.faces.values()) <= set(corner.faces):
            edge.faces = {permuter.seq[k]: v for k, v in edge.faces.items()}
            corner.faces = {permuter.seq[k]: v for k, v in corner.faces.items()}
            algorithm.append(Rotation('U'))
    elif Side.U in edge.faces:
        while not any(k == v for k, v in edge.faces.items()):
            edge.faces = {permuter.seq[k2]: v2 for k2, v2 in edge.faces.items()}
            algorithm.append(Rotation('U'))

    # List the cases! 42 total. Case numbers are according to https://www.speedsolving.com/wiki/index.php/F2L
    base = ''
    if Side.D in corner.faces:  # Corner in place
        if Side.U in edge.faces:  # Edge in U layer
            if corner.D == Side.D:  # Corner oriented
                if edge.U == Side.F:
                    # Case 25
                    base = "U' R' F R F' R U R'"
                else:
                    # Case 26
                    base = "U R U' R' U' F' U F"
            elif corner.F == Side.D:  # D color on F face
                if edge.U == Side.F:
                    # Case 27
                    base = "R U' R' U R U' R'"
                else:
                    # Case 29
                    base = "F' U' F U F' U' F"
            elif corner.R == Side.D:  # D color on R face
                if edge.U == Side.F:
                    # Case 30
                    base = "R U R' U' R U R'"
                else:
                    # Case 28
                    base = "R U R' U' F R' F' R"
        else:  # Edge in place
            if all(k == v for k, v in edge.faces.items()):  # Edge solved
                if corner.D == Side.D:  # Corner is in place and oriented
                    # Case 37 (solved)
                    pass
                elif corner.F == Side.D:
                    # Case 39
                    base = "R U' R' U' R U R' U2 R U' R'"
                else:
                    # Case 40
                    base = "R U' R' U R U2 R' U R U' R'"
            else:  # Edge twisted
                if corner.D == Side.D:  # Corner in place and oriented
                    # Case 38
                    base = "R' F R F' R U' R' U R U' R' U2 R U' R'"
                elif corner.F == Side.D:
                    # Case 41
                    base = "R U' R' U F' U' F U' F' U' F"
                else:
                    # Case 42
                    base = "R U' R' U2 F' U' F U' F' U F"
    else:  # Corner in U face
        if Side.U in edge.faces:  # Edge in U layer
            if corner.F == Side.D:  # D color on F face
                if edge.U == Side.F:
                    if Side.L in edge.faces:
                        # Case 7
                        base = "U' R U2' R' U2 R U' R'"
                    elif Side.R in edge.faces:
                        # Case 1
                        base = "U R U' R'"
                    elif Side.F in edge.faces:
                        # Case 15
                        base = "R B L U' L' B' R'"
                    elif Side.B in edge.faces:
                        # Case 5
                        base = "U' R U R' U2 R U' R'"
                else:  # Edge's R color on U face
                    if Side.L in edge.faces:
                        # Case 3
                        base = "F' U' F"
                    elif Side.R in edge.faces:
                        # Case 11
                        base = "U' R U2' R' U F' U' F"
                    elif Side.F in edge.faces:
                        # Case 13
                        base = "U F' U F U' F' U' F"
                    elif Side.B in edge.faces:
                        # Case 9
                        base = "U' R U' R' U F' U' F"
            elif corner.R == Side.D:  # D color on R face
                if edge.U == Side.F:
                    if Side.L in edge.faces:
                        # Case 10
                        base = "U' R U R' U R U R'"
                    elif Side.R in edge.faces:
                        # Case 14
                        base = "U' R U' R' U R U R'"
                    elif Side.F in edge.faces:
                        # Case 12
                        base = "R U' R' U R U' R' U2 R U' R'"
                    elif Side.B in edge.faces:
                        # Case 4
                        base = "R U R'"
                else:  # Edge's R color on U face
                    if Side.L in edge.faces:
                        # Case 6
                        base = "U F' U' F U2 F' U F"
                    elif Side.R in edge.faces:
                        # Case 16
                        base = "R U' R' U2 F' U' F"
                    elif Side.F in edge.faces:
                        # Case 2
                        base = "U' F' U F"
                    else:  # Side.B
                        # Case 8
                        base = "U F' U2 F U2 F' U F"
            else:  # D color on U face
                if edge.U == Side.F:
                    if Side.L in edge.faces:
                        # Case 21
                        base = "R U' R' U2 R U R'"
                    elif Side.R in edge.faces:
                        # Case 17
                        base = "R U2 R' U' R U R'"
                    elif Side.F in edge.faces:
                        # Case 23
                        base = "U2 R2 U2 R' U' R U' R2"
                    else:  # Side.B
                        # Case 19
                        base = "U R U2 R2 F R F'"
                else:  # Edge's R color on U face
                    if Side.L in edge.faces:
                        # Case 20
                        base = "U' F' U2 F2 R' F' R"
                    elif Side.R in edge.faces:
                        # Case 24
                        base = "U F' L' U L F R U R'"
                    elif Side.F in edge.faces:
                        # Case 18
                        base = "F' U2 F U F' U' F"
                    else:  # Side.B
                        # Case 22
                        base = "F' U F U2 F' U' F"
        else:  # (Corner in U Face), Edge in place
            if all(k == v for k, v in edge.faces.items()):  # Edge solved
                if corner.U == Side.U:
                    # Case 32
                    base = "R U R' U' R U R' U' R U R'"
                elif corner.F == Side.U:
                    # Case 33
                    base = "U' R U' R' U2 R U' R'"
                else:
                    # Case 34
                    base = "U F' U F U2 F' U F"
            else:  # Edge twisted
                if corner.U == Side.U:
                    # Case 31
                    base = "R U' R' U F' U F"
                elif corner.F == Side.U:
                    # Case 35
                    base = "U' R U R' U F' U' F"
                else:
                    # Case 36
                    base = "U F' U' F U' R U R'"

    algorithm.extend([Rotation(step) for step in base.split()])

    return rotate_algorithm(simplify_algorithm(algorithm), transform_rotations)
