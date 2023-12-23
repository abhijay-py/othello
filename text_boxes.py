import pygame

from constants import ADD_TUPLE, SUB_TUPLE, MULT_TUPLE, ADD_DIGIT, SUB_DIGIT, MULT_DIGIT
from constants import RG_LOCATION, RG_BOX, MIDMENU_LOCATION, MIDMENU_BOX, QUIT_BOX, MM_QUIT_LOCATION
from constants import TEXT_BOX_OFFSET, TEXT_BOX_CORNER, OPTION_BORDER, TEXT_BOX_GREEN

from helpers import tuple_op, write_text

#MENU HELPERS
def create_rg_box(screen, font):
    rg_top_left = tuple_op(RG_LOCATION, TEXT_BOX_OFFSET, SUB_TUPLE)
    rg_bot_right = tuple_op(rg_top_left, RG_BOX, ADD_TUPLE)
    pygame.draw.rect(screen, TEXT_BOX_GREEN, (rg_top_left, RG_BOX), border_radius = TEXT_BOX_CORNER)
    pygame.draw.rect(screen, "black", (rg_top_left, RG_BOX), border_radius = TEXT_BOX_CORNER, width = OPTION_BORDER)
    write_text("Resume Game", screen, font, "black", RG_LOCATION)

    return rg_top_left, rg_bot_right

def create_menu_box(screen, font):
    menu_tl = tuple_op(MIDMENU_LOCATION, TEXT_BOX_OFFSET, SUB_TUPLE)
    menu_br = tuple_op(menu_tl, MIDMENU_BOX, ADD_TUPLE)

    pygame.draw.rect(screen, TEXT_BOX_GREEN, (menu_tl, MIDMENU_BOX), border_radius = TEXT_BOX_CORNER)
    pygame.draw.rect(screen, "black", (menu_tl, MIDMENU_BOX), border_radius = TEXT_BOX_CORNER, width = OPTION_BORDER)
    write_text("Back to Menu", screen, font, "black", MIDMENU_LOCATION)

    return menu_tl, menu_br

def create_mm_quit(screen, font):
    quit_tl = tuple_op(MM_QUIT_LOCATION, TEXT_BOX_OFFSET, SUB_TUPLE)
    quit_br = tuple_op(quit_tl, QUIT_BOX, ADD_TUPLE)

    pygame.draw.rect(screen, TEXT_BOX_GREEN, (quit_tl, QUIT_BOX), border_radius = TEXT_BOX_CORNER)
    pygame.draw.rect(screen, "black", (quit_tl, QUIT_BOX), border_radius = TEXT_BOX_CORNER, width = OPTION_BORDER)
    write_text("Exit", screen, font, "black", MM_QUIT_LOCATION)

    return quit_tl, quit_br
