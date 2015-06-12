class Round:

    def __init__(self, hand_rank):
        self.leader = None
        self.current_play = None
        self.players = list(hand_rank)

    def Check_If_Can_Top(self, player):
        '''
            Checks if a player can top the current set of cards by
            checking to see if a player has at least as many cards
            of an equal or greater rank as the current play.
        '''
        for k, v in player.hand.items():
            # Checks to see if the player's hand contains a card of a higher
            # rank (lower value).
            if k < self.current_play[0]:
                # Checks if the player's hand contains 13 or 'joker' cards.
                if player.hand.get(13):
                    # If so, the number of cards in the play is compared against
                    # the number of cards plus and joker cards.
                    if v + player.hand.get(13) >= len(self.current_play):
                        return True
                else:
                    # If not, the number of cards in the player's hand is
                    # simply compared with the length of the current play.
                    if v >= len(self.current_play):
                        return True
            else:
                # If the value isn't less than the first value in the play,
                # then the hand contains no more cards or sets of cards of a
                # higher rank.
                return False
        return False

    def Check_If_Play_Topped(self, play):
        '''
            Checks if the conditions for topping a play are met.
            1. All the cards are the same value (excluding jokers).
            2. There are the same number of cards in the play as
               the current play.
            3. The play contains cards of a higher rank than the
               current play.
        '''
        # Checks if the cards in the set are all equal or if not, that the
        # difference is the same as the number of jokers in their hand.
        if play.count(play[0]) != len(play) and play.count(play[0]) != len(play) - play.count(13):
            return False
        if self.current_play is None:
            return True
        if len(play) == len(self.current_play):
            if play[0] < self.current_play[0]:
                return True

        return False

    def Play_Turn(self, player):
        '''
            The center of the game. The current situation is checked
            and if there is a play, players that meet the criteria it
            are asked if they would like to top. The play is then
            tested and then accepted or rejected.
        '''
        print("Leader: {}\nCurrent Play: {}".format(
            self.leader, self.current_play))

        player.Display_Hand()

        if self.current_play:
            if self.Check_If_Can_Top(player):
                if player.Prompt_For_Boolean("{}, do you want to pass?".format(player.name)):
                    self.players.remove(player)
                    return
                else:
                    while True:
                        cards = player.Prompt_For_Cards(
                            "which cards will you play? ")
                        if self.Check_If_Play_Topped(cards):
                            self.current_play = cards
                            self.leader = player
                            return
                        else:
                            player.Add_Cards_To_Hand(cards)
                            continue
            else:
                self.players.remove(player)
                return
        else:
            cards = player.Prompt_For_Cards("which cards will you play? ")
            self.current_play = cards
            self.leader = player

    def Play_Round(self, hand):
        '''
            Represents a series of turns. Performs the tasks
            to set up the next turn and clean up once the
            turn is played.
        '''
        while len(self.players) > 0:

            if self.leader is hand.hand_rank[0]:
                break

            # Get the user who is currently "up-to-bat."
            player = hand.hand_rank.pop(0)

            # Check if the player is still in and let them play their turn.
            if self.players.__contains__(player):
                self.Play_Turn(player)

            # If a player "goes out" during a round,
            # they are placed in the next_hand_rank
            # queue and removed from the current rotation.
            if len(player.hand) == 0:
                hand.next_hand_rank.append(player)
                if self.players.__contains__(player):
                    self.players.remove(player)
            else:
                hand.hand_rank.append(player)
