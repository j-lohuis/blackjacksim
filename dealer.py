from deck import *
from player import *


class Dealer:
    def __init__(self, deck: Deck, players) -> None:
        self.deck = deck
        self.players = players

        self.deck.shuffle()

    def show_to_others(self, card: Card, player: Player) -> None:
        for other in self.players:
            if other is not player:
                other.see_card(card)

    def play_round(self):
        # Players place a bet
        print("======== Placing Bets")
        bets = []
        for player in self.players:
            bets.append(player.bet())

        print("======== Dealing to Dealer")
        # Deal cards to dealer
        dealer_cards = [self.deck.pick(), self.deck.pick()]
        for player in self.players:
            player.see_card(dealer_cards[0])

        print("======== Dealing to Players")
        # Deal cards to players
        player_cards = []
        for player in self.players:
            c1, c2 = self.deck.pick(), self.deck.pick()
            # just for testing split
            c1 = Card(Suite.S_SPADES, CardValue.V_ACE)
            c2 = Card(Suite.S_DIAMONDS, CardValue.V_ACE)
            player_cards.append([c1, c2])

            self.show_to_others(c1, player)
            self.show_to_others(c2, player)

        print("======== Asking for Strategy")
        # Ask players for stategy
        split_aces = False
        for i, player in enumerate(self.players):
            if split_aces:
                continue
            while True:
                strat = player.decide(player_cards[i], dealer_cards[0])
                match strat:
                    case Action.HIT:
                        card = self.deck.pick()
                        player_cards[i].append(card)
                        self.show_to_others(card, player)

                        if score(player_cards[i]) > 21:
                            break
                    case Action.STAND:
                        break
                    case Action.DOUBLE_DOWN:
                        # TODO: Justus
                        # sometimes only possible with starting sum 9, 10, 11
                        # in biggest Casino chain mgm always possible
                        if player.budget < bets[i]:
                            continue  # not enough money to  double down

                        player.budget -= bets[i]
                        bets[i] *= 2

                        card = self.deck.pick()
                        player_cards[i].append(card)
                        self.show_to_others(card, player)

                        break
                    case Action.SPLIT:
                        # TODO: Justus
                        if player.budget < bets[i] or len(player_cards[i]) != 2 or player_cards[i][0].value() != player_cards[i][1].value():
                            continue  # cannot split

                        # modify player, bets, player_cards
                        self.players.insert(i+1, self.players[i])
                        bets.insert(i+1, bets[i])
                        player_cards.insert(i+1, [player_cards[i][1]])
                        player_cards[i] = [player_cards[i][0]]

                        # draw 1 card for both splits
                        card = self.deck.pick()
                        player_cards[i].append(card)
                        self.show_to_others(card, player)

                        card = self.deck.pick()
                        player_cards[i+1].append(card)
                        self.show_to_others(card, player)
                        if (player_cards[i][0].value() == 11):
                            split_aces = True
                            break  # you only get one more card after splitting aces

        print("======== Dealer playing with himself")
        # Dealer plays with himself
        while score(dealer_cards) <= 16:
            dealer_cards.append(self.deck.pick())

        for i in range(1, len(dealer_cards)):
            self.show_to_others(dealer_cards[i], None)

        dealer_score = score(dealer_cards)

        print("======== Determining winners")
        # Determine winners
        for i, player in enumerate(self.players):
            player_score = score(player_cards[i])

            if player_score > 21:
                player.result(0, player_cards[i], dealer_cards)
            elif dealer_score > 21 or player_score > dealer_score:
                player.result(bets[i]*2, player_cards[i], dealer_cards)
            elif player_score == dealer_score:
                player.result(bets[i], player_cards[i], dealer_cards)
            else:
                player.result(0, player_cards[i], dealer_cards)
