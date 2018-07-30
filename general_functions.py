import set_constants as sc
sc.init_sets()

def pawn_advances_two_squares(col):
    """ colors -> IP(moves) """
    if col == sc.white:
        return {((f,2),(f,4)) for f in range(1,9)}
    elif col == sc.black:
        return {((f,7),(f,5)) for f in range(1,9)}


def empty_board_moves(piece):
    """ pieces -> IP(moves) """
    if piece == "empty":
        return set()
    c = piece[0]
    x = piece[1]
    if x == "R":
        return set(filter(lambda t : t[0][0] == t[1][0] or t[0][1] == t[1][1], sc.moves))
    if x == "B":
        return set(filter(lambda t : abs(t[0][0] - t[1][0]) == abs(t[0][1] - t[1][1]), sc.moves))
    if x == "N":
        set1 = set(filter(lambda t : abs(t[0][0] - t[1][0]) == 2 and abs(t[0][1] - t[1][1]) == 1, sc.moves))
        set2 = set(filter(lambda t : abs(t[0][0] - t[1][0]) == 1 and abs(t[0][1] - t[1][1]) == 2, sc.moves))
        return set1.union(set2)
    if x == "Q":
        return empty_board_moves((c,"R")).union(empty_board_moves((c,"B")))
    if x == "K":
        return set(filter(lambda t : abs(t[0][0] - t[1][0]) <= 1 and abs(t[0][1] - t[1][1]) <= 1, sc.moves))
    if x == "P":
        return set(filter(lambda t : t[1][1] == t[0][1] + c, empty_board_moves((c,"R")))).union(pawn_advances_two_squares(c))
    print("Error on empty_board_set method")


def empty_board_attacks(piece):
    """ pieces -> IP(moves) """
    if piece == "empty":
        return set()
    c = piece[0]
    x = piece[1]
    if x == "P":
        return set(filter(lambda t : t[1][1] == t[0][1] + c, empty_board_moves((c,"B"))))
    return empty_board_moves(piece)


def initial_position(sq):
    """ squares -> squarevalues """
    #White:
    if sq == (1,1) or sq == (8,1):
        return (sc.white, "R")
    if sq == (2,1) or sq == (7,1):
        return (sc.white, "N")
    if sq == (3,1) or sq == (6,1):
        return (sc.white, "B")
    if sq == (4,1):
        return (sc.white, "Q")
    if sq == (5,1):
        return (sc.white, "K")
    if sq[1] == 2:
        return (sc.white, "P")
    #Black:
    if sq == (1,8) or sq == (8,8):
        return (sc.black, "R")
    if sq == (2,8) or sq == (7,8):
        return (sc.black, "N")
    if sq == (3,8) or sq == (6,8):
        return (sc.black, "B")
    if sq == (4,8):
        return (sc.black, "Q")
    if sq == (5,8):
        return (sc.black, "K")
    if sq[1] == 7:
        return (sc.black, "P")

    return "empty"


def print_board(pos):
    temp = ""
    for i in range (8,0,-1):
        for j in range (8,0,-1):
            if pos((j,i)) == "empty":
                temp += " --"
            else:
                if pos((j,i))[0] == sc.white:
                    temp += " w" + pos((j,i))[1]
                else:
                    temp += " b" + pos((j,i))[1]
        temp += "\n"
    print(temp)


def empty_squares(pos):
    """ position -> IP(square) """
    return set(filter(lambda s : pos(s) == "empty", sc.squares))


def do_move(pos, move):
    """ position x moves -> position """
    o = move[0]
    d = move[1]

    # pisition function, meaning p: squares -> squarevalues
    def p(square):
        if square == o:
            return "empty"
        if square == d:
            return pos(o)
        return pos(square)
    return p


def in_between(o, d):#TODO: improve, test, refactor
    """ InBetween(o,d) := {s in squares: exists lambda in (0,1) : s = lambda o + (1-lambda)d} """
    temp = set()
    o1, o2 = o[0], o[1]
    d1, d2 = d[0], d[1]

    # - line:
    if o1 == d1:
        for i in range(min(o2, d2) + 1, max(o2,d2)):
            temp.add((o1, i))

    # | line:
    elif o2 == d2:
        for i in range(min(o1, d1) + 1, max(o1,d1)):
            temp.add((i,o2))

    # / line:
    elif abs(o1 - d1) == abs(o2 - d2) and o1 >= o2 and d1 >= d2:
        x, y = min(o1, d1), min(o2, d2)
        for i in range(1, abs(o1 - d1)):
            temp.add((x + i, y + i))

    # \ line:
    elif abs(o1 - d1) == abs(o2 - d2):
        x, y = min(o1, d1), max(o2, d2)
        for i in range(1, abs(o1 - d1)):
            temp.add((x + i, y - i))

    return temp


