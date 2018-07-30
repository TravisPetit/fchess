white = 1
black = -1
colors = {white, black}

def init_sets():
    init_squares_set()
    init_pieces_set()
    init_moves_set()
    init_squarevalues_set()
    init_opposite_colors_set()

def init_squares_set():
    """ {1, ... ,8} x {1, ... ,8} """
    global squares
    squares = set()
    for i in range(1,9):
        for j in range(1,9):
            squares.add((i,j))

def init_pieces_set():
    """ colors x {K, Q, R, B, N, P} """
    global pieces
    pieces = set()
    for c in colors:
        for p in {"K", "Q", "R", "B", "N", "P"}:
            pieces.add((c,p))

def init_moves_set():
    """ {(o,d) in squares x squares : o != d} """
    global moves
    square_cartesian_product = set()
    for a in squares:
        for b in squares:
            square_cartesian_product.add((a,b))
        moves = {(sq1, sq2) for (sq1, sq2) in square_cartesian_product if sq1 != sq2}

def init_squarevalues_set():
    """ pieces U {empty} """
    global squarevalues
    squarevalues = pieces.copy()
    squarevalues.add("empty")

def init_opposite_colors_set():
    """ {((c1,x1),(c2,x2)) in pieces x pieces : c1 != c2} """
    global opposite_colors
    piecesXpieces = set()
    for p in pieces:
        for q in pieces:
            piecesXpieces.add((p,q))
    opposite_colors = {((c1, x1), (c2, x2)) for ((c1, x1),(c2,x2)) in piecesXpieces if c1 != c2}

def print_sets():
    print("squares:\n", squares)
    print("pieces:\n", pieces)
    print("moves:\n", moves)
    print("squarevalues:\n", squarevalues)
    print("colors:\n", colors)
    print("opposite_colors:\n", opposite_colors)

init_sets()
#print_sets()
