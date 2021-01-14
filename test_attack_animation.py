import math
import pygame

class Card(object):
    """docstring for Card"""
    def __init__(self, position):
        super(Card, self).__init__()
        self.animating = False
        self.center = (position[0] - 25, position[1] - 25)
        self.dims = (50, 50)
        self.direction = 0
        self.ease_frame = 0
        self.ease_frames_max = 40
        self.ease_start = self.center
        self.ease_steps = []
        self.surf = pygame.Surface(self.dims)
        self.x_origin = position[0]
        self.y_origin = position[1]
        self.x_target = 0
        self.y_target = 0
        self.x = position[0]
        self.y = position[1]

        self.surf.fill(pygame.Color('#444444')) # 2px border
        pygame.draw.rect(self.surf, pygame.Color('#777799'), pygame.Rect((2, 2), (46, 46)))

    def update(self):
        if self.animating:
            if not self.ease_steps:
                x_diff = self.x_target - self.ease_start[0]
                y_diff = self.y_target - self.ease_start[1]
                dist = math.sqrt(x_diff ** 2 + y_diff ** 2)
                self.ease_steps = set_static_ease_steps()

            self.ease_frame += 1
            if self.ease_frame == self.ease_frames_max:
                self.animating = False
                self.ease_frame = 0
                self.ease_steps = []
                self.x = self.x_origin
                self.y = self.y_origin
            else:
                ease_value = self.ease_steps[self.ease_frame]
                self.x = self.x + (math.cos(self.direction)) * ease_value
                self.y = self.y - (math.sin(self.direction)) * ease_value
                self.center = (self.x - 25, self.y - 25)

def attack(card, pos):
    x_diff = pos[0] - card.x
    y_diff = pos[1] - card.y
    angle = get_angle(x_diff, y_diff)
    card.direction = math.radians(angle)
    card.x_target = pos[0]
    card.y_target = pos[1]
    card.ease_start = (card.x, card.y)
    card.animating = True

def get_angle(dx, dy):
    return math.degrees(math.atan2(dy * -1, dx))

def set_ease_steps(delta, frames):
    # Create exponential ease
    ease = [delta * (2 ** (10 * (t / frames - 1))) for t in range(1, frames + 1)]
    # Translate steps so that total sum = delta
    div = sum(ease) / delta
    ease = [v / div for v in ease]
    if ease_type == 'out':
        ease.reverse()

    return ease

def set_static_ease_steps():
    return [-0.02, -0.08, -0.16, -0.32, -0.64, -1.28, -0.64, -0.32, -0.16, -0.08, 0.02, 0.03, 0.04, 0.06, 0.08, 0.11, 0.16, 0.23, 0.32, 0.46, 0.65, 0.92, 1.3, 1.83, 2.59, 3.66, 5.18, 7.83, 10.87, 17.36, -14.66, -10.37, -7.33, -5.18, -3.66, -2.59, -1.83, -1.3, -0.92, -0.65, -0.46, -0.32, -0.23, -0.16, -0.11, -0.08, -0.06, -0.04, -0.03, -0.02]

def main():
    dims = (500, 500)
    pygame.init()
    window_surface = pygame.display.set_mode(dims)
    clock = pygame.time.Clock()

    background = pygame.Surface(dims)
    background.fill(pygame.Color('#222222'))
    card = Card(position=(200, 250))

    is_running = True

    while is_running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                attack(card, pygame.mouse.get_pos())

        card.update()

        window_surface.blit(background, (0, 0))
        window_surface.blit(card.surf, card.center)
        pygame.display.update()

if __name__ == '__main__':
    main()
