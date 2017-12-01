cases = {
    # -- OLL-C subgroup (all edges correct)
    # S (Sune)
    (1, 0, 1, 0, 1, 0, 0, 0): "R U R' U R U2 R'",
    # -S (Antisune)
    (2, 0, 2, 0, 0, 0, 2, 0): "L' U' L U L' U2 ",
    # H (Double Sune)
    (2, 0, 1, 0, 2, 0, 1, 0): "R U R' U R U' R' U R U2 R'",
    # Pi (Bruno/Wheel)
    (2, 0, 2, 0, 1, 0, 1, 0): "R U2 R2 U' R2 U' R2 U2 R",
    # U (Headlights)
    (1, 0, 2, 0, 0, 0, 0, 0): "R2 D' R U2 R' D R U2 R",
    # T (Chameleon/Shark/Hammerhead)
    (1, 0, 0, 0, 0, 0, 2, 0): "L F R' F' L' F R F'",
    # L (Bowtie/Triple-Sune)
    (0, 0, 2, 0, 0, 0, 1, 0): "R' F' L' F R F' L F",

    # -- No edges flipped correctly
    # Runway
    (2, 1, 1, 1, 2, 1, 1, 1): "R U2 R2 F R F' U2 R' F R F'",
    # Zamboni
    (2, 1, 2, 1, 1, 1, 1, 1): "F R U R' U' F' B U L U' L' B'",  # Actually F R U R' U' F' f R U R' U' f'
    # Anti-Nazi/Anti-mouse
    (1, 1, 1, 1, 0, 1, 1, 1): "B U L U' L' B' U' F R U R' U' F'",  # Actually f (R U R' U') f' U' F (R U R' U') F'
    # Nazi/mouse
    (2, 1, 0, 1, 2, 1, 2, 1): "B U L U' L' B' U F R U R' U' F'",  # Actually f (R U R' U') f' U F (R U R' U') F'
    # Slash
    (0, 1, 2, 1, 0, 1, 1, 1): "R U R' U R' F R F' U2 R' F R F'",
    # Crown
    (2, 1, 0, 1, 0, 1, 1, 1): "R B U B' U R' U2 R' F R F'",  # Actually (y) F R U R' d R' U2 R' F R F'
    # Bunny
    (0, 1, 0, 1, 2, 1, 1, 1): "L' R B R B R' B' L R2 F R F'",  # Actually r' R U R U R' U' r R2' F R F'

    # -- "P" Shapes
    # Couch
    (0, 1, 2, 1, 1, 0, 0, 0): "L' U' B U L U' L' B' L",
    # Anti-Couch
    (1, 1, 0, 0, 0, 0, 2, 1): "R U B' U' R' U R B R'",
    # P
    (2, 1, 0, 0, 0, 0, 1, 1): "B U L U' L' B'",
    # Anti-P
    (0, 1, 1, 1, 2, 0, 0, 0): "B' U' R' U R B",

    # -- "W" Shapes
    # Wario
    (0, 1, 1, 1, 0, 0, 2, 0): "R' U' R U' R' U R U R B' R' B",
    # Mario
    (2, 1, 0, 0, 1, 0, 0, 1): "L U L' U L U' L' U' L' B L B'",

    # -- "L" Shapes
    # Breakneck
    (2, 0, 2, 1, 1, 1, 1, 0): "F R U R' U' R U R' U' F'",
    # Anti-Breakneck
    (1, 0, 1, 0, 2, 1, 2, 1): "F' L' U' L U L' U' L U F",
    # Frying Pan
    (2, 0, 1, 1, 2, 1, 1, 0): "R' F' L F' L' F L F' L' F2 R",  # Actually l' U' L U' L' U L U' L' U2 l
    # Anti-Frying Pan
    (2, 0, 1, 0, 2, 1, 1, 1): "L F R' F R F' R' F R F2 L'",  # Actually r U R' U R U' R' U R U2 r'
    # Right Back Squeezy
    (1, 1, 1, 1, 2, 0, 2, 0): "R B' R2 F R2 B R2 F' R",
    # Right Front Squeezy
    (2, 1, 2, 0, 1, 0, 1, 1): "R B' R B R2 U2 F R' F' R",

    # -- "C" Shapes
    # City (C and T)
    (2, 1, 1, 0, 0, 1, 0, 0): "R U R' U' B' R' F R F' B",
    # Seein' Headlights (C and headlights)
    (0, 0, 1, 1, 2, 0, 0, 1): "R' U' R' F R F' U R",

    # -- "T" Shapes
    # T (Suit up)
    (2, 1, 0, 0, 0, 1, 1, 0): "F R U R' U' F",
    # Key/Tying Shoelaces
    (1, 1, 0, 0, 0, 1, 2, 0): "R U R' U' R' F R F'",

    # -- "I" Shapes
    # Highway
    (2, 0, 1, 1, 2, 0, 1, 1): "R U2 R2 U' R U' R' U2 F R F'",
    # Streetlights
    (2, 1, 1, 0, 2, 1, 1, 0): "L F L' U R U' R' U R U' R' L F' L'",
    # Bottlecap
    (1, 1, 1, 0, 2, 1, 2, 0): "F U R U' R' U R U' R' F'",
    # Rice cooker
    (1, 0, 1, 1, 2, 0, 2, 1): "R' U' R U' R' U F' U F R",

    # -- Square shapes
    # Right Back Wide Antisune
    (1, 1, 1, 0, 0, 0, 1, 1): "L' B2 R B R' B L",  # Actually (r' U2) (R U R' U r)
    # Right Front Wide Antisune
    (2, 0, 0, 0, 2, 1, 2, 1): "L F2 R' F' R F' L'",  # Actually r U2 R' U' R U' r'

    # -- Big lightning bolt shapes
    # Fung
    (1, 1, 0, 0, 2, 1, 0, 0): "L F' L' U' L U F U' L'",
    # Anti-Fung
    (0, 1, 2, 0, 0, 1, 1, 0): "R' F R U R' U' F' U R",

    # -- Small lightning bolt shapes
    # Lightning/Wide Sune
    (1, 0, 1, 1, 1, 1, 0, 0): "L F R' F R F2 L'",
    # Reverse Lightning/Left Wide Sune
    (2, 0, 2, 0, 0, 1, 2, 1): "R' F' L F' L' F2 R",
    # Downstairs
    (0, 1, 1, 1, 1, 0, 1, 0): "F R B' R B' D B D' B R2 F'",  # Actually (y) r U R' U R' F R F' R U2 r'
    # Upstairs
    (2, 1, 0, 0, 2, 0, 2, 1): "F R U R' U' F' U F R U R' U' F'",

    # -- Fish shapes
    # Kite
    (2, 0, 2, 0, 2, 1, 0, 1): "F' U' F L F' L' U L F L'",  # Actually (y') R' U' R y r U' r' U r U r'
    # Anti-Kite
    (1, 0, 1, 1, 0, 1, 1, 0): "F U F' R' F R U' R' F' R",  # Actually (y') R U R' y R' F R U' R' F' R
    # Fish Salad
    (0, 1, 1, 0, 0, 0, 2, 1): "R U2 R2 F R F' R U2 R'",
    # Mounted Fish
    (1, 1, 0, 1, 2, 0, 0, 0): "R B' R' B U B U' B'",

    # -- Knight move shapes
    # Gun/Trigger
    (1, 1, 1, 0, 1, 1, 0, 0): "F U R U2 R' U' R U R' F'",
    # Anti-Gun/Anti-Trigger
    (2, 1, 2, 0, 0, 1, 2, 0): "R' F R U R' F' R F U' F'",  # Actually R' F R U R' F' R y' R U' R'
    # Squeegee
    (1, 1, 1, 0, 0, 1, 1, 0): "L' B' L R' U' R U L' B L",  # Actually r' U' r R' U' R U r' U r
    # Anti-Squeegee
    (2, 1, 2, 0, 2, 1, 0, 0): "R B R' L U L' U' R B' R'",

    # -- Awkward shapes
    # Spotted Chameleon
    (0, 1, 0, 1, 2, 0, 1, 0): "L2 U' L B L' U L2 U' L' B' L",  # Actually r2 D' r U r' D r2 U' r' U' r
    # Anti-Spotted Chameleon
    (0, 1, 0, 0, 2, 0, 1, 1): "R2 U R' B' R U' R2 U R B R'",
    # Awkward Fish
    (0, 1, 0, 0, 1, 0, 2, 1): "R U' R' U2 R U B U' B' U' R'",  # Actually R U' R' U2 R U y R U' R' y' U' R'
    # Lefty Awkward Fish
    (0, 1, 0, 1, 1, 0, 2, 0): "L' U L U2 L' U' B' U B U L",

    # -- All Corners Oriented
    # Fish
    (0, 0, 0, 1, 0, 1, 0, 0): "L F R' F' L' R U R U' R'",  # Actually r U R' U' r' R U R U' R'
    # H
    (0, 1, 0, 0, 0, 1, 0, 0): "R U R' U' R' L F R F' L'",  # Actually R U R' U' M' U R U' r'
    # X (Checkers)
    (0, 1, 0, 1, 0, 1, 0, 1): "L R F U2 L2 U2 L2 U2 L2 F' R' L'"
}
