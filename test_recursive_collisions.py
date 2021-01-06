import random

class Card(object):
    def __init__(self, label, col, row):
        super(Card, self).__init__()
        self.col = col
        self.knockback = 0
        self.label = label
        self.row = row
        self.travel_dir = None

def choose_neighbor_dir(seed):
    if seed == 'north':
        return random.choice(['northwest', 'northeast'])
    elif seed == 'east':
        return random.choice(['northeast', 'southeast'])
    elif seed == 'south':
        return random.choice(['southwest', 'southeast'])
    elif seed == 'west':
        return random.choice(['northwest', 'southwest'])
    elif seed == 'northwest':
        return random.choice(['west', 'north'])
    elif seed == 'northeast':
        return random.choice(['east', 'north'])
    elif seed == 'southwest':
        return random.choice(['west', 'south'])
    elif seed == 'southeast':
        return random.choice(['east', 'south'])

def get_dest(col, row, direction):
    if direction == 'north':
        return (col, row - 1)
    elif direction == 'east':
        return (col + 1, row)
    elif direction == 'south':
        return (col, row + 1)
    elif direction == 'west':
        return (col - 1, row)
    elif direction == 'northwest':
        return (col - 1, row - 1)
    elif direction == 'northeast':
        return (col + 1, row - 1)
    elif direction == 'southwest':
        return (col - 1, row + 1)
    elif direction == 'southeast':
        return (col + 1, row + 1)

def print_status(cards):
    for card in cards:
        print(f'{card.label} ({card.col}, {card.row}) -- KB {card.knockback}, travel_dir {card.travel_dir}')

def update_positions(cards, kb_cards):
    for card in kb_cards:
        while card.knockback:
            print(f'{card.label} at ({card.col}, {card.row}) is travelling {card.travel_dir}; KB = {card.knockback}')
            card.knockback -= 1
            # Get position of next tile card would move to
            dest_pos = get_dest(card.col, card.row, card.travel_dir)
            print(f'Card would move to {dest_pos}')
            # Check if any cards occupy that spot
            collided = [c for c in cards if (c.col, c.row) == dest_pos]
            if collided:
                collided = collided[0]
                print(f'{card.label} would collide with {collided.label} @ {dest_pos}')
                collided.knockback = 5
                collided.travel_dir = choose_neighbor_dir(card.travel_dir)
                print(f'{collided.label} was knocked to the {collided.travel_dir}')
                kb_cards.insert(0, collided)
                update_positions(cards, kb_cards)
            else:
                print(f'Destination {dest_pos} is free; {card.label} moves to {dest_pos}; KB = {card.knockback}')
                card.col = dest_pos[0]
                card.row = dest_pos[1]
    print('All cards have reached their destinations')

def main():
    cards = [
        Card('P0', 0, 3),
        Card('E1', 1, 3),
        Card('E2', 3, 3),
        Card('E3', 4, 2),
        Card('E4', 4, 4)]

    print_status(cards)

    # P0 attacks E1
    cards[1].travel_dir = 'east'
    cards[1].knockback = 5

    kb_cards = [c for c in cards if c.knockback]
    update_positions(cards, kb_cards)
    print_status(cards)

if __name__ == '__main__':
    main()
