from dealer import *
from deck import *
from player import *


def main():
    deck = Deck(6, 0.75)
    player = Optimal_Player(1000)
    dealer = Dealer(deck, [player])

    dealer.play_round()


if __name__ == '__main__':
    main()
