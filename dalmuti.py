from queue import Queue
from random import shuffle
from player import Player
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
    num_players = int(input("Number of Players: "))
    players = []

    for i in range(num_players):
        # name = input("Player {} name: ".format(i+1))
        # players.append(Player(name))
        # Auto-generate player names
        players.append(Player(chr(i + ord('A'))))

    return players


def Rank_Players(players):
    shuffle(players)
    return players


def Deal_Cards(players, deck):
    shuffle(deck)
    num_cards = len(deck)

    for i in range(num_cards):
        p = players[i % len(players)]
        p.Add_Cards_To_Hand([deck[0]])
        deck.pop(0)

    deck = Initialize_Deck()


def Revolution(players):

    for p in players:
        if p.hand.get(13) == 2:
            decision = input("Do you want a revolution? (Yes or No): ")

            while True:
                if decision.lower() == "yes":
                    if p is players[-1]:
                        players.reverse()
                    return True
                elif decision.lower() == "no":
                    return False
                else:
                    decision = input(
                        "Could you try that again? Yes or No please: ")

    return False


def Tax_Player(player, num_to_tax):
    cards = []

    hand = player.Get_Hand_As_List()

    for i in range(num_to_tax):
        cards.append(hand.pop(0))

    player.Remove_Cards_From_Hand(cards)
    return cards


def Calculate_Taxes(players):
    bad_cards = players[0].Prompt_For_Cards(
        "Select two cards that you wish to dispose of: ", 2)
    good_cards = Tax_Player(players[-1], 2)
    players[-1].Add_Cards_To_Hand(bad_cards)
    players[0].Add_Cards_To_Hand(good_cards)

    bad_cards = players[1].Prompt_For_Cards(
        "Select one cards that you wish to dispose of: ", 1)
    good_cards = Tax_Player(players[-2], 1)
    players[-2].Add_Cards_To_Hand(bad_cards)
    players[1].Add_Cards_To_Hand(good_cards)


def Setup(players, deck):

    Deal_Cards(players, deck)

    for p in players:
        print(p.name, reduce(lambda x, y: x + y, p.hand.values()), p.hand)

    if not Revolution(players):
        print("All the world shall be taxed!")
        Calculate_Taxes(players)


def main():
    hand_rank = Queue()
    deck = Initialize_Deck()
    players = Rank_Players(Get_Players())

    Setup(players, deck)

    for p in players:
        hand_rank.put(p)

    num_players = hand_rank.qsize()

    for i in range(num_players):
        p = hand_rank.get()
        print(p.name, reduce(lambda x, y: x + y, p.hand.values()), p.hand)


if __name__ == "__main__":
    main()
