import pygame

class Tile(object):
    def __init__(self, row, col, y_offset=False):
        super(Tile, self).__init__()
        self.dims = (70, 70)
        offset = self.dims[1] / 2 if y_offset else 0
        self.row = row
        self.col = col
        self.x = self.dims[0] * col + col + 1
        self.y = self.dims[1] * row + row + 1 + offset
        self.surf = pygame.Surface(self.dims)

        # 1px border
        self.surf.fill(pygame.Color('#b54848'))
        pygame.draw.rect(self.surf, pygame.Color('#6f3333'), pygame.Rect((1, 1), (68, 68)))
