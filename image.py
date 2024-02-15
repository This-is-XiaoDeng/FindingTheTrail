from PIL import Image, ImageDraw

from const import *


BLOCKS = {
    NULL: Image.open("images/stone_bricks.png"),
    WALL: Image.open("images/bricks.png"),
    START: Image.open("images/iron_block.png"),
    TERMINAL: Image.open("images/diamond_block.png"),
    SPECIAL: Image.open("images/piston_top.png")
}

def generate(game_map: list[list[int]]) -> None:
    image = Image.new("RGB", (len(game_map[0]) * 16, len(game_map) * 16), (51,255,255))
    draw = ImageDraw.Draw(image)
    for row in range(len(game_map)):
        for column in range(len(game_map[row])):
            item = game_map[row][column]
            x0 = column * 16
            y0 = row * 16
            # x1 = column * 16 + 16
            # y1 = row * 16 + 16
            # s = [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
            image.paste(BLOCKS[item], (x0, y0))
    image.save("1.png")