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

        self.set_bg_color('#777799')

    def animate(self):
        if self.animating:
            min_velocity = 2
            x_diff = self.x_target - self.x
            y_diff = self.y_target - self.y
            dist = math.sqrt(x_diff ** 2 + y_diff ** 2)
            speed = max(dist / 25, min_velocity)
            rad = math.radians(self.get_angle(x_diff, y_diff))
            self.x = self.x + speed * (math.cos(rad))
            self.y = self.y - speed * (math.sin(rad))

            # Snap to destination once within 2px
            if abs(x_diff) < 2 and abs(y_diff) < 2:
                print(f'(x, y) dest reached for {self.label}; turning off "animating" prop')
                self.x = self.x_target
                self.y = self.y_target
                self.animating = False

            self.set_bg_color('#cccccc')
        else:
            self.set_bg_color('#777799')

    def get_angle(self, dx, dy):
        return math.degrees(math.atan2(dy * -1, dx))

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

    def set_bg_color(self, color):
        self.surf.fill(pygame.Color('#222222')) # 2px border
        color = pygame.Color(color)
        pygame.draw.rect(self.surf, color, pygame.Rect((2, 2), (46, 46)))

        # Write label
        font = pygame.font.SysFont('Consolas', 24)
        label = font.render(self.label, True, pygame.Color('#000000'))
        offset_x = int((self.dims[0] - label.get_size()[0]) / 2) # Center X
        offset_y = int((self.dims[1] - label.get_size()[1]) / 2) # Center Y
        self.surf.blit(label, dest=(offset_x, offset_y))

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
