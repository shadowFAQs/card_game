import random
import pygame

from card import Card
from tile import Tile

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
    target.animating = True

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

def set_collision_events(cards, kb_cards, collisions):
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
                # Collision's power depends on the weight and knockback
                # values of the card knocked back
                wt_ratio = card.weight / collided.weight
                power = card.knockback * wt_ratio
                damage = 10 # TODO: How much dmg does this deal?
                collided.damage += damage
                collided.knockback = calculate_kb(
                    collided.damage, damage, collided.weight, power)
                if collided.knockback:
                    collided.travel_dir = choose_neighbor_dir(card.travel_dir)
                    print(f'{collided.label} will be knocked back {collided.knockback} tiles to the {collided.travel_dir}')
                    kb_cards.insert(0, collided)
                else:
                    card.knockback = 0
                    print(f'{collided.label} has stopped {card.label}\'s knockback')
                # Create collision event
                event = {
                    'collider': card,
                    'collided': collided,
                    'position': dest_pos
                }
                collisions.append(event)
                set_collision_events(cards, kb_cards, collisions)
            else:
                print(f'Destination {dest_pos} is free; {card.label} moves to {dest_pos}; KB = {card.knockback}')
                card.set_target(dest_pos)
        return collisions

def update_collision_events(collisions):
    revised = []
    for event in collisions:
        collider = event['collider']
        collided = event['collided']
        if collider.surf.get_rect(topleft=(collider.x, collider.y)).colliderect(collided.surf.get_rect(topleft=(collided.x, collided.y))):
            print(f'{event["collider"].label} has collided with {event["collided"].label} @ ({event["collider"].x}, {event["collider"].x}); turning on animation for {event["collided"].label}')
            event['collided'].animating = True
        else:
            revised.append(event)

    return revised

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

    player_card = Card(label='P', weight=3, power=15)
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

    print(player_card.x, player_card.y)
    print(enemy_card_1.x, enemy_card_1.y)

    collisions = []

    is_running = True

    while is_running:
        clock.tick(60)
        fps = clock.get_fps()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                attack(attacker=player_card, target=enemy_card_1)
                collisions = set_collision_events(
                    cards, [c for c in cards if c.knockback], collisions)
            elif event.type == pygame.MOUSEBUTTONUP:
                reset_cards(cards)

        # Animate collisions every frame
        if collisions:
            collisions = update_collision_events(collisions)

        # Pause input if cards are animating
        if input_paused:
            if not [c for c in cards if c.animating]:
                # All cards finished with animation
                input_paused = False
                print('Input unpaused')
        else:
            if [c for c in cards if c.animating]:
                input_paused = True
                print('Input paused')

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

    Change KB round delay so that cards start animating when they're hit
    Create wall tiles
    Handle wall collisions
    Add potential to "pop up" from collision instead of being knocked back

New animation/knockback system

Calculate all KBs and destinations up front, but don't switch on animation for each tile until the one that hits them arrives.

collision event
    collider
    collided

    if sprite collision occurs between collider and collided:
        collided.animating = True

"""
