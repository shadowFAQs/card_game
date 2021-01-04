import random

class Card(object):
    """docstring for Card"""
    def __init__(self, kind, suit, zone=0, owner='player', controller='player'):
        super(Card, self).__init__()
        self.controller = controller
        self.counters = []
        self.owner = owner
        self.kind = kind # Like 'A' or '5'
        self.suit = suit
        self.zone = zone

        self.kind_name = self.get_kind()
        self.full_name = self.get_full_name()
        self.short_name = self.kind + self.suit[0]
        self.value = self.get_value()

    def add_counter(self, counter):
        # Add a single counter
        if isinstance(counter, str):
            self.counters.append(counter)
        # Add a list of counters
        else:
            self.counters += counter

    def clear_counters(self):
        # Remove all counters
        self.counters = []

    def get_full_name(self):
        return f'{self.kind} of {self.suit}s'

    def get_kind(self):
        if self.kind == 'A':
            return 'Ace'
        elif self.kind == 'K':
            return 'King'
        elif self.kind == 'Q':
            return 'Queen'
        elif self.kind == 'J':
            return 'Jack'
        else:
            return [None, None, 'Deuce', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten'][int(self.kind)]

    def get_value(self):
        if self.kind.isalpha():
            return 11
        else:
            return int(self.kind)

    def set_kind(self, kind):
        self.kind = kind

    def set_zone(self, zone=None):
        if zone:
            self.zone = zone
        else:
            self.zone = 0
