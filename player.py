import re


class Player:

    def __init__(self, name):
        self.name = name
        self.hand = {}
        self.rank = None

    def Display_Hand(self):
        human_readable_hand = []

        for key in self.hand.keys():
            for i in range(self.hand[key]):
                human_readable_hand.append(key)

        print(human_readable_hand)

    def Check_Has_Cards(self, cards_to_remove):
        print(cards_to_remove)
        for k, v in cards_to_remove.items():
            if self.hand.get(k) is None:
                print("{} is not in your hand, try again.".format(str(k)))
                return False
            elif self.hand.get(k) < v:
                print(
                    "You don't have that many {}'s in your hand".format(str(k)))
                return False

        return True

    def Add_Cards_To_Hand(self, cards):
        for card in cards:
            if self.hand.__contains__(card):
                self.hand[card] += 1
            else:
                self.hand[card] = 1

    def Remove_Cards_From_Hand(self, cards):
        print(cards)
        for card in cards:
            num_cards = self.hand.get(card)
            if num_cards == 1:
                del self.hand[card]
            else:
                self.hand[card] -= 1

    def Prompt_For_Cards(self, message, num_to_remove=None):

        while True:
            self.Display_Hand()
            cards = input("{}, {}".format(self.name, message))
            cards = re.findall("\\b1[0-3]\\b|\\b[1-9]\\b", cards)

            if num_to_remove is not None:
                if len(cards) != num_to_remove:
                    example = ""
                    for i in range(num_to_remove):
                        example += " 12"
                    print(
                        "Please specify {} cards. Example:{}".format(str(num_to_remove), example))
                    continue

            cards = [int(c) for c in cards]

            cards_to_remove = {}

            for c in cards:
                if cards_to_remove.__contains__(c):
                    cards_to_remove[c] += 1
                else:
                    cards_to_remove[c] = 1

            if self.Check_Has_Cards(cards_to_remove):
                self.Remove_Cards_From_Hand(cards)
                return cards
            else:
                continue
