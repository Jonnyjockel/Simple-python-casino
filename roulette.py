import random


RED_NUMBERS = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36,
}


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
        return number


def ask_choice(prompt, choices):
    choices = {choice.lower() for choice in choices}
    while True:
        answer = input(prompt).strip().lower()
        if answer in choices:
            return answer
        print(f"Choose one of: {', '.join(sorted(choices))}")


def place_bet(bankroll):
    print("\nBet types:")
    print("  red / black - pays 1:1")
    print("  even / odd  - pays 1:1")
    print("  number      - pays 35:1")

    bet_type = ask_choice("What do you want to bet on? ", ["red", "black", "even", "odd", "number"])
    bet_target = bet_type

    if bet_type == "number":
        bet_target = ask_int("Pick a number from 0 to 36: ", 0, 36)

    amount = ask_int(f"Bet amount (bankroll ${bankroll}): $", 1, bankroll)
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


def main():
    print("Simple Python Roulette")
    print("----------------------")
    bankroll = 100

    while bankroll > 0:
        print(f"\nYou have ${bankroll}.")
        bet_type, bet_target, amount = place_bet(bankroll)

        print("\nSpinning...")
        result = random.randint(0, 36)
        result_color = color_for(result)
        print(f"The ball landed on {result} ({result_color}).")

        won, payout = resolve_bet(bet_type, bet_target, amount, result)
        bankroll += payout

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

    print(f"\nFinal bankroll: ${bankroll}")
    print("Thanks for playing.")


if __name__ == "__main__":
    main()
