import numpy as np
from enum import Enum
from deck import *
from debug import *


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

    def result(self, winnings: int, player_cards, dealer_cards) -> None:
        raise NotImplementedError("result not implemented")

    def on_shuffle(self) -> None:
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

    def on_shuffle(self) -> None:
        print("Deck was shuffled")


# implemented after rules from
# https://www.blackjackapprenticeship.com/blackjack-strategy-charts/
class Optimal_Player(Player):
    def __init__(self, budget: int) -> None:
        Player.__init__(self, budget)

    def see_card(self, card: Card) -> None:
        pass

    def decide(self, cards, dealer_card: Card) -> Action:
        hand_value = score(cards)
        if hand_value == 21:
            return Action.STAND

        # check for splits
        if len(cards) == 2 and cards[0].value() == cards[1].value():
            match cards[0].value():
                case 11 | 8: return Action.SPLIT
                case 9:
                    if dealer_card.value() <= 9 and dealer_card != 7:
                        return Action.SPLIT
                    else:
                        return Action.STAND
                case 7 | 3 | 2:
                    if dealer_card.value() <= 7:
                        return Action.SPLIT
                    else:
                        return Action.HIT
                case 6:
                    if dealer_card.value() <= 6:
                        return Action.SPLIT
                    else:
                        return Action.HIT
                case 5:
                    if dealer_card.value() <= 9:
                        return Action.DOUBLE_DOWN
                    else:
                        return Action.HIT
                case 4:
                    if 5 <= dealer_card.value() <= 6:
                        return Action.SPLIT
                    else:
                        return Action.HIT

        # soft totals and hard totals
        value_sum = sum(card.value() for card in cards)
        num_aces = [card.value() for card in cards].count(11)
        if value_sum - hand_value != num_aces * 10:
            # soft totals
            match hand_value:
                case 20: return Action.STAND
                case 19:
                    if dealer_card.value() == 6:
                        return Action.DOUBLE_DOWN
                    else:
                        return Action.STAND
                case 18:
                    if 2 <= dealer_card.value() <= 6:
                        return Action.DOUBLE_DOWN
                    elif 9 <= dealer_card.value():
                        return Action.HIT
                    else:
                        return Action.STAND
                case 17:
                    if 3 <= dealer_card.value() <= 6:
                        return Action.DOUBLE_DOWN
                    else:
                        return Action.HIT
                case 16 | 15:
                    if 4 <= dealer_card.value() <= 6:
                        return Action.DOUBLE_DOWN
                    else:
                        return Action.HIT
                case 14 | 13:
                    if 5 <= dealer_card.value() <= 6:
                        return Action.DOUBLE_DOWN
                    else:
                        return Action.HIT
        else:
            # hard totals
            match hand_value:
                case 20 | 19 | 18 | 17:
                    return Action.STAND
                case 16 | 15 | 14 | 13:
                    if 2 <= dealer_card.value() <= 6:
                        return Action.STAND
                    else:
                        return Action.HIT
                case 12:
                    if 4 <= dealer_card.value() <= 6:
                        return Action.STAND
                    else:
                        return Action.HIT
                case 11:
                    return Action.DOUBLE_DOWN
                case 10:
                    if 2 <= dealer_card.value() <= 9:
                        return Action.DOUBLE_DOWN
                    else:
                        return Action.HIT
                case 9:
                    if 3 <= dealer_card.value() <= 6:
                        return Action.DOUBLE_DOWN
                    else:
                        return Action.HIT
            if hand_value <= 8:
                return Action.HIT
        print("Something went wrong, this should not happen")

    def bet(self) -> int:
        bet = 100
        self.budget -= bet
        return bet

    def result(self, winnings: int, player_cards, dealer_cards) -> None:
        self.budget += winnings

    def on_shuffle(self) -> None:
        pass


class Card_Counter(Optimal_Player):
    def __init__(self, budget: int, num_decks: int) -> None:
        Optimal_Player.__init__(self, budget)
        self.score = 0
        self.num_decks = num_decks
        self.left_decks = self.num_decks-1
        self.seen_cards = 0

    def count(self, card: Card) -> None:
        self.seen_cards += 1

        if self.seen_cards == 52:
            self.seen_cards = 0
            self.left_decks -= 1

        if card.value() <= 6:
            self.score += 1
        elif card.value() >= 10:
            self.score -= 1
        else:
            pass

    def see_card(self, card: Card) -> None:
        self.count(card)

    def bet(self) -> int:
        debug(f"....... Score={self.score}")
        if self.score <= 0:
            debug(f"....... not betting")
            return 0

        num_decks = 1 if self.num_decks == 0 else self.num_decks
        bet = 100 * int(self.score / num_decks)
        debug(f"....... true score = {self.score / num_decks}")
        debug(f"....... betting {bet}")
        self.budget -= bet
        return bet

    def result(self, winnings: int, player_cards, dealer_cards) -> None:
        for card in dealer_cards:
            self.count(card)
        debug(f"... Budget={self.budget}")
        Optimal_Player.result(self, winnings, player_cards, dealer_cards)
    
    def on_shuffle(self) -> None:
        self.score = 0
        self.left_decks = self.num_decks-1
        self.seen_cards = 0
