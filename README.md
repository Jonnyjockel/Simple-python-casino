# Simple Python Casino

A small terminal casino game collection written in plain Python.

## Note

This is just a simple game project, not real gambling.

## Features

- Main menu with a separate game-select screen
- Menus refresh after each valid input to reduce terminal clutter
- Playable roulette mode
- Playable five-card poker mode
- Playable blackjack mode
- Starts you with a `$100` bankroll
- Roulette supports bets on:
  - red / black
  - even / odd
  - exact number from `0` to `36`
- Uses standard roulette payouts:
  - even-money bets pay `1:1`
  - exact number bets pay `35:1`
- Poker deals five cards to you and five to the dealer, ranks both hands, and pays `1:1`
- Blackjack supports hit/stand, dealer drawing to `17`, busts, pushes, and blackjack paying `3:2`
- No external dependencies

## Run

```bash
python roulette.py
```

On some systems, use:

```bash
python3 roulette.py
```

## Note

This is just a simple game project, not real gambling.
