import numpy as np
from deck import *
from player import *


class Dealer:
    def __init__(self, deck: Deck, players) -> None:
        self.deck = deck
        self.players = players

        self.deck.shuffle()
        self.budget_history = [np.array([]) for player in players]
        self.wins = [0 for player in players]
        self.losses = [0 for player in players]
        self.draws = [0 for player in players]

    # Shows card to all players except player
    def show_to_others(self, card: Card, player: Player) -> None:
        for other in self.players:
            if other is not player:
                other.see_card(card)

    # Picks a card and shows it to all players except to
    def deal(self, to: Player) -> Card:
        card = self.deck.pick()
        self.show_to_others(card, to)
        return card

    # Evaluates the whole strategy of the player and their bet
    # and returns array of hands with potential winnings
    def play_with(self, player: Player, bet: int):
        if bet == 0:
            return None

        potential_winnings = [bet * 2]
        hands = [[self.deal(player), self.deal(player)]]

        i = 0
        while i < len(hands):
            if score(hands[i]) >= 21:
                if score(hands[i]) == 21 and i == 0 and len(hands) == 1 and len(hands[0]) == 2:
                    potential_winnings[i] = int(1.5 * potential_winnings[i])
                i += 1
                continue

            decision = player.decide(hands[i], self.dealer_cards[0])
            match decision:
                case Action.HIT:
                    hands[i].append(self.deal(player))
                case Action.STAND:
                    i += 1
                case Action.DOUBLE_DOWN:
                    potential_winnings[i] += bet * 2
                    hands[i].append(self.deal(player))
                    player.budget -= bet
                    i += 1
                case Action.SPLIT:
                    if hands[i][0].value() == 11 and hands[i][0].value() == hands[i][1].value():
                        hands.insert(i+1, [hands[i].pop()])
                        hands[i].append(self.deal(player))
                        hands[i+1].append(self.deal(player))
                        potential_winnings.insert(i+1, bet)
                        player.budget -= bet
                        i += 2
                    else:
                        hands.append([hands[i].pop(), self.deal(player)])
                        hands[i].append(self.deal(player))
                        potential_winnings.append(bet)
                        player.budget -= bet

        return (hands, potential_winnings)

    def player_won(self, player_score: int, dealer_score: int) -> int:
        if player_score > 21:
            return 0
        if player_score == dealer_score:
            return 2
        if dealer_score > 21:
            return 1
        return 1 if player_score > dealer_score else 0

    def play_round(self):
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

        hands_and_wins = list()
        for i, player in enumerate(self.players):
            hands_and_wins.append(self.play_with(player, bets[i]))

        # Dealer plays with himself
        while score(self.dealer_cards) < 17:
            self.dealer_cards.append(self.deck.pick())

        for i in range(1, len(self.dealer_cards)):
            self.show_to_others(self.dealer_cards[i], None)

        dealer_score = score(self.dealer_cards)

        # Determine winners
        for i, player in enumerate(self.players):
            if hands_and_wins[i] == None:
                continue

            before = player.budget
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

                # print(f"{winnings-bets[i]}")
                player.result(
                    winnings, hands_and_wins[i][0][j], self.dealer_cards)

    def play(self, n_rounds: int) -> None:
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
