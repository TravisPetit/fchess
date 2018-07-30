import set_constants as sc
from random import choice, sample
import general_functions as gf

def dummy_position(sq):
    if sq == (3,3):
        return (sc.white, "K")
    if sq == (6,6):
        return (sc.black, "K")
    return "empty"

gf.print_board(dummy_position)
game_history = [dummy_position,]
move = choice(list(gf.valid_moves(*game_history)))

while(True):
    gf.print_board(move)
    move = choice(list(gf.valid_moves(*game_history)))
    game_history.append(move)
