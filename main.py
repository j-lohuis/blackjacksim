from dealer import *
from deck import *
from player import *


def main():
    deck = Deck(6, 0.75)
    player = Card_Counter(1000, 6)
    dealer = Dealer(deck, [player])

    dealer.play(100000)

    print(f"Total winnings: {player.budget-1000}")


if __name__ == '__main__':
    main()
