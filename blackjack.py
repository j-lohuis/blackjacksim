import matplotlib.pyplot as plt
import numpy as np
import random
import re
from dealer import *
from deck import *
from player import *


def play_alone():
    """Starts game with cli player."""
    deck = Deck(6, 0.75)
    dealer = Dealer(deck, [CLI_Player(1000)])

    dealer.play(10000)


def simulate(players, rounds, output_file):
    """Starts simulation with chosen strategies and plots the results."""
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

    plt.savefig("plots/" + output_file)


def main():
    """Entry point of the application. Asks the user what to do and does it accordingly."""
    print("Choose:")
    print("    [0] Play by yourself")
    print("    [1] Simulate")

    while True:
        choice = input("> ").strip()
        if re.match(r"^[01]$", choice):
            break
        else:
            print("Invalid choice, try again")

    if choice == '0':
        play_alone()
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


        strat_list = ""
        while True:
            strat_list = input("> ").strip()
            if re.match(r"^[0-9]( [0-9])*$", strat_list):
                break
            else:
                print("Invalid choice, try again")

        strategies = strat_list.split()
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

        rounds = 0
        while True:
            rounds_input = input("How many rounds?\n> ").strip()
            if re.match(r"^[0-9]+$", rounds_input):
                rounds = int(rounds_input)
                break
            else:
                print("Invalid choice, try again")

        output_file = input("Output plot to file?\n> ").strip()

        simulate(players, rounds, output_file)


if __name__ == '__main__':
    main()
