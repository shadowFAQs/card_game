import random

class Board(object):
    """docstring for Board"""
    def __init__(self, player_deck):
        super(Board, self).__init__()
        self.player_deck = player_deck
        self.zone_names = ["Player's Library", "Player's Hand", "Player's Field", "Player's Discard", "Opponent's Library", "Opponent's Hand", "Opponent's Field", "Opponent's Discard"]

        self.setup_zones()
        self.shuffle(self.player_deck)

        print(self.player_deck[0].short_name)

    def draw(self, source=None, destination=None):
        if not source:
            source = self.player_library

        if not destination:
            destination = self.player_hand

        destination['cards'].append(source['cards'].pop(0))

        print(f'Moved {destination["cards"][-1].short_name} from {source["name"]} to {destination["name"]}.')

    def setup_zones(self):
        index = 0

        self.player_library = {
            'cards': self.player_deck,
            'index': index,
            'name': self.zone_names[index]
        }

        index += 1
        self.player_hand = {
            'cards': [],
            'index': index,
            'name': self.zone_names[index]
        }

        index += 1
        self.player_field = {
            'cards': [],
            'index': index,
            'name': self.zone_names[index]
        }

        index += 1
        self.player_discard = {
            'cards': [],
            'index': index,
            'name': self.zone_names[index]
        }

        index += 1
        self.oppo_library = {
            'cards': [],
            'index': index,
            'name': self.zone_names[index]
        }

        index += 1
        self.oppo_hand = {
            'cards': [],
            'index': index,
            'name': self.zone_names[index]
        }

        index += 1
        self.oppo_field = {
            'cards': [],
            'index': index,
            'name': self.zone_names[index]
        }

        index += 1
        self.oppo_discard = {
            'cards': [],
            'index': index,
            'name': self.zone_names[index]
        }

    def shuffle(self, deck):
        random.shuffle(deck)
