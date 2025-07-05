# 31 Card Game Program
# Written by Joshua Santy, 7/6/2022

# This code assumes that the first person to go directly after being dealt cards knocks.
# You can still use this if you want to knock in the first round even if you aren't the first person to go


"""
TO USE THIS CODE:
1. Go to https://www.programiz.com/python-programming/online-compiler/
2. Clear the existing code that's on the left side (where it says main.py)
3. In its place, copy and paste this entire code WITHOUT ALTERING (ctrl+a, ctrl+c, ctrl+v)
4. Press run
5. On the right side of the screen (under Shell), the program will ask you how many players you want (maximum of 13)
6. Press ENTER
7. It will then ask how many games you want to run (the more the better: 1,000 games is a good estimate; 10,000 will be very precise)
8. Press ENTER
9. The program will give you the results of the average score of the other players, and hence what score it is safe to knock on.
10. The program also gives you the 75th and 25th percentiles that you can base your chances of winning on
11. Thanks!
"""

"""
ASSUMPTIONS:
    - If there is any positive point differential available, the player 
    will take it and not risk drawing from the deck for a possibly higher score

    - The player will discard the lowest value card that doesn't contribute 
    to the score, ignoring what suit the next player may need
"""

import math
import random


def increment_turn_variables(deck_draw: bool):
    """Increment turn tracking variables after the player takes a card"""
    global player_hand_idx, current_player_idx, current_player, upcard_index
    scores[current_player_idx] = hand_value
    player_hand_idx = (3 * current_player)
    current_player += 1
    current_player_idx += 1
    if deck_draw:
        # Increment the deck index (because a card was drawn from the deck)
        upcard_index += 1


def get_lowest_card(cards: list[tuple]) -> tuple[int, str]:
    """Get the lowest-value card from the provided list, and return its value and suit"""
    worst_card = min(cards, key=lambda card: card[0])
    return worst_card[0], worst_card[1]


def draw_card_no_shared_suits():  # add 3 of a kind
    global upcard_suit, upcard_value, hand_value

    value_groups = [deck[player_hand_idx][0], deck[player_hand_idx + 1][0], deck[player_hand_idx + 2][0],
                    deck[-upcard_index - 1][0]]

    # If the drawn card matches suit with card 1:
    if (deck[-upcard_index - 1][1]) == deck[player_hand_idx][1]:
        # If the drawn card and card 1 combined aren't the highest value (or tied for highest):
        if (deck[-upcard_index - 1][0] + deck[player_hand_idx][0]) > max(value_groups):
            hand_value = (deck[-upcard_index - 1][0]) + (deck[player_hand_idx][0])
            # Discard the lowest of the two non-matching cards
            upcard_value, upcard_suit = get_lowest_card([deck[player_hand_idx + 1], deck[player_hand_idx + 2]])


    # If the drawn card matches suit with card 2:
    elif (deck[-upcard_index - 1][1]) == deck[player_hand_idx + 1][1]:
        # If the drawn card and card 2 combined are the maximum value:
        if ((deck[-upcard_index - 1][0]) + deck[player_hand_idx + 1][0]) > max(value_groups):
            hand_value = (deck[-upcard_index - 1][0]) + (deck[player_hand_idx + 1][0])
            # Discard the lowest of the two non-matching cards
            upcard_value, upcard_suit = get_lowest_card([deck[player_hand_idx], deck[player_hand_idx + 2]])

    # If the drawn card matches suit with card 3:
    elif (deck[-upcard_index - 1][1]) == deck[player_hand_idx + 2][1]:
        # If the drawn card and card 3 combined are the maximum value:
        if ((deck[-upcard_index - 1][0]) + deck[player_hand_idx + 2][0]) > max(value_groups):
            hand_value = (deck[-upcard_index - 1][0]) + (deck[player_hand_idx + 2][0])

            # Discard the lowest of the two non-matching cards
            upcard_value, upcard_suit = get_lowest_card([deck[player_hand_idx + 1], deck[player_hand_idx]])

    # If the card matches no suits, or if the combination isn't the maximum value:
    else:
        hand_value = max(value_groups)
        # Discard the lowest card
        upcard_value, upcard_suit = get_lowest_card(
            [deck[player_hand_idx], deck[player_hand_idx + 1], deck[player_hand_idx + 2], deck[-upcard_index - 1]]
        )

    # Increment the turn variables, and move on to the next player
    increment_turn_variables(deck_draw=True)


