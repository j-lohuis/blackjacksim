from enum import Enum
import numpy as np


class CardValue(Enum):
    """Represents every possible face value of a card"""
    V_ACE = 0
    V_2 = 1
    V_3 = 2
    V_4 = 3
    V_5 = 4
    V_6 = 5
    V_7 = 6
    V_8 = 7
    V_9 = 8
    V_10 = 9
    V_JACK = 10
    V_QUEEN = 11
    V_KING = 12


class Suite(Enum):
    """Represents a suite of a card"""
    S_SPADES = 0b00_0000
    S_DIAMONDS = 0b01_0000
    S_CLUBS = 0b10_0000
    S_HEARTS = 0b11_0000


class Card:
    """Represents a card, i.e. both a suite and a value

    Card: 0bSSVVVV
    S = Suite
    V = Value
    """

    def __init__(self, suite: Suite, value: CardValue) -> None:
        self.card = suite.value | value.value

    def __repr__(self) -> str:
        """Formats the suite and value to be human readable"""
        name = ""
        match (self.card & 0b00_1111):
            case 0: name = "Ace"
            case 1: name = "2"
            case 2: name = "3"
            case 3: name = "4"
            case 4: name = "5"
            case 5: name = "6"
            case 6: name = "7"
            case 7: name = "8"
            case 8: name = "9"
            case 9: name = "10"
            case 10: name = "Jack"
            case 11: name = "Queen"
            case 12: name = "King"

        name += " of "
        match (self.card & 0b11_0000):
            case 0b00_0000: name += "Spades"
            case 0b01_0000: name += "Diamonds"
            case 0b10_0000: name += "Clubs"
            case 0b11_0000: name += "Hearts"

        return name

    def value(self) -> int:
        """Maps a card to the number of points it's worth in Blackjack"""
        match (self.card & 0b00_1111):
            case 0: return 11
            case 1: return 2
            case 2: return 3
            case 3: return 4
            case 4: return 5
            case 5: return 6
            case 6: return 7
            case 7: return 8
            case 8: return 9
            case 9: return 10
            case 10: return 10
            case 11: return 10
            case 12: return 10


class Deck:
    """Represents a collection of Cards"""

    def __init__(self, number_of_decks: int, shuffle_point: float) -> None:
        cards = []
        for i in range(number_of_decks):
            for suite in Suite:
                for val in CardValue:
                    cards.append(Card(suite, val))

        self.cards = np.array(cards)
        self.top = 0
        self.stop_card_index = int(shuffle_point * len(self.cards))

    def __repr__(self) -> str:
        return str(self.cards)

    def shuffle(self) -> None:
        """Shuffles the entire deck"""
        np.random.shuffle(self.cards)
        self.top = 0

    def pick(self) -> Card:
        """Picks the top card of the deck"""
        card = self.cards[self.top]
        self.top += 1
        return card

    def should_shuffle(self) -> bool:
        """Returns true if the deck should be shuffled after a round is over"""
        return self.top > self.stop_card_index


def score(cards) -> int:
    """
    Computes the most optimistic score of a list of cards.

    Optimistic means that if an ace can count as 11 without going over 21, it does.
    """
    result = 0
    ace_count = 0
    for card in cards:
        result += card.value()
        if card.value() == 11:
            ace_count += 1

        # we are over 21, look if we can make an ace count as 1.
        # if so, subtract 10 from the score to make it count as 1.
        if result > 21 and ace_count > 0:
            result -= 10
            ace_count -= 1

    return result
