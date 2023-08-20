import numpy as np
from enum import Enum
from deck import *


class Action(Enum):
    HIT = 0
    STAND = 1
    DOUBLE_DOWN = 2
    SPLIT = 3


class Player(object):
    def __init__(self, budget: int) -> None:
        self.budget = budget

    def see_card(self, card: Card) -> None:
        raise NotImplementedError("decide not implemented")

    def decide(self, cards, dealer_card: Card) -> Action:
        raise NotImplementedError("decide not implemented")

    def bet(self) -> int:
        raise NotImplementedError("bet not implemented")

    def result(self, winnings: int) -> None:
        raise NotImplementedError("result not implemented")


class CLI_Player(Player):
    def __init__(self, budget: int) -> None:
        Player.__init__(self, budget)

    def see_card(self, card: Card) -> None:
        print(f"Seen card {card}")

    def decide(self, cards, dealer_card: Card) -> Action:
        print(f"Dealers card: {dealer_card}")
        print(f"Your hand ({score(cards)}):")
        for card in cards:
            print(card)

        print()
        print("Choose one of these actions:")
        print("    [0] Hit")
        print("    [1] Stand")
        print("    [2] Double down")
        print("    [3] Split")

        while True:
            choice = input()
            try:
                num = int(choice)
                match num:
                    case 0: return Action.HIT
                    case 1: return Action.STAND
                    case 2: return Action.DOUBLE_DOWN
                    case 3: return Action.SPLIT
            except ValueError:
                pass
            print("Try again")

    def bet(self) -> int:
        while True:
            print(f"Place a bet, your current budget is {self.budget}:")
            try:
                bet = int(input())
                print(f"got input {bet}")
                if bet > self.budget:
                    print("You don't have that much money")
                    continue
                if bet <= 0:
                    print("You cannot bet a negative amout")
                    continue

                self.budget -= bet
                return bet
            except ValueError:
                pass

    def result(self, winnings: int, player_cards, dealer_cards) -> None:
        self.budget += winnings

        if winnings > 0:
            print(f"You won {winnings} $!")
        else:
            print("Looks like you've lost")

        print(f"Your score: {score(player_cards)}")
        print(f"Dealer's score: {score(dealer_cards)}")
