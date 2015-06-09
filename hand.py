class Round:

    def __init__(self, hand_rank):
        self.leader = None
        self.current_play = None
        self.players = list(hand_rank)

    def Check_If_Can_Top(self, player):
        for k, v in player.hand.items():
            if k < self.current_play[0]:
                if v >= len(self.current_play):
                    return True
            else:
                return False
        return False

    def Check_If_Play_Topped(self, play):
        if play[1:] != play[:-1]:
            return False
        if self.current_play is None:
            self.current_play = play
            return True
        if len(play) == len(self.current_play):
            if play[0] < self.current_play[0]:
                return True

        return False

    def Play_Turn(self, player):
        print(
            "Leader: {}\nPlay to beat: {}".format(self.leader, self.current_play))

        player.Display_Hand()

        # Check if
        if self.current_play:
            if self.Check_If_Can_Top(player):
                if player.Prompt_For_Boolean("{}, do you want to pass?".format(player.name)):
                    self.players.remove(player)
                    return
                else:
                    while True:
                        cards = player.Prompt_For_Cards(
                            ("{}, which cards will you play? ").format(player.name))
                        if self.Check_If_Play_Topped(cards):
                            self.current_play = cards
                            self.leader = player
                            return
                        else:
                            break
            else:
                self.players.remove(player)
                return
        else:
            cards = player.Prompt_For_Cards(
                ("{}, which cards will you play? ").format(player.name))
            self.current_play = cards
            self.leader = player

    def Play_Round(self, hand):
        while len(self.players) > 1:
            # Get the user who is currently "up-to-bat."
            player = hand.hand_rank.pop(0)

            print("Play order:", hand.hand_rank)
            print("Current Round:", self.players)

            # Check if a player has not passed.
            if self.players.__contains__(player):
                self.Play_Turn(player)

            # If a player "goes out" during a round,
            # they are placed in the next_hand_rank
            # queue and removed from the current rotation.
            if len(player.hand) == 0:
                hand.next_hand_rank.append(player)
            else:
                hand.hand_rank.append(player)


class Hand:

    def __init__(self, hand_rank):
        self.hand_rank = hand_rank
        self.next_hand_rank = []

    def Cycle_To_Leader(self, leader):
        '''
            Cycles through the players until the player at the
            front of hand_rank is the leader from the previous
            round.
        '''
        player = None

        # Accounts for situations where the leader has "gone out."=
        if self.hand_rank.__contains__(leader):
            while player is not leader:
                player = self.hand_rank.pop(0)
                if player is leader:
                    self.hand_rank.insert(0, player)
                else:
                    self.hand_rank.append(player)

    def Play_Hand(self):
        while len(self.hand_rank) != 0:

            current_round = Round(self.hand_rank)
            current_round.Play_Round(self)

            print("{}, you won the round!".format(current_round.leader))

            self.Cycle_To_Leader(current_round.leader)

        cont = self.next_hand_rank[0].Prompt_For_Boolean(
            "{}, you won! Do you wish to continue?".format(self.next_hand_rank[0].name))

        if cont:
            # If there are no more players to go out,
            # return the ranking for the next hand.
            return self.next_hand_rank
        else:
            return None
