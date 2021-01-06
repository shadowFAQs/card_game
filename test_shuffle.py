from card import Card
from gameboard import Board

def main():
    kinds = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Spade', 'Club', 'Diamond', 'Heart']
    deck = []
    for n in range(len(suits)):
        for i in range(len(kinds)):
            deck.append(Card(kind=kinds[i], suit=suits[n]))
    print(f'Deck complete: {len(deck)} cards')

    board = Board(player_deck=deck)

    while len(board.player_hand['cards']) < 7:
        print(f'Hand: [{", ".join([c.short_name for c in board.player_hand["cards"]])}]')
        input('Hit ENTER to draw: ')
        board.draw()

if __name__ == '__main__':
    main()
