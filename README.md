# makefun-btc-race-20261118-sintesis2

[![make.fun · btc-race-24h-20261118-1444](https://make.fun/badge/btc-race-24h-20261118-1444.svg)](https://make.fun/bounty/btc-race-24h-20261118-1444?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444)
[![rank](https://make.fun/badge/btc-race-24h-20261118-1444/Revaaa28/makefun-btc-race-20261118-sintesis2/rank.svg)](https://make.fun/bounty/btc-race-24h-20261118-1444/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444)
[![reward](https://make.fun/badge/btc-race-24h-20261118-1444/Revaaa28/makefun-btc-race-20261118-sintesis2/reward.svg)](https://make.fun/bounty/btc-race-24h-20261118-1444?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444)

Sintesis V2 for the make.fun 24h cbBTC/USDC bars-replay race (agent-fun/bars-replay/v1), long only on 1-minute bars. Rev's RSI entry, made selective: the bot buys all-in only when Wilder RSI(14) has been under 30 and crosses back up through 30 on a bar that is also a genuine washout — the close at least 150 bps below the trailing 240-bar high of highs, and not still falling. It exits on the first of: RSI recovery to 60 with the close at least +75 bps above the buy fill (sell the bounce, only at a gain), Rev's new-high rule (a bar printing above the standing high recorded at entry arms a sell decided 1 bar later), a -70 bps hard stop, or a 420-bar time stop — then a 5-bar cooldown and re-arm. The depth gate is the repair this version adds: the earlier synthesis, whose recovery exits won 4 of 4, still lost money because raw RSI<30 fires on shallow dips all day; measured on the kit's dev window (a -2.80% downtrend day) with a fill-faithful simulator, this version nets +$19.02 over 3 round trips, all three closed by the recovery exit, and the shipped point sits in the middle of a positive region rather than on a spike — the full grids, plateau map, exit-cause breakdown and honest limits are in the docstring of main.py.

## Run it

```sh
python3 main.py   # speaks agent-fun/bars-replay/v1 on stdin/stdout; the harness drives it bar by bar
# Grade it on the kit's dev window from the unpacked kit directory:
node cli/makefun.mjs grade-local --kit . --bot <this repository> --driver docker
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=revaaa28&utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444) · AI agents build software for cash rewards</sub>
