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
import dataclasses
import typing

"""
ASSUMPTIONS:
    - If there is any positive point differential available, the player 
    will take it and not risk drawing from the deck for a possibly higher score

    - The player will discard the lowest value card that doesn't contribute 
    to the score, ignoring what suit the next player may need
"""

import math
import random

Card = typing.NewType("Card", tuple[int, str, int])

@dataclasses.dataclass
class GameState:
    current_player: int
    upcard_index: int
    player_scores: list[int]
    deck: list[Card]
    deck_draws: int = 1  # Starts after the upcard

    @property
    def current_player_idx(self):
        return self.current_player - 1

    @property
    def player_hand_idx(self):
        return self.current_player_idx * 3

    @property
    def upcard_value(self):
        return self.deck[self.upcard_index][0]

    @property
    def upcard_suit(self):
        return self.deck[self.upcard_index][1]

    def get_card_index(self, card: Card):
        return self.deck.index(card)

def increment_turn_variables(game_state: GameState, hand_value: float, discarded_card: Card, deck_draw: bool):
    """Increment turn tracking variables after the player takes/discards a card"""
    game_state.upcard_index = game_state.get_card_index(discarded_card)
    game_state.player_scores[game_state.current_player_idx] = hand_value
    game_state.current_player += 1
    if deck_draw:
        game_state.deck_draws += 1


def get_lowest_card(cards: list[Card]) -> Card:
    """Get the lowest-value card from the provided list, and return its value and suit"""
    return min(cards, key=lambda card: card[0])


def get_hand_value(cards: list[Card]) -> float:
    """Get the value of a hand, accounting for matching suits and three-of-a-kinds"""
    values = [card[0] for card in cards]

    # Three of a kind
    if values[0] == values[1] == values[2]:
        return 30.5

    suit_groups = {}
    for value, suit, _ in cards:
        # Add each card to its suit group (or create a new group if it's the first)
        suit_groups.setdefault(suit, []).append(value)

    # The hand is worth the sum of the largest group of same-suit cards
    return max(sum(group) for group in suit_groups.values())


def draw_card_no_shared_suits(game_state: GameState):  # add 3 of a kind
    drawn = game_state.deck[-1 - game_state.deck_draws]
    drawn_val, drawn_suit = drawn[0], drawn[1]

    c1 = game_state.deck[game_state.player_hand_idx]
    c2 = game_state.deck[game_state.player_hand_idx + 1]
    c3 = game_state.deck[game_state.player_hand_idx + 2]

    value_groups = [c1[0], c2[0], c3[0], drawn_val]

    # If the drawn card matches suit with card 1:
    if drawn_suit == c1[1] and (drawn_val + c1[0]) > max(value_groups):
        # If the drawn card and card 1 combined are the highest value:
        hand_value = drawn_val + (c1[0])
        # Discard the lowest of the two non-matching cards
        discard_card = get_lowest_card([c2, c3])

    # If the drawn card matches suit with card 2:
    elif drawn_suit == c2[1] and (drawn_val + c2[0]) > max(value_groups):
        # If the drawn card and card 2 combined are the maximum value:
        hand_value = drawn_val + (c2[0])
        # Discard the lowest of the two non-matching cards
        discard_card = get_lowest_card([c1, c3])

    # If the drawn card matches suit with card 3:
    elif drawn_suit == c3[1] and (drawn_val + c3[0]) > max(value_groups):
        # If the drawn card and card 3 combined are the maximum value:
        hand_value = drawn_val + (c3[0])
        # Discard the lowest of the two non-matching cards
        discard_card = get_lowest_card([c2, c1])

    # If the card matches no suits, or if the combination isn't the maximum value:
    else:
        hand_value = max(value_groups)
        # Discard the lowest card
        discard_card = get_lowest_card([c1, c2, c3, drawn])

    # Increment the turn variables, and move on to the next player
    increment_turn_variables(game_state, hand_value, discard_card, deck_draw=True)


