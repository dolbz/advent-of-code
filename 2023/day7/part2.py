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
                # Now a Joker and worth 1 for comparison with other cards
                current_card = 1
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
        # Keep separate count of jokers because of their special properties
        joker_count = 0

        for card in self.cards:
            if card == 1:
                joker_count += 1
            else:
                card_counts[card] += 1

        count_values = list(card_counts.values())

        max_count = 1
        for count in count_values:
            if count > max_count:
                max_count = count

        hand_type = HandType.HIGH_CARD

        if max_count == 5:
            hand_type = HandType.FIVE_OF_A_KIND
        elif max_count == 4:
            hand_type = HandType.FOUR_OF_A_KIND
        elif max_count == 3:
            found_two = False
            for count_value in count_values:
                if count_value == 2:
                    found_two = True

            if found_two:
                hand_type = HandType.FULL_HOUSE
            else:
                hand_type = HandType.THREE_OF_A_KIND
        elif max_count == 2 and len(count_values) + joker_count == 3:
            hand_type = HandType.TWO_PAIR
        elif max_count == 2 and len(count_values) + joker_count == 4:
            hand_type = HandType.ONE_PAIR
        else:
            hand_type = HandType.HIGH_CARD

        # upgrade hand with Jacks
        for i in range(joker_count):
            if hand_type == HandType.ONE_PAIR:
                hand_type = HandType.THREE_OF_A_KIND
            elif hand_type == HandType.TWO_PAIR:
                hand_type = HandType.FULL_HOUSE
            elif hand_type == HandType.THREE_OF_A_KIND:
                hand_type = HandType.FOUR_OF_A_KIND
            else:
                hand_type = HandType(hand_type.value + 1)

            if hand_type == HandType.FIVE_OF_A_KIND:
                break

        return hand_type

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
