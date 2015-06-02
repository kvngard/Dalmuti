# Dalmuti
Python implementation of the card game "The Great Dalmuti"

Game Process

    Win Condition
        - Size of hand is 0

    General Information
        - Deck of size 80
        - 5 to 8 players
        - A card's rank goes up as its number goes down.
        - Jesters are rank 13, but can act as a wildcard when played with at least one other card.
        - The game consists of "hands," which in turn consist of "rounds."

    Setup
        - Shuffle Deck (Cards dealt in random order)
        - Each player is given a card
        - Based on the card's value, players are assigned a position
        - Highest: Greater Dalmuti (GD), 2nd: Lesser Dalmuti(LD), 2nd-to-last:Lesser Peon (LP), Last: Greater Peon (GP), Everyone Else: Merchant (M)
            + This could simply be represented by two arrays, one for the current hand and one for the folllowing.
            + GD: hand_rank[0], LD: hand_rank[1], LP: hand_rank[n-1], GP: hand_rank[n]

    The Deal
        - Cards are shuffled and distributed one by one until no cards remain
            + First card is dealt to the highest ranking player and goes in order

    Revolution
        - If a player is dealt both Jesters, they can call a revolution, meaning the taxation phase is skipped.
        - If the player declaring the revolution is the GP, then all ranked players exchanges seats with their opposites.

    Taxation
        - GD selects 2 cards and gives them to the GP, who then must give up their two best cards (highest rank).
        - LD selects 1 card and exchanges it for the best card of the LP.

    Play
        - The winner of the previous round (or the GD for the first round of a hand) plays a set of one or more cards of the same rank.
        - The following player may choose to "top" the play by placing a set of the same number of cards of better rank, OR
        - Players can choose not to top the current play and then must sit out the remainer of a round.

    Going Out
        - As players play their last card in their hands, they are said to have "gone out" of the current hand.
        - Players are ranked for the following hand in the order they go out of the current hand.
            + The first player to go out is the GD for the next hand, the second is the LD, and so on.
        - If no one tops the last play a player makes when going out, then the lead passes down the ranks to the next player who still has cards in their hand.

Design Notes (Subject to change)

    A few different classes spring to mind when looking at the specs.

    Game: Holds all of the information about the ongoing game.
        - Variables:
            + deck - An array of all of the different cards. Emptied by Deal(). Recreated at the beginning of each Hand.
            + hand_rank - A queue of the different Player objects. As each Player takes their turn they are removed from the head of the queue and placed at the back.
        - Methods:
            + Setup() - Each Player is randomly assigned values from the deck until all players are ranked in order.
                        Ties are resolved, with the loser taking the next-highest rank.
            + Deal() - Starting with the GD, each player (in order of rank) is given a random card until the deck is empty.
            + Revolution() - Checks for revolution condition and prompts the player that could declare revolution.
            + Tax() - Prompts GD and LD for choice of cards and determines which of the GP and LP's cards will be exchanged.
            + Play_Hand(hand_rank) - Creates a Hand object and replaces hand_rank when the Hand object's Play() method returns.

    Hand: Represents a series of rounds in which players attempt to empty their hands.
        - Variables:
            + hand_rank - A copy of the Game-level hand_rank.
            + next_hand_rank - A queue that is populated as Players go out of the current Hand. Is returned by the Play() method.
        - Methods:
            + Play() - Creates Round objects and runs Query_For_Play for each player in hand_rank. Removes each player and places them at the back of hand_rank.
                       Would use a while len(hand_rank) > 0 to loop over the players. As each round finishes, the Cycle_To_Leader() method is run.
            + Cycle_To_Leader(Player) -  Used to make sure that the next Round starts with the leader from the last.
                                         Pops, peeks, and pushes users until the leader as at the front of hand_rank.

    Round: Represents the current round that is being played.
        - Variables:
            + current_play - The set of cards that was most recently played. Starts as Null at the beginning of each round.
            + leader - repesents the player with the current highest play. Changes each time current_play is topped.
        - Methods:
            + Query_For_Play(Player) - Prompts the Player if they want to top or pass.
                                       Uses the Check_Can_Top Player class method to check if the player can top the current_play.

    Player: Represents a person playing the game.
        - Variables:
            + name - The Player's name.
            + hand - An array of the cards in the player's hand.
            + rank - Optional variable that could be used to store a string of the Player's current rank.
        - Methods:
            + Check_Can_Top(current_play) - Checks if the player currently has any sets of cards that could be used to top the current_play.
