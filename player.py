import random
import sys
from enum import Enum

from deck import *


class Action(Enum):
    """All possible game decisions a player can make"""
    HIT = 0
    STAND = 1
    DOUBLE_DOWN = 2
    SPLIT = 3


class Player(object):
    """Class representing a player. Super-class of all the other players."""

    def __init__(self, name: str, budget: int) -> None:
        self.name = name
        self.budget = budget

    def see_card(self, card: Card) -> None:
        """Called by dealer everytime a card is drawn from the deck."""
        raise NotImplementedError("decide not implemented")

    def decide(self, cards, dealer_card: Card) -> Action:
        """Decides the next action of the player.

        Keyword arguments:
        cards -- the players hand
        dealer -- the dealers first card
        """
        raise NotImplementedError("decide not implemented")

    def bet(self) -> int:
        """Returns the amount the player bets."""
        raise NotImplementedError("bet not implemented")

    def result(self, winnings: int, player_cards, dealer_cards) -> None:
        """Gives the player the winnings of the round."""
        raise NotImplementedError("result not implemented")

    def on_shuffle(self) -> None:
        """Informs the player when the dealer shuffles the deck."""
        raise NotImplementedError("result not implemented")


class CLI_Player(Player):
    """Interactive player to play from the command line."""

    def __init__(self, budget: int) -> None:
        Player.__init__(self, "CLI", budget)
        self.last_bet = 0

    def see_card(self, card: Card) -> None:
        pass

    def decide(self, cards, dealer_card: Card) -> Action:
        """Asks the user for an action."""
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
                    case 2:
                        if self.budget < self.last_bet:
                            print("You do not have the budget to double down")
                            continue
                        if len(cards) != 2:
                            print("Doubling down is disallowed after hit.")
                            continue
                        return Action.DOUBLE_DOWN
                    case 3:
                        if self.budget < self.last_bet:
                            print("You do not have the budget to split")
                            continue
                        if len(cards) != 2 or cards[0].value() != cards[1].value():
                            print("You cannot split.")
                            continue
                        return Action.SPLIT

            except ValueError:
                pass
            print("Try again")

    def bet(self) -> int:
        """Asks the user for a bet."""
        while True:
            print(
                f"Place a bet, your current budget is {self.budget} or bet 0 to leave table:")
            try:
                bet = int(input())
                if bet == 0:
                    print(f"Left table.\nTotal winnings: {self.budget-1000}")
                    sys.exit(0)
                if bet > self.budget:
                    print("You don't have that much money")
                    continue
                if bet <= 0:
                    print("You cannot bet a negative amout")
                    continue

                self.last_bet = bet
                return bet
            except ValueError:
                pass

    def result(self, winnings: int, player_cards, dealer_cards) -> None:
        """Informs the user about the results."""
        self.budget += winnings

        if winnings > 0:
            print(f"You won {winnings} $!")
        else:
            print("Looks like you've lost")

        print(f"Your cards: {player_cards}")
        print(f"Your score: {score(player_cards)}")
        print(f"Dealer's cards: {dealer_cards}")
        print(f"Dealer's score: {score(dealer_cards)}")

    def on_shuffle(self) -> None:
        print("Deck was shuffled")


# implemented after rules from
# https://www.blackjackapprenticeship.com/blackjack-strategy-charts/
class Optimal_Player(Player):
    """Player that implements the theoretically optimal strategy without card counting."""

    def __init__(self, budget: int) -> None:
        Player.__init__(self, "Optimal Player", budget)

    def see_card(self, card: Card) -> None:
        pass

    def decide(self, cards, dealer_card: Card) -> Action:
        """Returns the optimal decision based on the rules from:
        https://www.blackjackapprenticeship.com/blackjack-strategy-charts/ 
        """
        hand_value = score(cards)

        strat = None

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
        # get the total sum of the players' hand
        value_sum = sum(card.value() for card in cards)
        num_aces = [card.value() for card in cards].count(11)

        # checks if there is an ace in the hand that is counted as 11
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

        raise ValueError("Impossible Hand")

    def bet(self) -> int:
        return 100

    def result(self, winnings: int, player_cards, dealer_cards) -> None:
        self.budget += winnings

    def on_shuffle(self) -> None:
        pass


