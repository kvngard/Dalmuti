from round import Round


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
        '''
            Represents a series of rounds.
        '''
        while len(self.hand_rank) > 0:

            current_round = Round(self.hand_rank)
            current_round.Play_Round(self)

            if len(self.hand_rank) == 1:
                self.next_hand_rank.append(self.hand_rank.pop(0))

            self.Cycle_To_Leader(current_round.leader)

            print("{}, you won the round!".format(current_round.leader))

        cont = self.next_hand_rank[0].Prompt_For_Boolean(
            "{}, you won! Do you wish to continue?".format(self.next_hand_rank[0].name))

        if cont:
            # If there are no more players to go out,
            # return the ranking for the next hand.
            return self.next_hand_rank
        else:
            return None
