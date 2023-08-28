import matplotlib.pyplot as plt
from dealer import *
from deck import *
from player import *


def main():
    deck = Deck(6, 0.75)
    players = [
        # Optimal_Player(1000000),
        Card_Counter("Hi-Lo", 1000000, 6, STRAT_HI_LO),
        Card_Counter("Hi-Opt I", 1000000, 6, STRAT_HI_OPTI),
        Card_Counter("Hi-Opt II", 1000000, 6, STRAT_HI_OPTII),
        # Card_Counter("KO", 1000000, 6, STRAT_KO),
        Card_Counter("Omega II", 1000000, 6, STRAT_OMEGAII),
        Card_Counter("Zen Count", 1000000, 6, STRAT_ZEN_COUNT),
        # Card_Counter("10 Count", 1000000, 6, STRAT_10_COUNT),
        # RandomPlayer(1000000),
        # AveragePlayer(1000000),
    ]
    dealer = Dealer(deck, players)

    statistics = dealer.play(1000000)

    for i, player_budget in enumerate(statistics):
        plt.plot(player_budget, marker='', linestyle='-', label=f'{players[i].name}')

    plt.xlabel('Rounds Played')
    plt.ylabel('Player Budget')
    plt.title('Player Budget over Rounds')
    plt.legend()
    plt.grid(True)

    plt.savefig('plot.png')

if __name__ == '__main__':
    main()
