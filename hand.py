class Round:

    def __init__(self, hand_rank):
        self.leader = None
        self.current_play = None
        self.players = list(hand_rank)

    def Check_If_Play_Topped(self, play):
        if self.current_play is None:
            self.current_play = play
            return True
        if len(play) == len(self.current_play):
            if play[0] > self.current_play[0]:
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

            while len(current_round.players) > 0:
                # Get the user who is currently "up-to-bat."
                player = self.hand_rank.pop(0)

                # Check if a player has not passed.
                if current_round.players.__contains__(player):
                    print(current_round.current_play)
                    player.Display_Hand()

                    # Ask for player's decision to play or pass
                    if current_round.Get_Len_Current_Play() > 0:
                        if player.Prompt_For_Boolean("Do you want to pass?"):
                            current_round.players.remove(player)
                        else:
                            cards = player.Prompt_For_Cards("")
                            current_round.current_play = cards
                    else:
                        cards = player.Prompt_For_Cards("")
                        current_round.current_play = cards

                # If a player "goes out" during a round,
                # they are placed in the next_hand_rank
                # queue and removed from the current rotation.
                if len(player.hand) == 0:
                    self.next_hand_rank.append(player)
                else:
                    self.hand_rank.append(player)

        # If there are no more players to go out,
        # return the ranking for the next hand.
        return self.next_hand_rank

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
'''
        + Play() - Creates Round objects and runs Query_For_Play for each player in hand_rank. Removes each player and places them at the back of hand_rank.
            Would use a while len(hand_rank) > 0 to loop over the players. As each round finishes, the Cycle_To_Leader() method is run.
        + Cycle_To_Leader(Player) - Used to make sure that the next Round starts with the leader from the last.
            Pops, peeks, and pushes users until the leader as at the front of hand_rank.
'''