def draw_card_1_2_share_suits():
    global upcard_suit, upcard_value, hand_value

    value_groups = [deck[-upcard_index - 1][0], deck[player_hand_idx][0] + deck[player_hand_idx + 1][0],
                    deck[player_hand_idx + 2][0]]

    # If the drawn card shares no suits:
    if deck[-upcard_index - 1][1] != deck[player_hand_idx][1] and deck[-upcard_index - 1][1] != \
            deck[player_hand_idx + 2][1]:
        hand_value = max(value_groups)

        if deck[-upcard_index - 1][0] == min(value_groups):
            # Discard the drawn card
            upcard_value = deck[-upcard_index - 1][0]
            upcard_suit = deck[-upcard_index - 1][1]
        elif deck[player_hand_idx + 2][0] == min(value_groups):
            # Discard card 3
            upcard_value = deck[player_hand_idx + 2][0]
            upcard_suit = deck[player_hand_idx + 2][1]
        else:
            # Discard the lowest of the matching cards
            upcard_value, upcard_suit = get_lowest_card([deck[player_hand_idx], deck[player_hand_idx + 1]])

    # If the drawn card shares a suit with card 3:
    elif deck[-upcard_index - 1][1] == deck[player_hand_idx + 2][1]:
        hand_value = max(deck[-upcard_index - 1][0] + deck[player_hand_idx + 2][0],
                         deck[player_hand_idx][0] + deck[player_hand_idx + 1][0])

        # If the drawn card and card 3 combined are greater than cards 1 and 2 combined:
        if deck[-upcard_index - 1][0] + deck[player_hand_idx + 2][0] > deck[player_hand_idx][0] + \
                deck[player_hand_idx + 1][0]:

            # Discard the lesser of cards 1 and 2
            upcard_value, upcard_suit = get_lowest_card([deck[player_hand_idx], deck[player_hand_idx + 1]])

        # If the drawn card and card 3 combined are less than cards 1 and 2 combined
        elif deck[-upcard_index - 1][0] + deck[player_hand_idx + 2][0] < deck[player_hand_idx][0] + \
                deck[player_hand_idx + 1][0]:

            # Discard the lesser of the drawn card and card 3
            upcard_value, upcard_suit = get_lowest_card([deck[-upcard_index - 1], deck[player_hand_idx + 2]])

        # If the combination of the drawn card and card 3 is equal to the combination of cards 1 and 2:
        else:
            # Discard the lowest card
            upcard_value, upcard_suit = get_lowest_card(
                [deck[-upcard_index - 1], deck[player_hand_idx + 2], deck[player_hand_idx], deck[player_hand_idx + 1]]
            )

    # If the drawn card shares a suit with cards 1 and 2:
    else:
        hand_value = max(deck[-upcard_index - 1][0] + deck[player_hand_idx][0] + deck[player_hand_idx + 1][0],
                         deck[player_hand_idx + 2][0])

        # If the drawn card, card 1, and card 2 combined are greater than the value of card 3:
        if deck[-upcard_index - 1][0] + deck[player_hand_idx][0] + deck[player_hand_idx + 1][0] > \
                deck[player_hand_idx + 2][0]:
            # Discard card 3
            upcard_value = deck[player_hand_idx + 2][0]
            upcard_suit = deck[player_hand_idx + 2][1]

        # If the drawn card, card 1, and card 2 combined are NOT the maximum value:
        else:
            # Discard the least of cards 1, 2, and the drawn card
            upcard_value, upcard_suit = get_lowest_card(
                [deck[-upcard_index - 1], deck[player_hand_idx], deck[player_hand_idx + 1]]
            )

    # Increment the turn variables, and move on to the next player
    increment_turn_variables(deck_draw=True)


def draw_card_1_3_share_suits():
    global upcard_suit, upcard_value, hand_value

    value_groups = [deck[-upcard_index - 1][0], deck[player_hand_idx][0] + deck[player_hand_idx + 2][0],
                    deck[player_hand_idx + 1][0]]

    # If the drawn card shares no suits:
    if deck[-upcard_index - 1][1] != deck[player_hand_idx + 1][1] and deck[-upcard_index - 1][1] != \
            deck[player_hand_idx + 2][1]:
        hand_value = max(value_groups)

        # If the drawn card is the minimum value:
        if deck[-upcard_index - 1][0] == min(value_groups):
            # Discard the drawn card
            upcard_value = deck[-upcard_index - 1][0]
            upcard_suit = deck[-upcard_index - 1][1]
        # If card 2 is the minimum value:
        elif deck[player_hand_idx + 1][0] == min(value_groups):
            # Discard card 2
            upcard_value = deck[player_hand_idx + 1][0]
            upcard_suit = deck[player_hand_idx + 1][1]
        # If cards 1 and 3 combined are the minimum value:
        else:
            # Discard the lesser of cards 1 and 3
            upcard_value, upcard_suit = get_lowest_card([deck[player_hand_idx], deck[player_hand_idx + 2]])

    # If the drawn card shares a suit with card 2:
    elif deck[-upcard_index - 1][1] == deck[player_hand_idx + 1][1]:
        hand_value = max(deck[-upcard_index - 1][0] + deck[player_hand_idx + 1][0],
                         deck[player_hand_idx][0] + deck[player_hand_idx + 2][0])
        # If the combination of the drawn card and card 2 is greater than the combination of cards 1 and 3:
        if deck[-upcard_index - 1][0] + deck[player_hand_idx + 1][0] > deck[player_hand_idx][0] + \
                deck[player_hand_idx + 2][0]:

            # Discard the lesser of cards 1 and 3
            upcard_value, upcard_suit = get_lowest_card([deck[player_hand_idx], deck[player_hand_idx + 2]])

        # If the combination of the drawn card and card 2 is less than the combination of cards 1 and 3:
        elif deck[-upcard_index - 1][0] + deck[player_hand_idx + 1][0] < deck[player_hand_idx][0] + \
                deck[player_hand_idx + 2][0]:

            # Discard the lesser of card 2 and the drawn card
            upcard_value, upcard_suit = get_lowest_card([deck[-upcard_index - 1], deck[player_hand_idx + 1]])

        # If the combination of the drawn card and card 2 is equal to the combination of cards 1 and 3:
        else:
            # Discard the lowest card
            upcard_value, upcard_suit = get_lowest_card(
                [deck[-upcard_index - 1], deck[player_hand_idx + 1], deck[player_hand_idx], deck[player_hand_idx + 2]]
            )


    # If the drawn card shares a suit with cards 1 and 3:
    else:
        hand_value = max(deck[-upcard_index - 1][0] + deck[player_hand_idx][0] + deck[player_hand_idx + 2][0],
                         deck[player_hand_idx + 1][0])
        # If the combination of cards 1, 3, and the drawn card is greater than the value of card 2:
        if deck[-upcard_index - 1][0] + deck[player_hand_idx][0] + deck[player_hand_idx + 2][0] > \
                deck[player_hand_idx + 1][0]:
            # Discard card 2
            upcard_value = deck[player_hand_idx + 1][0]
            upcard_suit = deck[player_hand_idx + 1][1]

        # If the combination of cards 1, 3, and the drawn card is less than the value of card 2:
        else:
            # Discard the least of cards 1, 3, and the drawn card
            upcard_value, upcard_suit = get_lowest_card(
                [deck[-upcard_index - 1], deck[player_hand_idx], deck[player_hand_idx + 2]]
            )

    # Increment the turn variables, and move on to the next player
    increment_turn_variables(deck_draw=True)