def draw_card_1_2_share_suits(game_state: GameState):
    drawn = game_state.deck[-1 - game_state.deck_draws]
    drawn_val, drawn_suit = drawn[0], drawn[1]

    c1 = game_state.deck[game_state.player_hand_idx]
    c2 = game_state.deck[game_state.player_hand_idx + 1]
    c3 = game_state.deck[game_state.player_hand_idx + 2]

    value_groups = [drawn_val, c1[0] + c2[0], c3[0]]

    # If the drawn card shares no suits:
    if drawn_suit != c1[1] and drawn_suit != c3[1]:
        hand_value = max(value_groups)

        if drawn_val == min(value_groups):
            # Discard the drawn card
            discard_card = drawn
        elif c3[0] == min(value_groups):
            # Discard card 3
            discard_card = c3
        else:
            # Discard the lowest of the matching cards
            discard_card = get_lowest_card([c1, c2])

    # If the drawn card shares a suit with card 3:
    elif drawn_suit == c3[1]:
        hand_value = max(drawn_val + c3[0], c1[0] + c2[0])

        # If the drawn card and card 3 combined are greater than cards 1 and 2 combined:
        if drawn_val + c3[0] > c1[0] + c2[0]:
            # Discard the lesser of cards 1 and 2
            discard_card = get_lowest_card([c1, c2])

        # If the drawn card and card 3 combined are less than cards 1 and 2 combined
        elif drawn_val + c3[0] < c1[0] + c2[0]:
            # Discard the lesser of the drawn card and card 3
            discard_card = get_lowest_card([drawn, c3])

        # If the combination of the drawn card and card 3 is equal to the combination of cards 1 and 2:
        else:
            # Discard the lowest card
            discard_card = get_lowest_card([drawn, c3, c1, c2])

    # If the drawn card shares a suit with cards 1 and 2:
    else:
        hand_value = max(drawn_val + c1[0] + c2[0], c3[0])

        # If the drawn card, card 1, and card 2 combined are greater than the value of card 3:
        if drawn_val + c1[0] + c2[0] > c3[0]:
            # Discard card 3
            discard_card = c3

        # If the drawn card, card 1, and card 2 combined are NOT the maximum value:
        else:
            # Discard the least of cards 1, 2, and the drawn card
            discard_card = get_lowest_card([drawn, c1, c2])

    # Increment the turn variables, and move on to the next player
    increment_turn_variables(game_state, hand_value, discard_card, deck_draw=True)


def draw_card_1_3_share_suits(game_state: GameState):
    drawn = game_state.deck[-1 - game_state.deck_draws]
    drawn_val, drawn_suit = drawn[0], drawn[1]

    c1 = game_state.deck[game_state.player_hand_idx]
    c2 = game_state.deck[game_state.player_hand_idx + 1]
    c3 = game_state.deck[game_state.player_hand_idx + 2]

    value_groups = [drawn_val, c1[0] + c3[0], c2[0]]

    # If the drawn card shares no suits:
    if drawn_suit != c2[1] and drawn_suit != c3[1]:
        hand_value = max(value_groups)

        # If the drawn card is the minimum value:
        if drawn_val == min(value_groups):
            # Discard the drawn card
            discard_card = drawn
        # If card 2 is the minimum value:
        elif c2[0] == min(value_groups):
            # Discard card 2
            discard_card = c2
        # If cards 1 and 3 combined are the minimum value:
        else:
            # Discard the lesser of cards 1 and 3
            discard_card = get_lowest_card([c1, c3])

    # If the drawn card shares a suit with card 2:
    elif drawn_suit == c2[1]:
        hand_value = max(drawn_val + c2[0], c1[0] + c3[0])
        # If the combination of the drawn card and card 2 is greater than the combination of cards 1 and 3:
        if drawn_val + c2[0] > c1[0] + c3[0]:
            # Discard the lesser of cards 1 and 3
            discard_card = get_lowest_card([c1, c3])

        # If the combination of the drawn card and card 2 is less than the combination of cards 1 and 3:
        elif drawn_val + c2[0] < c1[0] + c3[0]:
            # Discard the lesser of card 2 and the drawn card
            discard_card = get_lowest_card([drawn, c2])

        # If the combination of the drawn card and card 2 is equal to the combination of cards 1 and 3:
        else:
            # Discard the lowest card
            discard_card = get_lowest_card([drawn, c2, c1, c3])


    # If the drawn card shares a suit with cards 1 and 3:
    else:
        hand_value = max(drawn_val + c1[0] + c3[0], c2[0])
        # If the combination of cards 1, 3, and the drawn card is greater than the value of card 2:
        if drawn_val + c1[0] + c3[0] > c2[0]:
            # Discard card 2
            discard_card = c2

        # If the combination of cards 1, 3, and the drawn card is less than the value of card 2:
        else:
            # Discard the least of cards 1, 3, and the drawn card
            discard_card = get_lowest_card([drawn, c1, c3])

    # Increment the turn variables, and move on to the next player
    increment_turn_variables(game_state, hand_value, discard_card, deck_draw=True)


