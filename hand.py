class Round:

    def __init__(self, hand_rank):
        self.leader = None
        self.current_play = None
        self.players = list(hand_rank)

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

    def Get_Len_Current_Play(self):
        if self.current_play is None:
            return 0
        else:
            return len(self.current_play)


class Hand:

    def __init__(self, hand_rank):
        self.hand_rank = hand_rank
        self.next_hand_rank = []

    def Play_Hand(self):
        while len(self.hand_rank) != 0:

            current_round = Round(self.hand_rank)

            while len(current_round.players) > 1:
                # Get the user who is currently "up-to-bat."
                player = self.hand_rank.pop(0)

                # Check if a player has not passed.
                if current_round.players.__contains__(player):
                    print(
                        "Play to beat: {}".format(current_round.current_play))

                    player.Display_Hand()

                    # Ask for player's decision to play or pass
                    if current_round.Get_Len_Current_Play() > 0:
                        if player.Prompt_For_Boolean("{}, do you want to pass?".format(player.name)):
                            current_round.players.remove(player)
                        else:
                            cards = player.Prompt_For_Cards(
                                "Which cards will you play? ")
                            if current_round.Check_If_Play_Topped(cards):
                                current_round.current_play = cards
                            else:
                                current_round.players.remove(player)
                    else:
                        cards = player.Prompt_For_Cards(
                            "Which cards will you play? ")
                        current_round.current_play = cards

                # If a player "goes out" during a round,
                # they are placed in the next_hand_rank
                # queue and removed from the current rotation.
                if len(player.hand) == 0:
                    self.next_hand_rank.append(player)
                else:
                    self.hand_rank.append(player)

            print("{}, you won the round!".format(current_round.leader))
            self.Cycle_To_Leader(current_round.leader)
            current_round = Round(self.hand_rank)

        print(self.next_hand_rank)
        cont = self.next_hand_rank[0].Prompt_For_Boolean(
            "{}, you won! Do you wish to continue?".format(player.name))

        if cont:
            # If there are no more players to go out,
            # return the ranking for the next hand.
            return self.next_hand_rank
        else:
            return None

    def Cycle_To_Leader(self, player):
        '''
            Cycles through the players until the player at the
            front of hand_rank is the leader from the previous
            round.
        '''
        leader = None
        while leader is not player:
            leader = self.hand_rank.pop(0)
            if leader is player:
                self.hand_rank.insert(0, player)
            else:
                self.hand_rank.append(player)
