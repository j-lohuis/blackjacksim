import matplotlib.pyplot as plt
import numpy as np
import random
from dealer import *
from deck import *
from player import *


def play_alone():
    deck = Deck(6, 0.75)
    dealer = Dealer(deck, [CLI_Player(1000)])

    dealer.play(10000)


def simulate(players, rounds, output_file):
    deck = Deck(6, 0.75)
    dealer = Dealer(deck, players)

    statistics = dealer.play(rounds)

    for i, player_budget in enumerate(statistics):
        plt.plot(player_budget, marker='', linestyle='-',
                 label=f'{players[i].name}')

    plt.xlabel('Rounds Played')
    plt.ylabel('Player Budget')
    plt.title('Player Budget over Rounds')
    plt.legend()
    plt.grid(True)

    plt.savefig(output_file)


def main():
    """
    Choose:
        [0] Play by yourself
        [1] Simulate

<On play by yourself call play_alone()>


<Only on Simulate:>

    Choose which strategies to simulate:
        [0] RandomPlayer
        [1] ..
        [2] ...

    > 0 1 2

    How many rounds?
    > 1000000

    Output plot to file?
    > plot.png
    ....
    """
    while True:
        print("Choose:")
        print("    [0] Play by yourself")
        print("    [1] Simulate")

        choice = input("> ").strip()

        if choice == '0':
            play_alone()
            break
        elif choice == '1':
            print("Choose which strategies to simulate:")
            print("    [0] Random player")
            print("    [1] Gambler fallacy player")
            print("    [2] Basic strategy")
            print("    [3] Hi-Lo card counter")
            print("    [4] Hi-Opt I card counter")
            print("    [5] Hi-Opt II card counter")
            print("    [6] KO card counter")
            print("    [7] Omega II card counter")
            print("    [8] Zen count card counter")
            print("    [9] 10 card counter")
            print("  Example: 0 1 3 4 5")

            strategies = input("> ").strip().split()
            print(strategies)
            players = []
            for strat in strategies:
                match strat:
                    case "0": players.append(RandomPlayer(0))
                    case "1": players.append(AveragePlayer(0))
                    case "2": players.append(Optimal_Player(0))
                    case "3": players.append(Card_Counter("Hi-Lo", 0, 6, STRAT_HI_LO))
                    case "4": players.append(Card_Counter("Hi-Opt I", 0, 6, STRAT_HI_OPTI))
                    case "5": players.append(Card_Counter("Hi-Opt II", 0, 6, STRAT_HI_OPTII))
                    case "6": players.append(Card_Counter("KO", 0, 6, STRAT_KO))
                    case "7": players.append(Card_Counter("Omega II", 0, 6, STRAT_OMEGAII))
                    case "8": players.append(Card_Counter("Zen Count", 0, 6, STRAT_ZEN_COUNT))
                    case "9": players.append(Card_Counter("10 Count", 0, 6, STRAT_10_COUNT))
                    case _: print("Invalid choice. Please try again.")

            rounds = int(input("How many rounds?\n> ").strip())

            output_file = input("Output plot to file?\n> ").strip()

            simulate(players, rounds, output_file)
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
