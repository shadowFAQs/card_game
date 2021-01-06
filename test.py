import random
import pygame

class Card(object):
    def __init__(self, label, owner='player'):
        super(Card, self).__init__()
        self.airborne = False
        self.dims = (50, 50)
        self.knockback = 0
        self.label = label
        self.owner = owner
        self.position = (0, 0) # (col, row)
        self.surf = pygame.Surface(self.dims)
        self.travel_dir = None
        self.x = 0
        self.y = 0

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

def attack(attacker, target):
    # Determine direction of knockback
    x_dir = None
    y_dir = None
    if attacker.x < target.x:
        x_dir = 'east'
    elif attacker.x < target.x:
        x_dir = 'west'
    if attacker.y < target.y:
        y_dir = 'south'
    elif attacker.y < target.y:
        y_dir = 'north'

    # Apply knockback force and direction to target
    target.knockback = 5
    target.travel_dir = ''.join([d for d in [y_dir, x_dir] if d])

    print('Attack event')

def choose_neighbor_dir(seed):
    if seed == 'north':
        return random.choice(['northwest', 'northeast'])
    elif seed == 'south':
        return random.choice(['southwest', 'southeast'])
    elif seed == 'northwest':
        return random.choice(['southwest', 'north'])
    elif seed == 'northeast':
        return random.choice(['southeast', 'north'])
    elif seed == 'southwest':
        return random.choice(['northwest', 'south'])
    elif seed == 'southeast':
        return random.choice(['northeast', 'south'])

def create_grid():
    tiles = []
    for col in range(10):
        if col % 2:
            # Even columns get 9 tiles
            for row in range(9):
                tiles.append(Tile(row, col, y_offset=True))
        else:
            # Odd columns get 10 tiles
            for row in range(10):
                tiles.append(Tile(row, col))
    return tiles

def get_dest(old_pos, direction):
    new_pos = list(old_pos)
    if 'north' in direction:
        new_pos[1] -= 1
    elif 'south' in direction:
        new_pos[1] += 1
    if 'east' in direction:
        new_pos[0] += 1
    elif 'west' in direction:
        new_pos[0] -= 1
    # For east/west travel, we have to take the differences in
    # column height into consideration.
    if 'east' in direction or 'west' in direction:
        if old_pos[0] % 2:
            if 'north' in direction:
                new_pos[1] += 1
        else:
            if 'south' in direction:
                new_pos[1] -= 1

    # Handle stage boundaries
    if new_pos[0] < 0:
        new_pos[0] = 0
        print('Ring out -- left')
    elif new_pos[0] > 9:
        new_pos[0] = 9
        print('Ring out -- right')
    if new_pos[1] < 0:
        new_pos[1] = 0
        print('Ring out -- top')
    elif new_pos[1] > 9:
        new_pos[1] = 9
        print('Ring out -- bottom')
    return tuple(new_pos)

def update_positions(cards, kb_cards):
    for card in kb_cards:
        while card.knockback:
            print(f'{card.label} at {card.position} is travelling {card.travel_dir}; KB = {card.knockback}')
            card.knockback -= 1
            # Get position of next tile card would move to
            dest_pos = get_dest(card.position, card.travel_dir)
            print(f'Card would move to {dest_pos}')
            # Check if any cards occupy that spot
            collided = [c for c in cards if c.position == dest_pos]
            if collided:
                collided = collided[0]
                print(f'{card.label} would collide with {collided.label} @ {dest_pos}')
                collided.knockback = 3
                collided.travel_dir = choose_neighbor_dir(card.travel_dir)
                print(f'{collided.label} was knocked to the {collided.travel_dir}')
                kb_cards.insert(0, collided)
                update_positions(cards, kb_cards)
            else:
                print(f'Destination {dest_pos} is free; {card.label} moves to {dest_pos}; KB = {card.knockback}')
                card.place(dest_pos)

def main():
    """
    TODO
        Create wall tiles
        Handle wall collisions
        Animate
            Separate "rounds" of knockback
    """
    dims = (711, 711)
    pygame.init()
    pygame.display.set_caption('Cunégonde in Hell')
    window_surface = pygame.display.set_mode(dims)

    clock = pygame.time.Clock()
    fps = 0

    background = pygame.Surface(dims)
    background.fill(pygame.Color('#222222'))
    grid = create_grid()

    player_card = Card(label='P')
    player_card.place((2, 2))

    enemy_card_1 = Card(label='E1', owner='opponent')
    enemy_card_2 = Card(label='E2', owner='opponent')
    enemy_card_1.place((3, 2))
    enemy_card_2.place((5, 3))
    cards = [player_card, enemy_card_1, enemy_card_2]

    is_running = True

    while is_running:
        clock.tick(60)
        fps = clock.get_fps()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                attack(attacker=player_card, target=enemy_card_1)

        moving_cards = [c for c in cards if c.knockback]
        if moving_cards:
            update_positions(cards, moving_cards)

        window_surface.blit(background, (0, 0))
        for tile in grid:
            window_surface.blit(tile.surf, (tile.x, tile.y))
        for card in cards:
            window_surface.blit(card.surf, (card.x, card.y))

        pygame.display.update()

if __name__ == '__main__':
    main()
