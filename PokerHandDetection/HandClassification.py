import math
import re


poker_hands = ["High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind", "EMPTY FOR EASE", "Straight Flush", "Royal Flush"]
poker_card_indices = {'Q': 12, 'K': 13, 'A': 14, 'J': 11}

def detect_hand(cards):
    hand_strength = 0
    card_count = {}
    suite_count = set()
    regex = r'[HDSC]'
    for card in cards:
        rank = re.split(regex, card)[0]
        if rank.isalpha():
            rank = poker_card_indices[rank]
        else:
            rank = int(rank)
        suite_count.add(re.findall(regex, card)[0])
        if rank not in card_count.keys():
            card_count[rank] = 1
        else:
            card_count[rank] += 1
    classed_cards = 0
    # Checking for pairs
    for key, value in card_count.items():
        if value > 1:
            hand_strength += math.floor((value - 1)*1.5)
            classed_cards += value
        if value == 4 or classed_cards > 4:
            hand_strength += math.floor(value/2) + 1
    card_arr = sorted(card_count.keys())
    # Checking for flush
    if len(suite_count) == 1:
        hand_strength += 5
    # Checking for straight
    if len(card_arr) == 5 and (card_arr[-1] - card_arr[0] == 4):
        # Checking for Royal Flush
        if card_arr[-1] == 14:
            hand_strength += 1
        hand_strength += 4
    print(poker_hands[hand_strength], hand_strength, suite_count)
    return hand_strength


if __name__ == "__main__":
    detect_hand(["AH", "4C", "5D", "7S", "KH"]) # High Card
    detect_hand(["AH", "4C", "5D", "7S", "7H"]) # One Pair
    detect_hand(["AH", "4C", "4D", "7S", "7H"]) # Two Pair
    detect_hand(["AH", "4C", "7D", "7S", "7H"]) # Three of a Kind
    detect_hand(["10H", "9C", "7D", "8S", "6H"]) # Straight
    detect_hand(["10H", "1H", "7H", "4H", "6H"]) # Flush
    detect_hand(["AH", "AC", "AD", "7S", "7H"]) # Full House
    detect_hand(["AH", "AC", "AD", "AS", "7H"]) # Four of a Kind
    detect_hand(["KH", "QH", "JH", "10H", "9H"]) # Straight Flush
    detect_hand(["AH", "KH", "QH", "JH", "10H"]) # Royal Flush
