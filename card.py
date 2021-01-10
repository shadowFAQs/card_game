import math
import pygame

class Card(object):
    def __init__(self, label, weight, power, owner='player'):
        super(Card, self).__init__()
        self.airborne = False
        self.animating = False
        self.damage = 0
        self.dims = (50, 50)
        self.knockback = 0
        self.knockback_round = 0
        self.label = label # Display text
        self.owner = owner
        self.position = (0, 0) # (col, row)
        self.power = power
        self.surf = pygame.Surface(self.dims)
        self.travel_dir = None
        self.weight = weight
        self.x = 0 # Global x pos
        self.y = 0 # Global y pos
        self.x_target = 0 # Target x pos for animation
        self.y_target = 0 # Target y pos for animation

        # 2px border
        self.surf.fill(pygame.Color('#222222'))
        color = pygame.Color('#777799') if self.owner == 'player' else pygame.Color('#997777')
        pygame.draw.rect(self.surf, color, pygame.Rect((2, 2), (46, 46)))

        # Write label
        font = pygame.font.SysFont('Consolas', 24)
        label = font.render(self.label, True, pygame.Color('#000000'))
        offset_x = int((self.dims[0] - label.get_size()[0]) / 2) # Center X
        offset_y = int((self.dims[1] - label.get_size()[1]) / 2) # Center Y
        self.surf.blit(label, dest=(offset_x, offset_y))

    def animate(self):
        if self.animating:
            x_diff = self.x_target - self.x
            y_diff = self.y_target - self.y
            if x_diff > 0:
                self.x += math.ceil(abs(x_diff / 5))
            elif x_diff < 0:
                self.x -= math.ceil(abs(x_diff / 5))
            if y_diff > 0:
                self.y += math.ceil(abs(y_diff / 5))
            elif y_diff < 0:
                self.y -= math.ceil(abs(y_diff / 5))

            if not x_diff and not y_diff:
                print(f'(x, y) dest reached for {self.label}; turning off "animating" prop')
                self.animating = False

    def place(self, pos):
        """Set card on a given (col, row) tile"""
        board_offset = 1
        tile_size = 70
        card_offset_x = int((tile_size - self.dims[0]) / 2)
        card_offset_y = int((tile_size - self.dims[1]) / 2)
        if pos[0] % 2:
            card_offset_y += tile_size / 2
        self.position = pos
        self.x = board_offset + pos[0] * tile_size + pos[0] + card_offset_x
        self.y = board_offset + pos[1] * tile_size + pos[1] + card_offset_y
        self.x_target = self.x
        self.y_target = self.y

    def set_target(self, pos):
        """Set target for animation"""
        board_offset = 1
        tile_size = 70
        card_offset_x = int((tile_size - self.dims[0]) / 2)
        card_offset_y = int((tile_size - self.dims[1]) / 2)
        if pos[0] % 2:
            card_offset_y += tile_size / 2
        self.position = pos
        self.x_target = board_offset + pos[0] * tile_size + pos[0] + card_offset_x
        self.y_target = board_offset + pos[1] * tile_size + pos[1] + card_offset_y
