import os
import random
from pathlib import Path


RED_NUMBERS = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36,
}
SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = list(range(2, 15))
RANK_NAMES = {
    11: "Jack",
    12: "Queen",
    13: "King",
    14: "Ace",
}
SAVE_FILE = Path.home() / "Documents" / "simple-python-casino-save"
STARTING_BANKROLL = 100.0


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def load_bankroll():
    try:
        SAVE_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not SAVE_FILE.exists():
            save_bankroll(STARTING_BANKROLL)
            return STARTING_BANKROLL

        saved_value = float(SAVE_FILE.read_text(encoding="utf-8").strip())
        return saved_value
    except (OSError, ValueError):
        return STARTING_BANKROLL


def save_bankroll(bankroll):
    SAVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    SAVE_FILE.write_text(format_money(bankroll), encoding="utf-8")


def color_for(number):
    if number == 0:
        return "green"
    if number in RED_NUMBERS:
        return "red"
    return "black"


def ask_int(prompt, minimum=None, maximum=None):
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
        except ValueError:
            print("Please enter a whole number.")
            continue

        if minimum is not None and number < minimum:
            print(f"Please enter at least {minimum}.")
            continue
        if maximum is not None and number > maximum:
            print(f"Please enter at most {maximum}.")
            continue
        clear_screen()
        return number


def ask_choice(prompt, choices):
    choices = {choice.lower() for choice in choices}
    while True:
        answer = input(prompt).strip().lower()
        if answer in choices:
            clear_screen()
            return answer
        print(f"Choose one of: {', '.join(sorted(choices))}")


def format_card(card):
    rank, suit = card
    rank_name = RANK_NAMES.get(rank, str(rank))
    return f"{rank_name} of {suit}"


def format_hand(hand):
    return ", ".join(format_card(card) for card in hand)


def print_hand(label, hand, total=None, hidden_cards=None):
    print(label)
    for card in hand:
        print(f"  - {format_card(card)}")
    if hidden_cards:
        for hidden_card in hidden_cards:
            print(f"  - {hidden_card}")
    if total is not None:
        print(f"  Total: {total}")


def format_money(amount):
    if amount == int(amount):
        return str(int(amount))
    return f"{amount:.2f}"


def place_bet(bankroll):
    print("\nBet types:")
    print("  1. red    - pays 1:1")
    print("  2. black  - pays 1:1")
    print("  3. even   - pays 1:1")
    print("  4. odd    - pays 1:1")
    print("  5. number - pays 35:1")

    bet_type = ask_choice(
        "What do you want to bet on? ",
        ["1", "2", "3", "4", "5", "red", "black", "even", "odd", "number"],
    )
    bet_type = {
        "1": "red",
        "2": "black",
        "3": "even",
        "4": "odd",
        "5": "number",
    }.get(bet_type, bet_type)
    bet_target = bet_type

    if bet_type == "number":
        bet_target = ask_int("Pick a number from 0 to 36: ", 0, 36)

    amount = ask_int(f"Bet amount (bankroll ${format_money(bankroll)}): $", 1, bankroll)
    return bet_type, bet_target, amount


def resolve_bet(bet_type, bet_target, amount, result):
    result_color = color_for(result)

    if bet_type in {"red", "black"}:
        won = result_color == bet_type
        payout = amount if won else -amount
    elif bet_type == "even":
        won = result != 0 and result % 2 == 0
        payout = amount if won else -amount
    elif bet_type == "odd":
        won = result % 2 == 1
        payout = amount if won else -amount
    else:
        won = result == bet_target
        payout = amount * 35 if won else -amount

    return won, payout


def play_roulette():
    print("Simple Python Roulette")
    print("----------------------")
    bankroll = load_bankroll()

    while bankroll > 0:
        print(f"\nYou have ${format_money(bankroll)}.")
        bet_type, bet_target, amount = place_bet(bankroll)

        print("\nSpinning...")
        result = random.randint(0, 36)
        result_color = color_for(result)
        print(f"The ball landed on {result} ({result_color}).")

        won, payout = resolve_bet(bet_type, bet_target, amount, result)
        bankroll += payout
        save_bankroll(bankroll)

        if won:
            print(f"You won ${payout}!")
        else:
            print(f"You lost ${amount}.")

        if bankroll <= 0:
            print("\nYou are out of money. Game over.")
            break

        again = ask_choice("Play another round? (y/n): ", ["y", "n"])
        if again == "n":
            break

    save_bankroll(bankroll)
    print(f"\nFinal bankroll: ${format_money(bankroll)}")
    print("Thanks for playing.")


