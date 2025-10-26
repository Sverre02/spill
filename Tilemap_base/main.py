"""A base for games using a singular simple tilmap"""
import pygame as p
from pathlib import Path
import json
import sys
class Tile:
    """A parent class for elements of tilmaps"""
    def __init__(self, x, y):
        self.rect = p.rect.Rect(x, y, 32, 32)
        self.wall = False
class Ground(Tile):
    """A type of Tile"""
    def __init__(self, x, y):
        super().__init__(x,y)
        self.color = (131, 131, 131)
        self.wall = False
        
        
class Wall(Tile):
    """A type of tile, attributes: solid"""
    def __init__(self, x, y):
        super().__init__(x,y)
        self.color = (50, 50, 50)
        self.wall = True
        
def init():
    if tilemap_path.exists():
        content = tilemap_path.read_text()
        json_tilemap = json.loads(content)
        tilemap = json_python_converter(json_tilemap)
        
    else:
        tilemap = [[Tile(x * 32, y * 32) for y in range(18)] for x in range(32)]
    return tilemap

def json_python_converter(json_tilemap):
    tilemap = []
    row_number = 0
    for json_tilerow in json_tilemap:
        tile_row = []
        tile_number = 0
        for json_tile in json_tilerow:
            if json_tile == "w":
                tile_row.append(Wall(row_number * 32, tile_number * 32))
            else:
                tile_row.append(Ground(row_number * 32, tile_number * 32))
            tile_number += 1
        tilemap.append(tile_row)
        row_number += 1
    return tilemap
def python_json_converter(tilemap):
    """Converts a normal tilemap(using classes) into a list only including strings"""
    json_tilemap = []
    for tilerow in tilemap:
        json_tilerow = []
        for tile in tilerow:
            if isinstance(tile, Wall):
                json_tilerow.append("w")
            else:
                json_tilerow.append("g")
        json_tilemap.append(json_tilerow)
    return json_tilemap
TILE_SIZE = 32
screen = p.display.set_mode((32 * TILE_SIZE, 18 * TILE_SIZE))#Defines screen the numbers getting multiplied with TILE_SIZE is the amount of tile in each row
clock = p.time.Clock()


tilemap_path = Path('tilemap.json')
tilemap = init()
edit = True#change manually
edit_class = Wall#painted class in edit mode, change manually
running = True
while running:
    dt = clock.tick(60)/1000
    screen.fill((0, 0, 0))
    keys = p.key.get_pressed()
    position = p.mouse.get_pos()
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        if event.type == p.MOUSEBUTTONDOWN:
            if edit:
                for row in tilemap:
                    for tile in row:
                         if tile.rect.collidepoint(position):
                            x_index = int(tile.rect.x / TILE_SIZE)
                            y_index = int(tile.rect.y / TILE_SIZE)
                            if tile.rect.collidepoint(position):
                                if event.button == 1:
                                    tilemap[x_index][y_index] = edit_class(tile.rect.x, tile.rect.y)
                                if event.button == 3:
                                    tilemap[x_index][y_index] = Ground(tile.rect.x, tile.rect.y)

        if event.type == p.KEYDOWN:
            if edit:
                if keys[p.K_LCTRL] and event.key == p.K_s:
                    contents = json.dumps(python_json_converter(tilemap))
                    tilemap_path.write_text(contents)
                    print("Saved")
    for row in tilemap:
        for tile in row:
            p.draw.rect(screen, tile.color, tile.rect)
    p.display.update()
sys.exit()
p.quit()