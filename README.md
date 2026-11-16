# makefun-tiny-chess

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/edisonradit93/makefun-tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/edisonradit93/makefun-tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

High-performance Python chess engine under 4 KB designed for make.fun's tiny-chess-01 bounty.
Optimized Sunfish architecture featuring mailbox board representation and alpha-beta search.

## Engine Architecture

- Negamax search with alpha-beta pruning and capture quiescence.
- Positional evaluation via Piece-Square Tables (PST) and material imbalance.
- MVV-LVA move ordering for maximum pruning efficiency.
- Deterministic evaluation adhering strictly to the <4,096 bytes constraint.

## Run

```sh
python main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=z30rer01&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