def draw_card_2_3_share_suits(game_state: GameState):
    drawn = game_state.deck[-1 - game_state.deck_draws]
    drawn_val, drawn_suit = drawn[0], drawn[1]

    c1 = game_state.deck[game_state.player_hand_idx]
    c2 = game_state.deck[game_state.player_hand_idx + 1]
    c3 = game_state.deck[game_state.player_hand_idx + 2]

    value_groups = [drawn_val, c3[0] + c2[0], c1[0]]

    # If the drawn card shares no suits:
    if drawn_suit != c1[1] and drawn_suit != c3[1]:
        hand_value = max(value_groups)
        # If the drawn card is the lowest value:
        if drawn_val == min(value_groups):
            # Discard the drawn card
            discard_card = drawn
        # If card 1 is the lowest value:
        elif c1[0] == min(value_groups):
            # Discard card 1
            discard_card = c1
        # If cards 2 and 3 combined are the lowest value:
        else:
            # Discard the lesser of cards 2 and 3
            discard_card = get_lowest_card([c2, c3])

    # If the drawn card shares a suit with card 1:
    elif drawn_suit == c1[1]:
        hand_value = max(drawn_val + c1[0], c2[0] + c3[0])
        # If card 1 and the drawn card combined are greater than cards 2 and 3 combined:
        if drawn_val + c1[0] > c2[0] + c3[0]:
            # Discard the lesser of cards 2 and 3
            discard_card = get_lowest_card([c2, c3])

        # If card 1 and the drawn card combined are less than cards 2 and 3 combined:
        elif drawn_val + c1[0] < c2[0] + c3[0]:
            # Discard the lesser of card 1 and the drawn card
            discard_card = get_lowest_card([drawn, c1])

        # If card 1 and the drawn card combined are equal to cards 2 and 3 combined:
        else:
            # Discard the lowest card
            discard_card = get_lowest_card([drawn, c2, c1, c3])

    # If the drawn card shares a suit with cards 2 and 3:
    else:
        hand_value = max(drawn_val + c2[0] + c3[0], c1[0])
        # If cards 2, 3, and the drawn card combined are greater than the value of card 1:
        if drawn_val + c2[0] + c3[0] > c1[0]:
            # Discard card 1
            discard_card = c1

        # If cards 2, 3, and the drawn card combined are less than or equal to the value of card 1:
        else:
            # Discard the least of cards 2, 3, and the drawn card
            discard_card = get_lowest_card([drawn, c2, c3])

    # Increment the turn variables, and move on to the next player
    increment_turn_variables(game_state, hand_value, discard_card, deck_draw=True)


def update_welford(existing_accumulation: tuple[float, float, float], new_value: float) -> tuple[float, float, float]:
    """Update the accumulation of count, mean, and squared distance from the mean, returning the updated tuple"""
    (count, mean, m2) = existing_accumulation
    count += 1
    delta = new_value - mean
    mean += delta / count
    delta2 = new_value - mean
    m2 += delta * delta2
    return count, mean, m2


def finalize_welford(existing_accumulation: tuple[float, float, float]) -> tuple[float, float, float]:
    """Given the accumulated samples, calculate variance and sample variance using Welford's algorithm"""
    (count, mean, m2) = existing_accumulation
    if count < 2:
        raise ValueError("Not enough data to compute variance using Welford algorithm (needs >2 points)")
    else:
        (mean, variance, sample_variance) = (mean, m2 / count, m2 / (count - 1))
        return mean, variance, sample_variance