def build_deck():
    return [(rank, suit) for suit in SUITS for rank in RANKS]


def is_straight(values):
    unique_values = sorted(set(values))
    if unique_values == [2, 3, 4, 5, 14]:
        return True, 5

    if len(unique_values) != 5:
        return False, None

    low = unique_values[0]
    high = unique_values[-1]
    if high - low == 4:
        return True, high

    return False, None


def evaluate_poker_hand(hand):
    values = sorted((rank for rank, _suit in hand), reverse=True)
    suits = [suit for _rank, suit in hand]
    counts = {value: values.count(value) for value in set(values)}
    count_groups = sorted(counts.items(), key=lambda item: (item[1], item[0]), reverse=True)
    flush = len(set(suits)) == 1
    straight, straight_high = is_straight(values)

    if straight and flush:
        return 8, [straight_high], "Straight Flush"
    if count_groups[0][1] == 4:
        four = count_groups[0][0]
        kicker = max(value for value in values if value != four)
        return 7, [four, kicker], "Four of a Kind"
    if count_groups[0][1] == 3 and count_groups[1][1] == 2:
        return 6, [count_groups[0][0], count_groups[1][0]], "Full House"
    if flush:
        return 5, values, "Flush"
    if straight:
        return 4, [straight_high], "Straight"
    if count_groups[0][1] == 3:
        three = count_groups[0][0]
        kickers = sorted((value for value in values if value != three), reverse=True)
        return 3, [three, *kickers], "Three of a Kind"

    pairs = sorted((value for value, count in counts.items() if count == 2), reverse=True)
    if len(pairs) == 2:
        kicker = max(value for value in values if value not in pairs)
        return 2, [*pairs, kicker], "Two Pair"
    if len(pairs) == 1:
        pair = pairs[0]
        kickers = sorted((value for value in values if value != pair), reverse=True)
        return 1, [pair, *kickers], "One Pair"

    return 0, values, "High Card"


def compare_hands(player_hand, dealer_hand):
    player_score = evaluate_poker_hand(player_hand)
    dealer_score = evaluate_poker_hand(dealer_hand)

    if player_score[:2] > dealer_score[:2]:
        return 1, player_score, dealer_score
    if player_score[:2] < dealer_score[:2]:
        return -1, player_score, dealer_score
    return 0, player_score, dealer_score


def play_poker():
    print("\nSimple Five-Card Poker")
    print("----------------------")
    bankroll = load_bankroll()

    while bankroll > 0:
        print(f"\nYou have ${format_money(bankroll)}.")
        amount = ask_int(f"Bet amount (bankroll ${format_money(bankroll)}): $", 1, bankroll)

        deck = build_deck()
        random.shuffle(deck)
        player_hand = deck[:5]
        dealer_hand = deck[5:10]

        print()
        print_hand("Your hand:", player_hand)
        print_hand("Dealer hand:", dealer_hand)

        result, player_score, dealer_score = compare_hands(player_hand, dealer_hand)
        print(f"\nYou have:    {player_score[2]}")
        print(f"Dealer has:  {dealer_score[2]}")

        if result > 0:
            bankroll += amount
            print(f"You won ${amount}!")
        elif result < 0:
            bankroll -= amount
            print(f"You lost ${amount}.")
        else:
            print("Push. Nobody wins.")
        save_bankroll(bankroll)

        if bankroll <= 0:
            print("\nYou are out of money. Game over.")
            break

        again = ask_choice("Play another poker hand? (y/n): ", ["y", "n"])
        if again == "n":
            break

    save_bankroll(bankroll)
    print(f"\nFinal bankroll: ${format_money(bankroll)}")
    print("Thanks for playing.")


def blackjack_card_value(card):
    rank, _suit = card
    if rank == 14:
        return 11
    if rank >= 10:
        return 10
    return rank