# Cardvalues   0   1   2   3   4   5   6   7   8   9  10  11
STRAT_HI_LO = [0,  0, +1, +1, +1, +1, +1,  0,  0,  0, -1, -1]
STRAT_HI_OPTI = [0,  0,  0, +1, +1, +1, +1,  0,  0,  0, -1,  0]
STRAT_HI_OPTII = [0,  0, +1, +1, +2, +2, +1,  0,  0,  0, -2,  0]
STRAT_KO = [0,  0, +1, +1, +1, +1, +1, +1,  0,  0, -1, -1]
STRAT_OMEGAII = [0,  0, +1, +1, +2, +2, +2, +1,  0, -1, -2,  0]
STRAT_ZEN_COUNT = [0,  0, +1, +1, +2, +2, +2, +1,  0,  0, -2, -1]
STRAT_10_COUNT = [0,  0, +1, +1, +1, +1, +1, +1, +1, +1, -2, +1]


class Card_Counter(Optimal_Player):
    """Player that performs card counting according to a passed in strategy"""

    def __init__(self, name: str, budget: int, num_decks: int, strat) -> None:
        Optimal_Player.__init__(self, budget)
        self.name = name
        self.score = 0
        self.num_decks = num_decks
        self.left_decks = self.num_decks-1
        self.seen_cards = 0
        self.strat = strat

    def count(self, card: Card) -> None:
        """Adjusts the current count bases on the strategy this player was initialized with"""

        self.seen_cards += 1

        # we've seen an entire deck (52 cards)
        # so we need to adjust the number of decks left to be delt
        if self.seen_cards == 52:
            self.seen_cards = 0
            self.left_decks -= 1

        self.score += self.strat[card.value()]

    def see_card(self, card: Card) -> None:
        self.count(card)

    def bet(self) -> int:
        if self.score <= 0:
            return 0

        num_decks = 1 if self.num_decks == 0 else self.num_decks
        # compute the amout to bet based on the "true score"
        # The true score is simply computed by dividing the current score
        # by the number of decks left to be delt.
        bet = 100 * int(self.score / num_decks)
        return bet

    def on_shuffle(self) -> None:
        self.score = 0
        self.left_decks = self.num_decks-1
        self.seen_cards = 0


class RandomPlayer(Player):
    """Player that plays completely random moves and bets random amount"""

    def __init__(self, budget: int) -> None:
        Player.__init__(self, "Random Player", budget)
        self.last_bet = 0

    def see_card(self, card: Card) -> None:
        pass

    def decide(self, cards, dealer_card: Card) -> Action:
        if len(cards) == 2 and cards[0].value() == cards[1].value():
            return random.choice(list(Action))
        else:
            return random.choice([Action.HIT, Action.STAND, Action.DOUBLE_DOWN])

    def bet(self) -> int:
        self.last_bet = random.randint(0, 1000)

        return self.last_bet

    def result(self, winnings: int, player_cards, dealer_cards) -> None:
        self.budget += winnings

    def on_shuffle(self) -> None:
        pass


class AveragePlayer(Player):
    """Player simulating the behaviour of a average person that is pretty bad at Blackjack."""

    def __init__(self, budget: int) -> None:
        Player.__init__(self, "Average Player", budget)
        self.mood = "average"
        self.last_bet = 100
        self.last_result = "draw"

    def see_card(self, card: Card) -> None:
        pass

    def decide(self, cards, dealer_card: Card) -> Action:
        """ Decides the next action based on the results of the last round

        Plays: 
        -> careful if overshot last round
        -> more risky if lost last round
        -> normal if won last round
        """

        threshold = 16
        actions = []
        match(self.mood):
            case 'average':
                pass
            case 'careful':
                threshold -= 3
            case 'risky':
                threshold += 2
                if score(cards) == 11:
                    return Action.DOUBLE_DOWN
        if score(cards) <= threshold:
            return Action.HIT
        else:
            return Action.STAND

    def bet(self) -> int:
        """Doubles bet from last round if lost to make up the losses"""
        match(self.last_result):
            case "lose":
                self.last_bet = 2*self.last_bet
            case "win":
                self.last_bet = 100
            case "draw":
                self.last_bet = self.last_bet

        return self.last_bet

    def result(self, winnings: int, player_cards, dealer_cards) -> None:
        """Simulate basic behaviour based on results of last round

        Sets the "mood" depending on the result of the last round
        """
        if score(player_cards) > 21:
            self.mood = "careful"
            self.last_result = "lose"
        elif score(player_cards) <= 21 and winnings == 0:
            self.mood = "risky"
            self.last_result = "lose"
        if winnings == self.last_bet:
            self.mood = "average"
            self.last_result = "draw"
        elif winnings > self.last_bet:
            self.last_result = "win"
            # if they won, they keep the last decision style (mood), because it 'worked'

        self.budget += winnings

    def on_shuffle(self) -> None:
        pass