def no_jumps(pos):
    """ position -> IP(moves) """
    return set(filter(lambda t : in_between(t[0], t[1]).issubset(empty_squares(pos)),sc.moves))


def non_captures(pos):
    """ position -> IP(moves) """
    return set(filter(lambda t : t in empty_board_moves(pos(t[0])) and pos(t[1]) == "empty", no_jumps(pos)))


def attacks(pos):
    """ position -> IP(moves) """
    return set(filter(lambda t : t in empty_board_attacks(pos(t[0])), no_jumps(pos)))


def captures(pos):
    """ position -> IP(moves) """
    def temp(t):
        return (pos(t[0]), pos(t[1])) in sc.opposite_colors
    return set(filter(temp, attacks(pos)))


def potential_moves(pos, color):
    """ position x color -> IP(moves) """
    return set(filter(lambda t : pos(t[0])[0] == color, non_captures(pos).union(captures(pos))))


def promotion(pos):
    """ position -> IP(position) """
    temp = set()
    pos_legal = True
    for piece in {"R","N","B","Q"}:
        for (f,r) in sc.squares:
            for c in sc.colors:
                if (pos((f,r)) == (c, "P") and r in {1,8}):
                    pos_legal = False
                    if c == sc.white:
                        if piece == "R":
                            def new_pos(sq):
                                if pos(sq)[1] == "P" and sq[1] == 8:
                                    return (sc.white, "R")
                                return pos(sq)
                            temp.add(new_pos)
                        elif piece == "N":
                            def new_pos(sq):
                                if pos(sq)[1] == "P" and sq[1] == 8:
                                    return (sc.white, "N")
                                return pos(sq)
                            temp.add(new_pos)
                        elif piece == "B":
                            def new_pos(sq):
                                if pos(sq)[1] == "P" and sq[1] == 8:
                                    return (sc.white, "B")
                                return pos(sq)
                            temp.add(new_pos)
                        elif piece == "Q":
                            def new_pos(sq):
                                if pos(sq)[1] == "P" and sq[1] == 8:
                                    return (sc.white, "Q")
                                return pos(sq)
                            temp.add(new_pos)

                    elif c == sc.black:
                        if piece == "R":
                            def new_pos(sq):
                                if pos(sq)[1] == "P" and sq[1] == 1:
                                    return (sc.black, "R")
                                return pos(sq)
                            temp.add(new_pos)
                        elif piece == "N":
                            def new_pos(sq):
                                if pos(sq)[1] == "P" and sq[1] == 1:
                                    return (sc.black, "N")
                                return pos(sq)
                            temp.add(new_pos)
                        elif piece == "B":
                            def new_pos(sq):
                                if pos(sq)[1] == "P" and sq[1] == 1:
                                    return (sc.black, "B")
                                return pos(sq)
                            temp.add(new_pos)
                        elif piece == "Q":
                            def new_pos(sq):
                                if pos(sq)[1] == "P" and sq[1] == 1:
                                    return (sc.black, "Q")
                                return pos(sq)
                            temp.add(new_pos)
    if pos_legal:
        temp.add(pos)
    return temp


def normal_moves(pos,col):
    temp = set()
    """ position x color -> IP(board) """
    for move in potential_moves(pos, col):
        for new_pos in promotion(do_move(pos,move)):
            temp.add(new_pos)
    return temp


def squares_attacked(pos, col):
    """ position x color -> IP(board) """
    temp = set()
    for d in sc.squares:
        for o in sc.squares:
            if pos(o)[0] == col and (o,d) in attacks(pos):
                temp.add(d)
                #print("added ",d)
    return temp


def implies(p,q):
    return not (p) or q


def cart_prod(p,q):
    temp = set()
    for a in p:
        for b in q:
            temp.add((a,b))
    return temp

#print_board(initial_position)
#print_board(do_move(initial_position,((4,2),(4,4))))
#o = (1,1)
#d = (8,8)
#print(in_between(o,d))
#print(no_jumps(initial_position))
#print(non_captures(initial_position))
#print(attacks(initial_position))
#print(captures(do_move(initial_position,((4,2),(4,6)))))
#print(potential_moves(initial_position, sc.black))
#print_board(do_move(initial_position,((4,2),(4,8))))
#for el in promotion(do_move(initial_position,((4,2),(4,8)))):
    #print_board(el)
#for el in normal_moves(do_move(initial_position,((4,2),(4,7))),sc.white):
    #print_board(el)
print(squares_attacked(initial_position, sc.white))