def blackjack_hand_value(hand):
    total = sum(blackjack_card_value(card) for card in hand)
    aces = sum(1 for rank, _suit in hand if rank == 14)

    while total > 21 and aces:
        total -= 10
        aces -= 1

    return total


def is_blackjack(hand):
    return len(hand) == 2 and blackjack_hand_value(hand) == 21


def show_blackjack_hands(player_hand, dealer_hand, hide_dealer_card):
    print()
    print_hand("Your hand:", player_hand, total=blackjack_hand_value(player_hand))
    if hide_dealer_card:
        print_hand("Dealer hand:", [dealer_hand[0]], hidden_cards=["Hidden Card"])
    else:
        print_hand("Dealer hand:", dealer_hand, total=blackjack_hand_value(dealer_hand))


def play_blackjack():
    print("\nSimple Blackjack")
    print("----------------")
    bankroll = load_bankroll()

    while bankroll > 0:
        print(f"\nYou have ${format_money(bankroll)}.")
        amount = ask_int(f"Bet amount (bankroll ${format_money(bankroll)}): $", 1, bankroll)

        deck = build_deck()
        random.shuffle(deck)
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        show_blackjack_hands(player_hand, dealer_hand, hide_dealer_card=True)

        player_blackjack = is_blackjack(player_hand)
        dealer_blackjack = is_blackjack(dealer_hand)

        if player_blackjack or dealer_blackjack:
            show_blackjack_hands(player_hand, dealer_hand, hide_dealer_card=False)
            if player_blackjack and dealer_blackjack:
                print("Both have blackjack. Push.")
            elif player_blackjack:
                winnings = amount * 1.5
                bankroll += winnings
                print(f"Blackjack! You won ${format_money(winnings)}.")
            else:
                bankroll -= amount
                print(f"Dealer has blackjack. You lost ${amount}.")
        else:
            while blackjack_hand_value(player_hand) < 21:
                action = ask_choice("Hit or stand? (h/s): ", ["h", "s"])
                if action == "s":
                    break

                player_hand.append(deck.pop())
                show_blackjack_hands(player_hand, dealer_hand, hide_dealer_card=True)

            player_total = blackjack_hand_value(player_hand)
            if player_total > 21:
                bankroll -= amount
                print(f"You busted with {player_total}. You lost ${amount}.")
            else:
                show_blackjack_hands(player_hand, dealer_hand, hide_dealer_card=False)
                while blackjack_hand_value(dealer_hand) < 17:
                    dealer_hand.append(deck.pop())
                    print(f"Dealer hits: {format_card(dealer_hand[-1])}")
                    print(f"Dealer total: {blackjack_hand_value(dealer_hand)}")

                dealer_total = blackjack_hand_value(dealer_hand)
                if dealer_total > 21:
                    bankroll += amount
                    print(f"Dealer busted with {dealer_total}. You won ${amount}!")
                elif player_total > dealer_total:
                    bankroll += amount
                    print(f"You won ${amount}!")
                elif player_total < dealer_total:
                    bankroll -= amount
                    print(f"You lost ${amount}.")
                else:
                    print("Push. Nobody wins.")
        save_bankroll(bankroll)

        if bankroll <= 0:
            print("\nYou are out of money. Game over.")
            break

        again = ask_choice("Play another blackjack hand? (y/n): ", ["y", "n"])
        if again == "n":
            break

    print(f"\nFinal bankroll: ${format_money(bankroll)}")
    save_bankroll(bankroll)
    print("Thanks for playing.")


def show_game_menu():
    while True:
        print("\nChoose a Game")
        print("-------------")
        print("1. Roulette")
        print("2. Poker")
        print("3. Blackjack")
        print("4. Back")

        choice = ask_choice("Choose an option: ", ["1", "2", "3", "4"])

        if choice == "1":
            play_roulette()
        elif choice == "2":
            play_poker()
        elif choice == "3":
            play_blackjack()
        else:
            break


def main():
    while True:
        print("\nCasino Main Menu")
        print("----------------")
        print("1. Play")
        print("2. Quit")

        choice = ask_choice("Choose an option: ", ["1", "2"])

        if choice == "1":
            show_game_menu()
        else:
            print("\nGoodbye.")
            break


if __name__ == "__main__":
    main()
