import random
import pygame

from card import Card
from tile import Tile

def advance_kb_round(cards, kb_animation_event, current_kb_round):
    print(f'Looking for cards with KB round {current_kb_round}...')
    for card in [c for c in cards if c.knockback_round == current_kb_round]:
        print(f'Turning on animation for {card.label}')
        card.animating = True
        card.knockback_round = 0
    pygame.time.set_timer(kb_animation_event, 500, True)
    return current_kb_round + 1

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
    damage = 15
    target.damage += damage
    target.knockback = calculate_kb(
        target.damage, damage, target.weight, attacker.power)
    target.travel_dir = ''.join([d for d in [y_dir, x_dir] if d])

    print(f'{attacker.label}\'s attack deals {damage} damage and knocks {target.label} back {target.knockback} tiles to the {target.travel_dir}')

def calculate_kb(p, d, w, b):
    """
    Returns number of tiles target will be knocked back

    p = target's post-attack damage    (0 - 9,999)
    d = damage dealt by attack         (0 - 9,999)
    w = target's weight                   (1 - 10)
    b = attacker's base power             (1 - 10)
    """
    return int((((p / 20 + p * b * 0.7 + 1 / d) * 5 / w)) / 100)

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

def reset_cards(cards):
    print('Resetting cards to original configuration')
    cards[1].place((3, 2))
    cards[2].place((5, 3))
    cards[3].place((6, 3))
    cards[4].place((6, 4))

    for card in cards:
        card.damage = 0
        card.travel_dir = None

def update_positions(cards, kb_cards, round=1):
    for card in kb_cards:
        while card.knockback:
            print(f'{card.label} at {card.position} is travelling {card.travel_dir}; KB = {card.knockback}')
            card.knockback -= 1
            if not card.knockback_round:
                card.knockback_round = round
                print(f'Set knockback_round for {card.label} to {round}')
            # Get position of next tile card would move to
            dest_pos = get_dest(card.position, card.travel_dir)
            print(f'Card would move to {dest_pos} (KB round {round})')
            # Check if any cards occupy that spot
            collided = [c for c in cards if c.position == dest_pos]
            if collided:
                collided = collided[0]
                print(f'{card.label} would collide with {collided.label} @ {dest_pos}')
                # Collision's power depends on the weight and knockback
                # values of the card knocked back
                wt_ratio = card.weight / collided.weight
                power = card.knockback * wt_ratio
                # TODO: How much dmg does this deal?
                damage = 10
                collided.damage += damage
                collided.knockback = calculate_kb(
        collided.damage, damage, collided.weight, power)
                collided.travel_dir = choose_neighbor_dir(card.travel_dir)
                collided.knockback_round = card.knockback_round + 1
                print(f'{collided.label} will be knocked back {collided.knockback} tiles to the {collided.travel_dir} (KB round {collided.knockback_round})')
                kb_cards.insert(0, collided)
                update_positions(cards, kb_cards, collided.knockback_round)
            else:
                print(f'Destination {dest_pos} is free; {card.label} moves to {dest_pos}; KB = {card.knockback}')
                card.set_target(dest_pos)

def main():
    dims = (711, 711)
    pygame.init()
    pygame.display.set_caption('Cunégonde in Hell')
    window_surface = pygame.display.set_mode(dims)

    clock = pygame.time.Clock()
    fps = 0
    input_paused = False

    background = pygame.Surface(dims)
    background.fill(pygame.Color('#222222'))
    grid = create_grid()
    current_kb_round = 1
    kb_animation_event = pygame.USEREVENT+ 1

    player_card = Card(label='P', weight=3, power=5)
    player_card.place((2, 2))

    enemy_card_1 = Card(label='E1', weight=1, power=1, owner='opponent')
    enemy_card_2 = Card(label='E2', weight=1, power=1, owner='opponent')
    enemy_card_3 = Card(label='E3', weight=1, power=1, owner='opponent')
    enemy_card_4 = Card(label='E4', weight=1, power=1, owner='opponent')
    enemy_card_1.place((3, 2))
    enemy_card_2.place((5, 3))
    enemy_card_3.place((6, 3))
    enemy_card_4.place((6, 4))
    cards = [player_card, enemy_card_1, enemy_card_2, enemy_card_3, enemy_card_4]

    is_running = True

    while is_running:
        clock.tick(60)
        fps = clock.get_fps()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                attack(attacker=player_card, target=enemy_card_1)
            elif event.type == pygame.MOUSEBUTTONUP:
                reset_cards(cards)
            elif event.type == kb_animation_event:
                if current_kb_round <= max([c.knockback_round for c in cards]):
                    current_kb_round = advance_kb_round(cards, kb_animation_event, current_kb_round)
                else:
                    current_kb_round = 1

        # Update card positions every frame
        update_positions(cards, [c for c in cards if c.knockback])

        # Step through rounds of travelling cards and animate
        if input_paused:
            if not [c for c in cards if c.animating or c.knockback_round]:
                input_paused = False
                print('Input unpaused')
        else:
            if max([c.knockback_round for c in cards]):
                input_paused = True
                print('Input paused')
                current_kb_round = advance_kb_round(cards, kb_animation_event, current_kb_round)

        for card in cards:
            card.animate()

        window_surface.blit(background, (0, 0))
        for tile in grid:
            window_surface.blit(tile.surf, (tile.x, tile.y))
        for card in cards:
            window_surface.blit(card.surf, (card.x, card.y))

        pygame.display.update()

if __name__ == '__main__':
    main()

"""

TODO

    Create wall tiles
    Handle wall collisions

"""
