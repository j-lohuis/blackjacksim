import numpy as np

from deck import *
from player import *


class Dealer:
    """
    Class that manages all logic needed to play blackjack

    It calls all specific methods from the players during play.
    """

    def __init__(self, deck: Deck, players) -> None:
        self.deck = deck
        self.players = players

        self.deck.shuffle()
        self.budget_history = [np.array([]) for player in players]
        self.wins = [0 for player in players]
        self.losses = [0 for player in players]
        self.draws = [0 for player in players]

    def show_to_others(self, card: Card, player: Player) -> None:
        """Shows a card do all players except `player`"""
        for other in self.players:
            if other is not player:
                other.see_card(card)

    def deal(self, to: Player) -> Card:
        """Picks a card from the deck, show it to everyone except `player` and returns it"""
        card = self.deck.pick()
        self.show_to_others(card, to)
        return card

    def play_with(self, player: Player, bet: int):
        """
        Plays one round with `player`, evaluating its strategy until no more cards can be delt.

        Returns an array of hands and potential winnings for each hand.
        """

        # player didn't bet anything, just ignore them
        if bet == 0:
            return None

        # Deal the initial 2 card hand
        potential_winnings = [bet * 2]
        hands = [[self.deal(player), self.deal(player)]]

        # Iterate through each hand yet to be delt with
        i = 0
        while i < len(hands):
            # Hand is bust or 21
            if score(hands[i]) >= 21:
                # Is hand a blackjack?
                if score(hands[i]) == 21 and i == 0 and len(hands) == 1 and len(hands[0]) == 2:
                    potential_winnings[i] = int(1.5 * potential_winnings[i])

                # move on to the next hand
                i += 1
                continue

            # Ask player for their strategy
            decision = player.decide(hands[i], self.dealer_cards[0])
            match decision:
                case Action.HIT:
                    # simply add another card to the current hand
                    hands[i].append(self.deal(player))
                case Action.STAND:
                    # Hand is finished, move to the next
                    i += 1
                case Action.DOUBLE_DOWN:
                    # Add one final card, add bet and move to the next hand
                    hands[i].append(self.deal(player))
                    potential_winnings[i] += bet * 2
                    player.budget -= bet
                    i += 1
                case Action.SPLIT:
                    # If splitting aces, the next cards delt are the last of the hand.
                    # So just move to the next hand after these
                    if hands[i][0].value() == 11 and hands[i][0].value() == hands[i][1].value():
                        hands.insert(i+1, [hands[i].pop()])
                        hands[i].append(self.deal(player))
                        hands[i+1].append(self.deal(player))
                        potential_winnings.insert(i+1, bet*2)
                        player.budget -= bet
                        i += 2
                    else:
                        # move one card from current hand to a new one
                        # and deal a new to each hand
                        hands.append([hands[i].pop(), self.deal(player)])
                        hands[i].append(self.deal(player))
                        # add bet for the new hand
                        potential_winnings.append(bet*2)
                        player.budget -= bet

        return (hands, potential_winnings)

    def player_won(self, player_score: int, dealer_score: int) -> int:
        """
        Determines who has won in a round
        Returns
            0 if the dealer wins,
            1 if the player wins,
            2 on a draw.
        """
        if player_score > 21:
            return 0
        if player_score == dealer_score:
            return 2
        if dealer_score > 21:
            return 1
        return 1 if player_score > dealer_score else 0

    def play_round(self):
        """Plays one round with every player"""

        # add player budgets to the statistics
        for i, player in enumerate(self.players):
            self.budget_history[i] = np.append(
                self.budget_history[i], player.budget)

        # Players place a bet
        bets = []
        for player in self.players:
            bets.append(player.bet())
            player.budget -= bets[-1]

        # Deal cards to dealer
        self.dealer_cards = [self.deal(None), self.deck.pick()]

        # Deal for each player
        hands_and_wins = list()
        for i, player in enumerate(self.players):
            hands_and_wins.append(self.play_with(player, bets[i]))

        # Dealer picks cards until reaching 17 or over
        while score(self.dealer_cards) < 17:
            self.dealer_cards.append(self.deck.pick())

        # Show the picked cards to all players
        for i in range(1, len(self.dealer_cards)):
            self.show_to_others(self.dealer_cards[i], None)

        dealer_score = score(self.dealer_cards)

        # Determine winners
        for i, player in enumerate(self.players):
            if hands_and_wins[i] == None:
                continue

            # collect all winnings from every hand the player
            # played in this round
            for j in range(len(hands_and_wins[i][0])):
                player_score = score(hands_and_wins[i][0][j])
                result = self.player_won(player_score, dealer_score)
                if dealer_score == 21 and len(self.dealer_cards) == 2:
                    result = 2 if player_score == 21 and len(
                        hands_and_wins[i][0][j]) == 2 else 0
                winnings = 0
                match result:
                    case 0:
                        self.losses[i] += 1
                        pass
                    case 1:
                        self.wins[i] += 1
                        winnings = hands_and_wins[i][1][j]
                    case 2:
                        self.draws[i] += 1
                        winnings = bets[i]

                # give player their money
                player.result(
                    winnings, hands_and_wins[i][0][j], self.dealer_cards)

    def play(self, n_rounds: int) -> None:
        """Simulates `n_rounds` of blackjack and returns the statistics collected"""
        for i in range(n_rounds):
            if self.deck.should_shuffle():
                self.deck.shuffle()
                for p in self.players:
                    p.on_shuffle()

            if (i+1) % 1000 == 0:
                print(f"Round {i+1}")

            self.play_round()

        for i, p in enumerate(self.players):
            print(
                f"Total for player {p.name}: {self.wins[i]}/{self.draws[i]}/{self.losses[i]}")
        return self.budget_history