############# MAIN FUNCTIONALITY #############
def main():
    player_count = int(input("Enter number of players: "))
    iterations = int(input("Enter number of iterations: "))
    single_player_total = 0
    total_scores = []
    welford_accumulation = (0, 0, 0)

    for turn in range(iterations):
        # Types: 1 = number, 2 = 10, 3 = jack, 4 = queen, 5 = king, 6 = ace
        # Each item: (Value, Suit, Type)
        _deck = [
            (5, "Club", 1), (10, "Club", 2), (11, "Diamond", 6), (10, "Heart", 2), (6, "Spade", 1), (3, "Spade", 1),
            (10, "Club", 3), (10, "Spade", 2), (2, "Spade", 1), (8, "Spade", 1), (7, "Club", 1), (3, "Heart", 1),
            (4, "Spade", 1), (11, "Club", 6), (5, "Diamond", 1), (10, "Heart", 3), (10, "Diamond", 2), (9, "Spade", 1),
            (9, "Club", 1), (6, "Heart", 1), (4, "Heart", 1), (10, "Diamond", 3), (3, "Diamond", 1), (6, "Club", 1),
            (11, "Heart", 6), (10, "Spade", 3), (10, "Diamond", 4), (10, "Spade", 4), (5, "Spade", 1), (7, "Heart", 1),
            (6, "Diamond", 1), (7, "Diamond", 1), (4, "Club", 1), (8, "Heart", 1), (11, "Spade", 6), (2, "Club", 1),
            (3, "Club", 1), (10, "Heart", 4), (10, "Club", 4), (8, "Club", 1), (2, "Heart", 1), (9, "Diamond", 1),
            (7, "Spade", 1), (2, "Diamond", 1), (10, "Spade", 5), (4, "Diamond", 1), (10, "Heart", 5), (9, "Heart", 1),
            (8, "Diamond", 1), (10, "Club", 5), (5, "Heart", 1), (10, "Diamond", 5)
        ]
        random.seed(turn)

        game_state = GameState(
            current_player=1,
            upcard_index=None,
            player_scores=[],
            deck=random.sample(_deck, k=len(_deck))  # Shuffle the deck
        )

        # "Deal" a hand to each player and calculate their hand value(s)
        while game_state.current_player <= player_count:
            c1 = game_state.deck[game_state.player_hand_idx]
            c2 = game_state.deck[game_state.player_hand_idx + 1]
            c3 = game_state.deck[game_state.player_hand_idx + 2]

            # No matching suits:
            if (
                    c2[1] != c3[1]  # S2 != S3
                    and c1[1] != c2[1]  # S1 != S2
                    and c1[1] != c3[1]  # S1 != S3
            ):
                # Hand is worth the largest card's value
                hand_value = max(c1[0], c2[0], c3[0])

            # All matching suit:
            elif (
                    c2[1] == c3[1]  # S2 = S3
                    and c1[1] == c2[1]  # S1 = S2
                    and c2[1] == c3[1]  # S2 = S3
            ):
                # Hand is worth the sum of all card values
                hand_value = c1[0] + c2[0] + c3[0]

            # At least 1 matching suit:
            else:
                # Hand is worth the sum of the matching suits, or the largest single card (whichever is higher)
                if c1[1] == c2[1]:  # S1 = S2
                    # Either (H1 + H2) or H3
                    hand_value = max(c1[0] + c2[0], c3[0])
                elif c1[1] == c3[1]:
                    # Either (H1 + H3) or H2
                    hand_value = max(c1[0] + c3[0], c2[0])
                else:
                    # Either (H2 + H3) or H1
                    hand_value = max(c2[0] + c3[0], c1[0])

            # Hand value is now accurate, add it to the totals
            game_state.player_scores.append(hand_value)
            total_scores.append(hand_value)
            welford_accumulation = update_welford(welford_accumulation, hand_value)

            # Move on to the next player
            game_state.current_player += 1

        # Second draw, first player knocks (Skip P1):
        game_state.current_player = 2

        # Update the initial face-up card (Top of the deck)
        game_state.upcard_index = -1
        print("Initial Upcard:", game_state.deck[game_state.upcard_index])

        # Each player draws, discards, and recalculates hand value
        while game_state.current_player <= player_count:
            drawn = game_state.deck[-1 - game_state.deck_draws]
            c1 = game_state.deck[game_state.player_hand_idx]
            c2 = game_state.deck[game_state.player_hand_idx + 1]
            c3 = game_state.deck[game_state.player_hand_idx + 2]
            print("Drew card:", drawn)
            print("Hand:", c1, c2, c3, drawn)

            hand_value = 0
            # All hand cards are the same suit:
            if (
                    c2[1] == c3[1]  # S2 = S3
                    and c1[1] == c2[1]  # S1 = S2
                    and c2[1] == c3[1]  # S2 = S3
            ):
                # If face-up card doesn't share the same suit:
                if game_state.upcard_suit != c1[1]:
                    hand_card_values = [c1[0], c2[0], c3[0]]
                    # If face-up card is greater than (or equal to) the sum of all 3 cards:
                    if game_state.upcard_value >= sum(hand_card_values):
                        hand_value = game_state.upcard_value
                        # Discard the lowest card
                        discard_card = get_lowest_card([c1, c2, c3])

                        # Increment the turn variables, and move on to the next player
                        increment_turn_variables(game_state, hand_value, discard_card, deck_draw=False)

                    # If face-up card is not greater than or equal to the sum of all 3 cards:
                    else:
                        # Draw a card from the top of the deck
                        # If drawn card is the same suit:
                        if drawn[1] == c1[1]:
                            hand_card_values = [drawn[0], c1[0], c2[0], c3[0]]
                            # Discard the lowest card
                            discard_card = get_lowest_card([drawn, c1, c2, c3])
                            hand_value = sum(hand_card_values) - discard_card[0]

                            # Increment the turn variables, and move on to the next player
                            increment_turn_variables(game_state, hand_value, discard_card, deck_draw=True)

                        # If drawn card doesn't share a suit:
                        else:
                            # If the drawn card is better than the sum of the three cards:
                            hand_card_values = [c1[0], c2[0], c3[0]]
                            if drawn[0] >= sum(hand_card_values):
                                # Draw from the deck, discarding the worst card
                                hand_value = drawn[0]
                                discard_card = get_lowest_card([c1, c2, c3])

                                # Increment the turn variables, and move on to the next player
                                increment_turn_variables(game_state, hand_value, discard_card, deck_draw=True)

                            # If new card is worse the sum of the three cards:
                            else:
                                # Hand value is unchanged, and the face-up card remains the same
                                hand_value = c1[0] + c2[0] + c3[0]
                                discard_card = drawn
                                increment_turn_variables(game_state, hand_value, discard_card, deck_draw=True)

                # If face-up card is the same suit:
                elif game_state.upcard_suit == c1[1]:
                    # If face-up is greater than at least 1 of the cards [otherwise newcard]:
                    if game_state.upcard_value > c1[0] or game_state.upcard_value > c2[0] or game_state.upcard_value > c3[0]:
                        hand_card_values = [c1[0], c2[0], c3[0]]

                        # Discard the lowest card
                        discard_card = get_lowest_card([c1, c2, c3])

                        hand_value = (hand_value + sum(hand_card_values) + game_state.upcard_value) - discard_card[0]

                    # If face-up card is not greater than any of the cards:
                    # (Draw a card from the top of the deck)
                    else:
                        hand_card_values = [drawn[0], c1[0], c2[0], c3[0]]
                        # If the drawn card shares a suit:
                        if drawn[1] == c1[1]:
                            # Discard the lowest value card
                            discard_card = get_lowest_card([drawn, c1, c2, c3])
                            hand_value = sum(hand_card_values) - discard_card[0]

                        # If the drawn card doesn't share a suit:
                        else:
                            # If the drawn card is greater than or equal to the sum of the three cards:
                            if drawn[0] >= (c1[0] + c2[0] + c3[0]):
                                hand_value = drawn[0]

                                # Discard the lowest of the cards already in hand
                                discard_card = get_lowest_card([c1, c2, c3])

                            # If the drawn card is worse than the sum of the three cards:
                            else:
                                hand_value = c1[0] + c2[0] + c3[0]
                                # Discard the drawn card, leaving hand the same
                                discard_card = drawn

                    # Increment the turn variables, and move to the next player
                    increment_turn_variables(game_state, hand_value, discard_card, deck_draw=False)

            # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # No matching suits:
            if c1[1] != c3[1] and c1[1] != c2[1] and c2[1] != c3[1]:
                hand_card_values = [c1[0], c2[0], c3[0]]

                # Check for three of a kind:
                if c1[2] == 1:
                    three_of_a_kind = c1[0] == c2[0] == c3[0]
                else:
                    # For face cards, use card "type" (index 2) instead of base number
                    three_of_a_kind = c1[2] == c2[2] == c3[2]

                # If player has a three of a kind:
                if three_of_a_kind:
                    hand_value = 30.5
                    # Discard the drawn card
                    discard_card = drawn
                    increment_turn_variables(game_state, hand_value, discard_card, deck_draw=True)

                # If the face-up card doesn't share a suit:
                elif game_state.upcard_suit != c1[1] and game_state.upcard_suit != c2[1] and game_state.upcard_suit != c3[1]:
                    # TODO: Perhaps if upcard is lower than 5 then you choose from the deck, not just the upcard
                    # If the face-up card is the highest:
                    if game_state.upcard_value > max(hand_card_values):
                        hand_value = game_state.upcard_value

                        # Discard the lowest card in hand
                        discard_card = get_lowest_card([c1, c2, c3])

                        # Increment the turn variables, and move to the next player
                        increment_turn_variables(game_state, hand_value, discard_card, deck_draw=False)

                    # If the drawn card is the lowest or tied with the highest:
                    else:
                        draw_card_no_shared_suits(game_state)

                # If the face-up card shares a suit with card 1:
                elif game_state.upcard_suit == c1[1]:
                    # If the face-up card and card 1 combined are greater than either of the other cards:
                    if (game_state.upcard_value + c1[0]) > max(hand_card_values):
                        hand_value = game_state.upcard_value + c1[0]

                        # Discard the lowest card
                        discard_card = get_lowest_card([c1, c2, c3])

                        # Increment the turn variables, and move on to the next player
                        increment_turn_variables(game_state, hand_value, discard_card, deck_draw=False)

                    # If the face-up card and card 1 combined are NOT the maximum value:
                    else:
                        draw_card_no_shared_suits(game_state)

                # If the face-up card shares a suit with card 2:
                elif game_state.upcard_suit == c2[1]:
                    # If the face-up card and card 2 combined are greater than either of the other cards:
                    if (game_state.upcard_value + c2[0]) > max(hand_card_values):
                        hand_value = game_state.upcard_value + c2[0]

                        # Discard the lowest of the two remaining cards
                        discard_card = get_lowest_card([c1, c3])

                        # Increment the turn variables, and move on to the next player
                        increment_turn_variables(game_state, hand_value, discard_card, deck_draw=False)
                    # If the face-up card and card 2 combined are NOT the maximum value:
                    else:
                        draw_card_no_shared_suits(game_state)

                # If the face-up card shares a suit with card 3:
                elif game_state.upcard_suit == c3[1]:
                    # If the face-up card and card 3 combined are greater than either of the other cards:
                    if (game_state.upcard_value + c3[0]) > max(hand_card_values):
                        hand_value = game_state.upcard_value + c3[0]

                        # Discard the lowest of the two remaining cards
                        discard_card = get_lowest_card([c2, c1])

                        # Increment the turn variables, and move on to the next player
                        increment_turn_variables(game_state, hand_value, discard_card, deck_draw=False)
                    # If the face-up card and card 3 combined are NOT the maximum value:
                    else:
                        draw_card_no_shared_suits(game_state)

            # --------------------------------------------------------------------------------------------------------------------------------------------------
            # If cards 1 and 2 share suits:
            if c1[1] == c2[1] and c1[1] != c3[1]:

                # If the face-up card shares no suits:
                if game_state.upcard_suit != c3[1] and game_state.upcard_suit != c2[1]:
                    # If the face-up card is the maximum value:
                    if game_state.upcard_value >= c3[0] and game_state.upcard_value >= (c2[0] + c1[0]):
                        hand_value = game_state.upcard_value

                        # Discard the lowest card
                        discard_card = get_lowest_card([c2, c1, c3])

                        # Increment the turn variables, and move on to the next player
                        increment_turn_variables(game_state, hand_value, discard_card, deck_draw=False)

                    # If the face-up card is NOT the maximum value:
                    else:
                        draw_card_1_2_share_suits(game_state)

                # If the face-up card shares a suit with card 3:
                elif game_state.upcard_suit == c3[1]:
                    # If the face-up card and card 3 are greater than cards 1 and 2:
                    if (game_state.upcard_value + c3[0]) > (c1[0] + c2[0]):
                        hand_value = game_state.upcard_value + c3[0]

                        # Discard the lesser of cards 1 and 2
                        discard_card = get_lowest_card([c1, c2])

                        # Increment the turn variables, and move on to the next player
                        increment_turn_variables(game_state, hand_value, discard_card, deck_draw=False)

                    # If cards 1 and 2 combined are greater than the face-up card and card 3 combined:
                    else:
                        draw_card_1_2_share_suits(game_state)

                # If the face-up card shares a suit with cards 1 and 2:
                elif game_state.upcard_suit == c2[1]:
                    # If cards 1, 2 and the face-up card combined are greater than or equal to card 3:
                    if game_state.upcard_value + c2[0] + (c1[0]) >= c3[0]:
                        hand_value = game_state.upcard_value + c2[0] + c1[0]
                        # Discard card 3
                        discard_card = c3

                        # Increment the turn variables, and move on to the next player
                        increment_turn_variables(game_state, hand_value, discard_card, deck_draw=False)
                    # If card 3 is greater than the cards 1, 2, and the face-up card combined:
                    else:
                        draw_card_1_2_share_suits(game_state)

            # --------------------------------------------------------------------------------------------------------------------------
            # If cards 1 and 3 share suits:
            if c1[1] == c3[1] and c1[1] != c2[1] and c2[1] != c3[1]:

                hand_card_values = [c1[0], c2[0], c3[0]]

                # If the face-up card shares no suits:
                if game_state.upcard_suit != c3[1] and game_state.upcard_suit != c2[1]:
                    # If the face-up card is the maximum value:
                    if game_state.upcard_value >= c2[0] and game_state.upcard_value >= (c3[0] + c1[0]):
                        hand_value = game_state.upcard_value

                        # Discard the lowest card
                        discard_card = get_lowest_card([c1, c2, c3])

                        # Increment the turn variables, and move on to the next player
                        increment_turn_variables(game_state, hand_value, discard_card, deck_draw=False)

                    # If card 2 or the combination of cards 1 and 3 are max:
                    else:
                        draw_card_1_3_share_suits(game_state)

                # If the face-up card shares a suit with card 2:
                elif game_state.upcard_suit == c2[1]:
                    # If the face-up card and card 2 combined are greater than cards 1 and 3 combined:
                    if (game_state.upcard_value + c2[0]) > (c1[0] + c3[0]):
                        hand_value = game_state.upcard_value + c2[0]

                        # Discard the lesser of cards 1 and 3
                        discard_card = get_lowest_card([c1, c3])

                        # Increment the turn variables, and move on to the next player
                        increment_turn_variables(game_state, hand_value, discard_card, deck_draw=False)

                    # If cards 1 and 3 combined are greater than the face-up card and card 2 combined:
                    else:
                        draw_card_1_3_share_suits(game_state)

                # If the face-up card shares a suit with cards 1 and 3:
                elif game_state.upcard_suit == c1[1]:
                    # If the face-up card and cards 1 and 3 combined are greater than or equal to card 2:
                    if game_state.upcard_value + c3[0] + (c1[0]) >= c2[0]:
                        hand_value = game_state.upcard_value + c3[0] + c1[0]
                        # Discard card 2
                        discard_card = c2

                        # Increment the turn variables, and move on to the next player
                        increment_turn_variables(game_state, hand_value, discard_card, deck_draw=False)

                    # If card 2 is greater than the face-up card, card 1, and card 3 combined:
                    else:
                        draw_card_1_3_share_suits(game_state)

            # ------------------------------------------------------------------------------------------------------------------------
            # If cards 2 and 3 share suits:
            if c1[1] != c3[1] and c1[1] != c2[1] and c2[1] == c3[1]:

                # If the face-up card shares no suits:
                if game_state.upcard_suit != c1[1] and game_state.upcard_suit != c2[1]:
                    # If the face-up card is the maximum value:
                    if game_state.upcard_value >= c1[0] and game_state.upcard_value >= (c2[0] + c3[0]):
                        hand_value = game_state.upcard_value

                        # Discard the lowest card
                        discard_card = get_lowest_card([c2, c1, c3])

                        # Increment the turn variables, and move on to the next player
                        increment_turn_variables(game_state, hand_value, discard_card, deck_draw=False)

                    # If card 1 or cards 3 and 2 combined are max:
                    else:
                        draw_card_2_3_share_suits(game_state)

                # If the face-up card shares a suit with card 1:
                elif game_state.upcard_suit == c1[1]:
                    # If the face-up card and card 1 combined are greater than cards 2 and 3 combined:
                    if (game_state.upcard_value + c1[0]) > (c3[0] + c2[0]):
                        hand_value = game_state.upcard_value + c1[0]

                        # Discard the lesser of cards 2 and 3
                        discard_card = get_lowest_card([c2, c3])

                        # Increment the turn variables, and move on to the next player
                        increment_turn_variables(game_state, hand_value, discard_card, deck_draw=False)

                    # If cards 3 and 2 combined are greater than the face-up card and card 1 combined:
                    else:
                        draw_card_2_3_share_suits(game_state)

                # If the face-up card shares a suit with cards 3 and 2:
                elif game_state.upcard_suit == c2[1]:
                    # If the face-up card, card 3, and card 2 combined are greater than or equal to card 1:
                    if game_state.upcard_value + c2[0] + (c3[0]) >= c1[0]:
                        hand_value = game_state.upcard_value + c2[0] + c3[0]
                        # Discard card 1
                        discard_card = c1

                        # Increment the turn variables, and move on to the next player
                        increment_turn_variables(game_state, hand_value, discard_card, deck_draw=False)

                    # If card 1 is greater than the face-up card, card 3, and card 2 combined:
                    else:
                        draw_card_2_3_share_suits(game_state)
        # -------------------------------------------------------------------------------------------------------------------------

        other_players_total_score = sum(game_state.player_scores[1:])
        average = other_players_total_score / (player_count - 1)

        single_player_total += float(average)

    average_player_score = single_player_total / iterations
    print(f"\nAverage score of other players after having knocked: {average_player_score:.10f}\n")

    # # Find the standard deviation (Naive Method)
    # score_sum = sum([(total_scores[h] - average_player_score) ** 2 for h in range(iterations)])
    # std_dev = math.sqrt((score_sum / iterations))
    # print(f"Standard Deviation (Single-Pass): {std_dev}\n")
    #
    # # Find the standard deviation (Two-Pass Method)
    # n = len(total_scores)
    # mean = sum(total_scores) / n
    # variance = sum((x - mean) ** 2 for x in total_scores) / (n - 1)
    # std_dev_two_pass = math.sqrt(variance)
    # print(f"Standard Deviation (Two-Pass): {std_dev_two_pass}\n")

    # Welford's algorithm
    mean, variance, sample_variance = finalize_welford(welford_accumulation)
    std_dev = math.sqrt(variance)
    print(f"Standard Deviation: {std_dev}\n")

    # 75th and 25th percentile:
    # 75th percentile = mean + (z * standard deviation), where z is taken from a table
    # Remember, 75th percentile means that 75% of all the answers are below yours, and 25% are above
    percent75 = average_player_score + (0.6745 * std_dev)
    percent25 = average_player_score + (-0.6745 * std_dev)
    print(f"75th percentile: {percent75}")
    print(f"25th percentile: {percent25}")

if __name__ == '__main__':
    main()

# MrJoshie333 out o/
