from random import shuffle
from player import Player
from hand import Hand
from functools import reduce


def Initialize_Deck():
    '''
        Generates a list of 78 values that range in value from 1 to 12.
        Two jokers, with a value of 13, are also added.
    '''
    deck = []

    for index in range(13):
        for i in range(index):
            deck.append(index)

    deck.extend([13, 13])

    return deck


def Get_Players():
    '''
        Generates a list of named player objects.
        Can be used to query the user for names.
    '''
    num_players = int(input("Number of Players: "))
    players = []

    for i in range(num_players):
        name = input("Player {} name: ".format(i + 1))
        players.append(Player(name))
        # Auto-generate player names
        # players.append(Player(chr(i + ord('A'))))

    return players


def Rank_Players(players):
    '''
        Simply randomizes the order of the players.
        Created as a seperate function to allow for
        different methods of randomization in the
        future.
    '''
    shuffle(players)
    return players


def Deal_Cards(players, deck):
    '''
        Randomizes the order of the deck and then distributes
        the cards, beginning with the highest ranked player.
    '''
    shuffle(deck)
    num_cards = len(deck)

    for i in range(num_cards):
        p = players[i % len(players)]
        p.Add_Cards_To_Hand([deck[0]])
        deck.pop(0)

    deck = Initialize_Deck()


def Revolution(players):
    '''
        Checks to see if one of the player holds both "joker" cards,
        then asks that player if they want to skip the taxation phase.
        If the player accepts and they are the lowest ranked player,
        rank is also reversed.
    '''

    for p in players:
        if p.hand.get(13) == 2:

            decision = p.Prompt_For_Boolean("Do you want a revolution?")

            if decision:
                if p is players[-1]:
                    players.reverse()

            return decision


def Tax_Player(player, num_to_tax):
    '''
        Removes a given number of the best cards
        from a given players hand and returns them
        as a list.
    '''

    cards = []

    hand = player.Get_Hand_As_List()

    for i in range(num_to_tax):
        cards.append(hand.pop(0))

    player.Remove_Cards_From_Hand(cards)
    return cards


def Calculate_And_Collect_Taxes(players):
    '''
        Provides a framework for the process of taxation.
        Taxation is static and always affects players that
        occupy particular spots in the ranking, so the function
        has hard-coded values. The repetition of code is painful,
        but is more legible than most alternatives in my opinion.
    '''

    # GD taxes the GP
    bad_cards = players[0].Prompt_For_Cards(
        "Select two cards that you wish to dispose of: ", 2)
    good_cards = Tax_Player(players[-1], 2)
    # Players exchange 2 cards.
    players[-1].Add_Cards_To_Hand(bad_cards)
    players[0].Add_Cards_To_Hand(good_cards)

    # LD taxes the LP
    bad_card = players[1].Prompt_For_Cards(
        "Select one cards that you wish to dispose of: ", 1)
    good_card = Tax_Player(players[-2], 1)
    # Players exchange a card.
    players[-2].Add_Cards_To_Hand(bad_card)
    players[1].Add_Cards_To_Hand(good_card)


def Setup(players):
    '''
        Wrapper function for the different tasks that
        need to take place before each game begins.
    '''

    deck = Initialize_Deck()

    Deal_Cards(players, deck)

    for p in players:
        print(p.name, reduce(lambda x, y: x + y, p.hand.values()), p.hand)

    if not Revolution(players):
        print("All the world shall be taxed!")
        Calculate_And_Collect_Taxes(players)


def main():

    players = Rank_Players(Get_Players())
    while players is not None:

        Setup(players)
        hand = Hand(players)
        players = hand.Play_Hand()


if __name__ == "__main__":
    main()
