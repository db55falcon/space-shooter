from pygame.image import load  # we will use this module to load a file
from pathlib import Path  # we will use the module to define our file path
from pygame.math import Vector2  # we need to use Vector Math on our Wrap_position Method


def load_sprite(name, with_alpha=True):  # this method deals with the loading of sprites
    filename = Path(__file__).parent / Path("assets/sprites/" + name + ".png")  # (__file__) parameter is a constant
    # that resolves to the name of the source file or in this case utils.py, the.parent method resolves to the
    # directory that utils.py lives in, the portion after the slash is then combined.

    sprite = load(filename.resolve())  # we call the resolve method on the created filename and pass it into the
    # pygame image load method that returns the loaded sprite
    if with_alpha:  # this checks to see if we want to use the alpha transparency method, to deal with rectangular
        # images and make them transparent in the proper ways.
        return sprite.convert_alpha()
    return sprite.convert()  # if alpha method not needed (like for a background) we can use this faster convert method
# both returns convert into a format that pygame can use


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()  # finds the width and height of the surface being drawn on
    return Vector2(x % w, y % h)