def draw_card_2_3_share_suits():
    global upcard_suit, upcard_value, hand_value

    value_groups = [deck[-upcard_index - 1][0], deck[player_hand_idx + 2][0] + deck[player_hand_idx + 1][0],
                    deck[player_hand_idx][0]]

    # If the drawn card shares no suits:
    if deck[-upcard_index - 1][1] != deck[player_hand_idx][1] and deck[-upcard_index - 1][1] != \
            deck[player_hand_idx + 2][1]:
        hand_value = max(value_groups)
        # If the drawn card is the lowest value:
        if deck[-upcard_index - 1][0] == min(value_groups):
            # Discard the drawn card
            upcard_value = deck[-upcard_index - 1][0]
            upcard_suit = deck[-upcard_index - 1][1]
        # If card 1 is the lowest value:
        elif deck[player_hand_idx][0] == min(value_groups):
            # Discard card 1
            upcard_value = deck[player_hand_idx][0]
            upcard_suit = deck[player_hand_idx][1]
        # If cards 2 and 3 combined are the lowest value:
        else:
            # Discard the lesser of cards 2 and 3
            upcard_value, upcard_suit = get_lowest_card([deck[player_hand_idx + 1], deck[player_hand_idx + 2]])

    # If the drawn card shares a suit with card 1:
    elif deck[-upcard_index - 1][1] == deck[player_hand_idx][1]:
        hand_value = max(deck[-upcard_index - 1][0] + deck[player_hand_idx][0],
                         deck[player_hand_idx + 1][0] + deck[player_hand_idx + 2][0])

        # If card 1 and the drawn card combined are greater than cards 2 and 3 combined:
        if deck[-upcard_index - 1][0] + deck[player_hand_idx][0] > deck[player_hand_idx + 1][0] + \
                deck[player_hand_idx + 2][0]:

            # Discard the lesser of cards 2 and 3
            upcard_value, upcard_suit = get_lowest_card([deck[player_hand_idx + 1], deck[player_hand_idx + 2]])

        # If card 1 and the drawn card combined are less than cards 2 and 3 combined:
        elif deck[-upcard_index - 1][0] + deck[player_hand_idx][0] < deck[player_hand_idx + 1][0] + \
                deck[player_hand_idx + 2][0]:

            # Discard the lesser of card 1 and the drawn card
            upcard_value, upcard_suit = get_lowest_card([deck[-upcard_index - 1], deck[player_hand_idx]])

        # If card 1 and the drawn card combined are equal to cards 2 and 3 combined:
        else:
            # Discard the lowest card
            upcard_value, upcard_suit = get_lowest_card(
                [deck[-upcard_index - 1], deck[player_hand_idx + 1], deck[player_hand_idx], deck[player_hand_idx + 2]]
            )

    # If the drawn card shares a suit with cards 2 and 3:
    else:
        hand_value = max(deck[-upcard_index - 1][0] + deck[player_hand_idx + 1][0] + deck[player_hand_idx + 2][0],
                         deck[player_hand_idx][0])
        # If cards 2, 3, and the drawn card combined are greater than the value of card 1:
        if deck[-upcard_index - 1][0] + deck[player_hand_idx + 1][0] + deck[player_hand_idx + 2][0] > \
                deck[player_hand_idx][0]:
            # Discard card 1
            upcard_value = deck[player_hand_idx][0]
            upcard_suit = deck[player_hand_idx][1]

        # If cards 2, 3, and the drawn card combined are less than or equal to the value of card 1:
        else:
            # Discard the least of cards 2, 3, and the drawn card
            upcard_value, upcard_suit = get_lowest_card(
                [deck[-upcard_index - 1], deck[player_hand_idx + 1], deck[player_hand_idx + 2]]
            )

    # Increment the turn variables, and move on to the next player
    increment_turn_variables(deck_draw=True)


