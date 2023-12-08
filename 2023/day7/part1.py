from enum import Enum
from collections import defaultdict


class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


class Hand:
    def __init__(self, handLine) -> None:
        handLine_parts = handLine.split(" ")

        cards_string = handLine_parts[0]
        self.bid = int(handLine_parts[1])

        cards = []

        for i in range(5):
            current_card_str = cards_string[i]

            if current_card_str == "T":
                current_card = 10
            elif current_card_str == "J":
                current_card = 11
            elif current_card_str == "Q":
                current_card = 12
            elif current_card_str == "K":
                current_card = 13
            elif current_card_str == "A":
                current_card = 14
            else:
                current_card = int(current_card_str)

            cards.append(current_card)
        self.cards = cards

        self.hand_type = self.determine_hand()

    def determine_hand(self):
        card_counts = defaultdict(int)

        for card in self.cards:
            card_counts[card] += 1

        count_values = list(card_counts.values())

        max_count = 1
        for count in count_values:
            if count > max_count:
                max_count = count

        if max_count == 5:
            return HandType.FIVE_OF_A_KIND
        elif max_count == 4:
            return HandType.FOUR_OF_A_KIND
        elif max_count == 3:
            if count_values[0] == 2 or count_values[1] == 2 or count_values[2] == 2:
                return HandType.FULL_HOUSE
            else:
                return HandType.THREE_OF_A_KIND
        elif max_count == 2 and len(count_values) == 3:
            return HandType.TWO_PAIR
        elif max_count == 2 and len(count_values) == 4:
            return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD

    def __lt__(self, other):
        if self.hand_type.value < other.hand_type.value:
            return True
        elif self.hand_type.value > other.hand_type.value:
            return False

        for i in range(5):
            if self.cards[i] == other.cards[i]:
                continue

            return self.cards[i] < other.cards[i]


file = open("input.txt", "r")
lines = file.read().splitlines()

all_hands = []

for line in lines:
    all_hands.append(Hand(line))

sorted_all_hands = sorted(all_hands)
winnings = 0

for i in range(len(sorted_all_hands)):
    winnings += sorted_all_hands[i].bid * (i + 1)

print(winnings)