player_count = int(input('Enter number of players: '))
iterations = int(input('Enter number of iterations: '))
all_total = 0
total_scores = []
for _ in range(iterations):
    # Types: 1 = number, 2 = 10, 3 = jack, 4 = queen, 5 = king, 6 = ace
    # Each item: (Value, Suit, Type)
    deck = [
        (5, 'Club', 1), (10, 'Club', 2), (11, 'Diamond', 6), (10, 'Heart', 2), (6, 'Spade', 1), (3, 'Spade', 1),
        (10, 'Club', 3), (10, 'Spade', 2), (2, 'Spade', 1), (8, 'Spade', 1), (7, 'Club', 1), (3, 'Heart', 1),
        (4, 'Spade', 1), (11, 'Club', 6), (5, 'Diamond', 1), (10, 'Heart', 3), (10, 'Diamond', 2), (9, 'Spade', 1),
        (9, 'Club', 1), (6, 'Heart', 1), (4, 'Heart', 1), (10, 'Diamond', 3), (3, 'Diamond', 1), (6, 'Club', 1),
        (11, 'Heart', 6), (10, 'Spade', 3), (10, 'Diamond', 4), (10, 'Spade', 4), (5, 'Spade', 1), (7, 'Heart', 1),
        (6, 'Diamond', 1), (7, 'Diamond', 1), (4, 'Club', 1), (8, 'Heart', 1), (11, 'Spade', 6), (2, 'Club', 1),
        (3, 'Club', 1), (10, 'Heart', 4), (10, 'Club', 4), (8, 'Club', 1), (2, 'Heart', 1), (9, 'Diamond', 1),
        (7, 'Spade', 1), (2, 'Diamond', 1), (10, 'Spade', 5), (4, 'Diamond', 1), (10, 'Heart', 5), (9, 'Heart', 1),
        (8, 'Diamond', 1), (10, 'Club', 5), (5, 'Heart', 1), (10, 'Diamond', 5)
    ]
    deck = random.sample(deck, k=len(deck))  # Shuffle the deck
    scores = []

    # First player starts
    player_hand_idx = 0
    current_player = 1

    # "Deal" a hand to each player and calculate their hand value(s)
    while current_player <= player_count:
        hand_value = 0
        # No matching suits:
        if (
                deck[player_hand_idx + 1][1] != deck[player_hand_idx + 2][1]  # S2 != S3
                and deck[player_hand_idx][1] != deck[player_hand_idx + 1][1]  # S1 != S2
                and deck[player_hand_idx][1] != deck[player_hand_idx + 2][1]  # S1 != S3
        ):
            # Hand is worth the largest card's value
            hand_value = max(deck[player_hand_idx][0], deck[player_hand_idx + 1][0], deck[player_hand_idx + 2][0])

        # All matching suit:
        elif (
                deck[player_hand_idx + 1][1] == deck[player_hand_idx + 2][1]  # S2 = S3
                and deck[player_hand_idx][1] == deck[player_hand_idx + 1][1]  # S1 = S2
                and deck[player_hand_idx + 1][1] == deck[player_hand_idx + 2][1]  # S2 = S3
        ):
            # Hand is worth the sum of all card values
            hand_value = deck[player_hand_idx][0] + deck[player_hand_idx + 1][0] + deck[player_hand_idx + 2][0]

        # At least 1 matching suit:
        else:
            # Hand is worth the sum of the matching suits, or the largest single card (whichever is higher)
            if deck[player_hand_idx][1] == deck[player_hand_idx + 1][1]:  # S1 = S2
                # Either (H1 + H2) or H3
                hand_value = max(deck[player_hand_idx][0] + deck[player_hand_idx + 1][0], deck[player_hand_idx + 2][0])
            elif deck[player_hand_idx][1] == deck[player_hand_idx + 2][1]:
                # Either (H1 + H3) or H2
                hand_value = max(deck[player_hand_idx][0] + deck[player_hand_idx + 2][0], deck[player_hand_idx + 1][0])
            else:
                # Either (H2 + H3) or H1
                hand_value = max(deck[player_hand_idx + 1][0] + deck[player_hand_idx + 2][0], deck[player_hand_idx][0])

        # Hand value is now accurate, add it to the totals
        scores.append(hand_value)
        total_scores.append(hand_value)

        # Move on to the next player
        player_hand_idx = (3 * current_player)
        current_player += 1

    # Second draw, first player knocks (Skip P1):
    current_player = 2
    current_player_idx = 1
    player_hand_idx = 3
    upcard_index = 1

    # Update the initial face-up card
    upcard_value = deck[-upcard_index][0]
    upcard_suit = deck[-upcard_index][1]

    # Each player draws, discards, and recalculates hand value
    while current_player <= player_count:
        hand_value = 0

        # All hand cards are the same suit:
        if (
                deck[player_hand_idx + 1][1] == deck[player_hand_idx + 2][1]  # S2 = S3
                and deck[player_hand_idx][1] == deck[player_hand_idx + 1][1]  # S1 = S2
                and deck[player_hand_idx + 1][1] == deck[player_hand_idx + 2][1]  # S2 = S3
        ):
            # If face-up card doesn't share the same suit:
            if upcard_suit != deck[player_hand_idx][1]:
                hand_card_values = [deck[player_hand_idx][0], deck[player_hand_idx + 1][0],
                                    deck[player_hand_idx + 2][0]]
                # If face-up card is greater than (or equal to) the sum of all 3 cards:
                if upcard_value >= sum(hand_card_values):
                    hand_value = upcard_value
                    # Discard the lowest card
                    upcard_value, upcard_suit = get_lowest_card(
                        [deck[player_hand_idx], deck[player_hand_idx + 1], deck[player_hand_idx + 2]]
                    )

                    # Increment the turn variables, and move on to the next player
                    increment_turn_variables(deck_draw=False)
                    continue

                # If face-up card is not greater than or equal to the sum of all 3 cards:
                else:
                    # Draw a card from the top of the deck
                    # If drawn card is the same suit:
                    if deck[-upcard_index - 1][1] == deck[player_hand_idx][1]:
                        hand_card_values = [deck[-upcard_index - 1][0], deck[player_hand_idx][0],
                                            deck[player_hand_idx + 1][0], deck[player_hand_idx + 2][0]]
                        # Discard the lowest card
                        upcard_value, upcard_suit = get_lowest_card(
                            [deck[-upcard_index - 1], deck[player_hand_idx], deck[player_hand_idx + 1],
                             deck[player_hand_idx + 2]]
                        )
                        hand_value = sum(hand_card_values) - upcard_value

                        # Increment the turn variables, and move on to the next player
                        increment_turn_variables(deck_draw=True)
                        continue

                    # If drawn card doesn't share a suit:
                    else:
                        # If the drawn card is better than the sum of the three cards:
                        hand_card_values = [deck[player_hand_idx][0], deck[player_hand_idx + 1][0],
                                            deck[player_hand_idx + 2][0]]
                        if deck[-upcard_index - 1][0] >= sum(hand_card_values):
                            # Draw from the deck, discarding the worst card
                            hand_value = deck[-upcard_index - 1][0]
                            upcard_value, upcard_suit = get_lowest_card(
                                [deck[player_hand_idx], deck[player_hand_idx + 1], deck[player_hand_idx + 2]]
                            )

                            # Increment the turn variables, and move on to the next player
                            increment_turn_variables(deck_draw=True)
                            continue

                        # If new card is worse the sum of the three cards:
                        else:
                            # Hand value is unchanged, and the face-up card remains the same
                            hand_value = deck[player_hand_idx][0] + deck[player_hand_idx + 1][0] + \
                                         deck[player_hand_idx + 2][0]
                            upcard_value = deck[-upcard_index - 1][0]
                            upcard_suit = deck[-upcard_index - 1][1]
                            increment_turn_variables(deck_draw=True)
                            continue

            # If face-up card is the same suit:
            elif upcard_suit == deck[player_hand_idx][1]:
                # If face-up is greater than at least 1 of the cards [otherwise newcard]:
                if (
                        upcard_value > deck[player_hand_idx][0]
                        or upcard_value > deck[player_hand_idx + 1][0]
                        or upcard_value > deck[player_hand_idx + 2][0]
                ):
                    hand_card_values = [deck[player_hand_idx][0], deck[player_hand_idx + 1][0],
                                        deck[player_hand_idx + 2][0]]

                    # Discard the lowest card
                    worst_value, worst_suit = get_lowest_card(
                        [deck[player_hand_idx], deck[player_hand_idx + 1], deck[player_hand_idx + 2]]
                    )

                    hand_value = (hand_value + sum(hand_card_values) + upcard_value) - worst_value
                    upcard_value = worst_value
                    upcard_suit = worst_suit

                # If face-up card is not greater than any of the cards:
                # (Draw a card from the top of the deck)
                else:
                    hand_card_values = [deck[-upcard_index - 1][0], deck[player_hand_idx][0],
                                        deck[player_hand_idx + 1][0], deck[player_hand_idx + 2][0]]
                    # If the drawn card shares a suit:
                    if deck[-upcard_index - 1][1] == deck[player_hand_idx][1]:
                        # Discard the lowest value card
                        worst_value, worst_suit = get_lowest_card(
                            [deck[-upcard_index - 1], deck[player_hand_idx], deck[player_hand_idx + 1],
                             deck[player_hand_idx + 2]]
                        )
                        hand_value = sum(hand_card_values) - worst_value
                        upcard_value = worst_value
                        upcard_suit = worst_suit

                    # If the drawn card doesn't share a suit:
                    else:
                        # If the drawn card is greater than or equal to the sum of the three cards:
                        if deck[-upcard_index - 1][0] >= (
                                deck[player_hand_idx][0] + deck[player_hand_idx + 1][0] + deck[player_hand_idx + 2][0]):
                            hand_value = deck[-upcard_index - 1][0]

                            # Discard the lowest of the cards already in hand
                            upcard_value, upcard_suit = get_lowest_card(
                                [deck[player_hand_idx], deck[player_hand_idx + 1], deck[player_hand_idx + 2]]
                            )

                        # If the drawn card is worse than the sum of the three cards:
                        else:
                            hand_value = deck[player_hand_idx][0] + deck[player_hand_idx + 1][0] + \
                                         deck[player_hand_idx + 2][0]
                            # Discard the drawn card, leaving hand the same
                            upcard_value = deck[-upcard_index - 1][0]
                            upcard_suit = deck[-upcard_index - 1][1]

                # Increment the turn variables, and move to the next player
                increment_turn_variables(deck_draw=False)
                continue

        # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # No matching suits:
        if deck[player_hand_idx][1] != deck[player_hand_idx + 2][1] and deck[player_hand_idx][1] != \
                deck[player_hand_idx + 1][1] and deck[player_hand_idx + 1][1] != deck[player_hand_idx + 2][1]:

            hand_card_values = [deck[player_hand_idx][0], deck[player_hand_idx + 1][0],
                                deck[player_hand_idx + 2][0]]

            # Check for three of a kind:
            if deck[player_hand_idx][2] == 1:
                three_of_a_kind = deck[player_hand_idx][0] == deck[player_hand_idx + 1][0] == deck[player_hand_idx + 2][
                    0]
            else:
                # For face cards, use card "type" (index 2) instead of base number
                three_of_a_kind = deck[player_hand_idx][2] == deck[player_hand_idx + 1][2] == deck[player_hand_idx + 2][
                    2]

            # If player has a three of a kind:
            if three_of_a_kind:
                hand_value = 30.5
                # Discard the drawn card
                upcard_value = deck[-upcard_index - 1][0]
                upcard_suit = deck[-upcard_index - 1][1]
                increment_turn_variables(deck_draw=True)
                continue

            # If the face-up card doesn't share a suit:
            if upcard_suit != deck[player_hand_idx][1] and upcard_suit != deck[player_hand_idx + 1][
                1] and upcard_suit != deck[player_hand_idx + 2][1]:
                # TODO: Perhaps if upcard is lower than 5 then you choose from the deck, not just the upcard
                # If the face-up card is the highest:
                if upcard_value > max(hand_card_values):
                    hand_value = upcard_value

                    # Discard the lowest card in hand
                    upcard_value, upcard_suit = get_lowest_card(
                        [deck[player_hand_idx], deck[player_hand_idx + 1], deck[player_hand_idx + 2]]
                    )

                    # Increment the turn variables, and move to the next player
                    increment_turn_variables(deck_draw=False)
                    continue

                # If the drawn card is the lowest or tied with the highest:
                else:
                    draw_card_no_shared_suits()
                    continue

            # If the face-up card shares a suit with card 1:
            elif upcard_suit == deck[player_hand_idx][1]:
                # If the face-up card and card 1 combined are greater than either of the other cards:
                if (upcard_value + deck[player_hand_idx][0]) > max(hand_card_values):
                    hand_value = upcard_value + deck[player_hand_idx][0]

                    # Discard the lowest card
                    upcard_value, upcard_suit = get_lowest_card(
                        [deck[player_hand_idx], deck[player_hand_idx + 1], deck[player_hand_idx + 2]]
                    )

                    # Increment the turn variables, and move on to the next player
                    increment_turn_variables(deck_draw=False)
                    continue

                # If the face-up card and card 1 combined are NOT the maximum value:
                else:
                    draw_card_no_shared_suits()
                    continue

            # If the face-up card shares a suit with card 2:
            elif upcard_suit == deck[player_hand_idx + 1][1]:
                # If the face-up card and card 2 combined are greater than either of the other cards:
                if (upcard_value + deck[player_hand_idx + 1][0]) > max(hand_card_values):
                    hand_value = upcard_value + deck[player_hand_idx + 1][0]

                    # Discard the lowest of the two remaining cards
                    upcard_value, upcard_suit = get_lowest_card([deck[player_hand_idx], deck[player_hand_idx + 2]])

                    # Increment the turn variables, and move on to the next player
                    increment_turn_variables(deck_draw=False)
                    continue
                # If the face-up card and card 2 combined are NOT the maximum value:
                else:
                    draw_card_no_shared_suits()
                    continue

            # If the face-up card shares a suit with card 3:
            elif upcard_suit == deck[player_hand_idx + 2][1]:
                # If the face-up card and card 3 combined are greater than either of the other cards:
                if (upcard_value + deck[player_hand_idx + 2][0]) > max(hand_card_values):
                    hand_value = upcard_value + deck[player_hand_idx + 2][0]

                    # Discard the lowest of the two remaining cards
                    upcard_value, upcard_suit = get_lowest_card([deck[player_hand_idx + 1], deck[player_hand_idx]])

                    # Increment the turn variables, and move on to the next player
                    increment_turn_variables(deck_draw=False)
                    continue
                # If the face-up card and card 3 combined are NOT the maximum value:
                else:
                    draw_card_no_shared_suits()
                    continue

        # --------------------------------------------------------------------------------------------------------------------------------------------------
        # If cards 1 and 2 share suits:
        if deck[player_hand_idx][1] == deck[player_hand_idx + 1][1] and deck[player_hand_idx][1] != \
                deck[player_hand_idx + 2][1]:

            # If the face-up card shares no suits:
            if upcard_suit != deck[player_hand_idx + 2][1] and upcard_suit != deck[player_hand_idx + 1][1]:
                # If the face-up card is the maximum value:
                if upcard_value >= deck[player_hand_idx + 2][0] and upcard_value >= (
                        deck[player_hand_idx + 1][0] + deck[player_hand_idx][0]):
                    hand_value = upcard_value

                    # Discard the lowest card
                    upcard_value, upcard_suit = get_lowest_card(
                        [deck[player_hand_idx + 1], deck[player_hand_idx], deck[player_hand_idx + 2]]
                    )

                    # Increment the turn variables, and move on to the next player
                    increment_turn_variables(deck_draw=False)
                    continue

                # If the face-up card is NOT the maximum value:
                else:
                    draw_card_1_2_share_suits()
                    continue

            # If the face-up card shares a suit with card 3:
            elif upcard_suit == deck[player_hand_idx + 2][1]:
                # If the face-up card and card 3 are greater than cards 1 and 2:
                if (upcard_value + deck[player_hand_idx + 2][0]) > (
                        deck[player_hand_idx][0] + deck[player_hand_idx + 1][0]):
                    hand_value = upcard_value + deck[player_hand_idx + 2][0]

                    # Discard the lesser of cards 1 and 2
                    upcard_value, upcard_suit = get_lowest_card([deck[player_hand_idx], deck[player_hand_idx + 1]])

                    # Increment the turn variables, and move on to the next player
                    increment_turn_variables(deck_draw=False)
                    continue

                # If cards 1 and 2 combined are greater than the face-up card and card 3 combined:
                else:
                    draw_card_1_2_share_suits()
                    continue

            # If the face-up card shares a suit with cards 1 and 2:
            elif upcard_suit == deck[player_hand_idx + 1][1]:
                # If cards 1, 2 and the face-up card combined are greater than or equal to card 3:
                if (upcard_value + deck[player_hand_idx + 1][0] + (deck[player_hand_idx][0]) >=
                        deck[player_hand_idx + 2][0]):
                    hand_value = upcard_value + deck[player_hand_idx + 1][0] + deck[player_hand_idx][0]
                    # Discard card 3
                    upcard_value = deck[player_hand_idx + 2][0]
                    upcard_suit = deck[player_hand_idx + 2][1]

                    # Increment the turn variables, and move on to the next player
                    increment_turn_variables(deck_draw=False)
                    continue
                # If card 3 is greater than the cards 1, 2, and the face-up card combined:
                else:
                    draw_card_1_2_share_suits()
                    continue

        # --------------------------------------------------------------------------------------------------------------------------
        # If cards 1 and 3 share suits:
        if deck[player_hand_idx][1] == deck[player_hand_idx + 2][1] and deck[player_hand_idx][1] != \
                deck[player_hand_idx + 1][1] and deck[player_hand_idx + 1][1] != deck[player_hand_idx + 2][1]:

            hand_card_values = [deck[player_hand_idx][0], deck[player_hand_idx + 1][0],
                                deck[player_hand_idx + 2][0]]

            # If the face-up card shares no suits:
            if upcard_suit != deck[player_hand_idx + 2][1] and upcard_suit != deck[player_hand_idx + 1][1]:
                # If the face-up card is the maximum value:
                if upcard_value >= deck[player_hand_idx + 1][0] and upcard_value >= (
                        deck[player_hand_idx + 2][0] + deck[player_hand_idx][0]):
                    hand_value = upcard_value

                    # Discard the lowest card
                    upcard_value, upcard_suit = get_lowest_card(
                        [deck[player_hand_idx], deck[player_hand_idx + 1], deck[player_hand_idx + 2]]
                    )

                    # Increment the turn variables, and move on to the next player
                    increment_turn_variables(deck_draw=False)
                    continue

                # If card 2 or the combination of cards 1 and 3 are max:
                else:
                    draw_card_1_3_share_suits()
                    continue

            # If the face-up card shares a suit with card 2:
            elif upcard_suit == deck[player_hand_idx + 1][1]:
                # If the face-up card and card 2 combined are greater than cards 1 and 3 combined:
                if (upcard_value + deck[player_hand_idx + 1][0]) > (
                        deck[player_hand_idx][0] + deck[player_hand_idx + 2][0]):
                    hand_value = upcard_value + deck[player_hand_idx + 1][0]

                    # Discard the lesser of cards 1 and 3
                    upcard_value, upcard_suit = get_lowest_card([deck[player_hand_idx], deck[player_hand_idx + 2]])

                    # Increment the turn variables, and move on to the next player
                    increment_turn_variables(deck_draw=False)
                    continue

                # If cards 1 and 3 combined are greater than the face-up card and card 2 combined:
                else:
                    draw_card_1_3_share_suits()
                    continue

            # If the face-up card shares a suit with cards 1 and 3:
            elif upcard_suit == deck[player_hand_idx][1]:
                # If the face-up card and cards 1 and 3 combined are greater than or equal to card 2:
                if (upcard_value + deck[player_hand_idx + 2][0] + (deck[player_hand_idx][0]) >=
                        deck[player_hand_idx + 1][0]):
                    hand_value = upcard_value + deck[player_hand_idx + 2][0] + deck[player_hand_idx][0]
                    # Discard card 2
                    upcard_value = deck[player_hand_idx + 1][0]
                    upcard_suit = deck[player_hand_idx + 1][1]

                    # Increment the turn variables, and move on to the next player
                    increment_turn_variables(deck_draw=False)
                    continue

                # If card 2 is greater than the face-up card, card 1, and card 3 combined:
                else:
                    draw_card_1_3_share_suits()
                    continue

        # ------------------------------------------------------------------------------------------------------------------------
        # If cards 2 and 3 share suits:
        if deck[player_hand_idx][1] != deck[player_hand_idx + 2][1] and deck[player_hand_idx][1] != \
                deck[player_hand_idx + 1][1] and deck[player_hand_idx + 1][1] == deck[player_hand_idx + 2][1]:

            # If the face-up card shares no suits:
            if upcard_suit != deck[player_hand_idx][1] and upcard_suit != deck[player_hand_idx + 1][1]:
                # If the face-up card is the maximum value:
                if upcard_value >= deck[player_hand_idx][0] and upcard_value >= (
                        deck[player_hand_idx + 1][0] + deck[player_hand_idx + 2][0]):
                    hand_value = upcard_value

                    # Discard the lowest card
                    upcard_value, upcard_suit = get_lowest_card(
                        [deck[player_hand_idx + 1], deck[player_hand_idx], deck[player_hand_idx + 2]]
                    )

                    # Increment the turn variables, and move on to the next player
                    increment_turn_variables(deck_draw=False)
                    continue

                # If card 1 or cards 3 and 2 combined are max:
                else:
                    draw_card_2_3_share_suits()
                    continue

            # If the face-up card shares a suit with card 1:
            elif upcard_suit == deck[player_hand_idx][1]:
                # If the face-up card and card 1 combined are greater than cards 2 and 3 combined:
                if (upcard_value + deck[player_hand_idx][0]) > (
                        deck[player_hand_idx + 2][0] + deck[player_hand_idx + 1][0]):
                    hand_value = upcard_value + deck[player_hand_idx][0]

                    # Discard the lesser of cards 2 and 3
                    upcard_value, upcard_suit = get_lowest_card([deck[player_hand_idx + 1], deck[player_hand_idx + 2]])

                    # Increment the turn variables, and move on to the next player
                    increment_turn_variables(deck_draw=False)
                    continue

                # If cards 3 and 2 combined are greater than the face-up card and card 1 combined:
                else:
                    draw_card_2_3_share_suits()
                    continue

            # If the face-up card shares a suit with cards 3 and 2:
            elif upcard_suit == deck[player_hand_idx + 1][1]:
                # If the face-up card, card 3, and card 2 combined are greater than or equal to card 1:
                if (upcard_value + deck[player_hand_idx + 1][0] + (deck[player_hand_idx + 2][0]) >=
                        deck[player_hand_idx][0]):
                    hand_value = upcard_value + deck[player_hand_idx + 1][0] + deck[player_hand_idx + 2][0]
                    # Discard card 1
                    upcard_value = deck[player_hand_idx][0]
                    upcard_suit = deck[player_hand_idx][1]

                    # Increment the turn variables, and move on to the next player
                    increment_turn_variables(deck_draw=False)
                    continue

                # If card 1 is greater than the face-up card, card 3, and card 2 combined:
                else:
                    draw_card_2_3_share_suits()
                    continue
    # -------------------------------------------------------------------------------------------------------------------------

    other_players_total_score = sum(scores[1:])
    average = round(other_players_total_score / (player_count - 1), 10)

    all_total += float(average)

all_total = round(all_total / iterations, 10)
print(f"\nAverage score of other players after having knocked: {all_total}\n")

# Find the standard deviation
score_sum = sum([(total_scores[h] - all_total) ** 2 for h in range(iterations)])
std_dev = math.sqrt((score_sum / iterations))
print(f'Standard Deviation: {std_dev}\n')

# 75th and 25th percentile:
# 75th percentile = mean + (z * standard deviation), where z is taken from a table (https://www.statology.org/calculate-percentile-from-mean-standard-deviation/)
# Remember, 75th percentile means that 75% of all the answers are below yours, and 25% are above

percent75 = all_total + (0.67 * std_dev)
percent25 = all_total + (-0.67 * std_dev)
print(f'75th percentile: {percent75}')
print(f'25th percentile: {percent25}')

# MrJoshie333 out o/
