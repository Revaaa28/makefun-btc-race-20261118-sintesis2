"""Sintesis V2 for the make.fun cbBTC bars-replay race
(agent-fun/bars-replay/v1): Rev's RSI entry, gated by depth, with
the RSI-recovery exit. Long only, at most one position, paper USDC.

How this design was reached, in the open: Rev specified an
RSI(14) strategy (buy oversold; sell when BTC makes a new high
versus the entry moment, +1 bar). Built exactly as specified it
measured -23.80 USDC on this kit's dev window — in a falling tape
the new-high exit never fired. A first synthesis kept his entry
and repaired only the exit (sell when RSI recovers, at a profit);
it measured -6.57, least-bad of 180 configurations, all negative:
its recovery exits won 4 of 4 (+16.74), but the raw RSI<30 entry
fires on shallow dips all day (23 episodes on this window) and
three stop-outs (-23.31) outweighed them. What paid on this
window in the sibling designs was selectivity — buying only deep
deviations. Rev approved this V2 shape: his entry, plus that
selectivity, plus the proven exit.

  * Entry — all on the same decision bar:
      1. His RSI signal, cross-up form: Wilder RSI(14) on
         1-minute closes has been under 30 and crosses back up
         through 30. (The pure form — buy while RSI < 30 — is
         measured below; it is worse at every depth.)
      2. DEPTH GATE (new): the close is at least 150 bps below
         the trailing 240-bar high of highs. Only real washouts
         qualify; the shallow oversold dips that sank V1 are
         refused. Rev asked about 120 bps (1.2%) specifically;
         it is measured below and also passes.
      3. A stabilisation bar: the close is at or above the
         previous close (carried from the proven scalper entry;
         on this window it never binds — see below).
    All-in, a 5-bar cooldown after any exit, then re-arm.
  * Exit, first to fire:
      1. RSI recovery with a profit floor (the proven exit):
         RSI at or above 60 AND the close at least +75 bps above
         the actual buy fill price — sell the bounce, only at a
         gain worth the ~26 bps a round trip costs.
      2. His ATH rule, still armed: at the entry bar, record the
         standing high (the highest high from the window's start
         through the entry bar). The first later bar whose high
         exceeds it arms the exit; the sell is decided 1 bar
         after that print.
      3. A -70 bps hard stop from the buy fill price (on closes).
      4. A 420-bar time stop.

Measured on the kit's dev window (24h ending 2026-11-18T14:44Z, a
-2.80% buy-and-hold downtrend) with a fill-faithful simulator — an
exact integer port of the harness's fill engine, which reproduces
the grader's buy-and-hold score of -31.633698 USDC to the unit —
and confirmed by running this file end-to-end over stdio under the
harness's runtime command, twice, byte-identical replies:

  * NET PnL +19.021045 USDC — this entry PASSES the dev gate
    locally (the gate needs only > 0 after costs; the server's
    own grade is the authority, and the race window is unseen,
    so this is a pass, not a promise).
  * 3 round trips, win rate 100%, profit factor infinite (no
    losing trade), expectancy +$6.34 per trade, max drawdown
    0.70% of the starting cash (the guardrail allows 25%).
  * Every exit was the recovery exit: buys decided at bars 72,
    134 and 725 (depths at entry 202, 227 and 151 bps), sold
    +5.51, +7.45 and +6.06. ATH 0, stop 0, time 0, end-of-window
    0 — on this falling tape his new-high rule again never fired
    for a held position, and neither backstop was needed; the
    depth gate kept the bot out of every dip that would have
    stopped out in V1. A fourth buy, decided on the last bar,
    was rejected after_end and cost nothing.
  * Half windows, by the full run's own trades: first half
    +12.96 (trades 1-2), second half +6.06 (trade 3) — both
    halves positive. (Fresh-bot truncated runs: first half
    +12.9562, identical; second half 0 trades — the oversold
    episode straddles the boundary and a cold-start bot misses
    its cross-up, a truncation artefact, disclosed as such.)
  * This is a positive REGION, not a lone spike — the failure
    mode of V1's jagged landscape, checked for explicitly:
      - Depth, one at a time at the shipped exit: 100 bps
        +2.69 (a stop-out and a time exit creep back in), 120
        +18.14, 135 +18.14, 150 +19.02 (shipped), 165 +12.96,
        180 +12.96, 210 +7.42 — positive across the whole axis,
        with 150 mid-region rather than at an edge.
      - The full exit grid at this entry (recovery threshold
        {55, 60, 65} x floor {30, 50, 75} x stop {50, 70, 100}
        x time {240, 420, 600}) is positive in 69 of 81 cells
        at both depth 120 and depth 150. The floor is the axis
        that binds: 30 +9.35, 50 +13.12, 62 +13.97, 75 +19.02
        (shipped), 90 +9.90, 125 +12.00, 150 +12.71 — positive
        on both sides of the shipped value.
      - Threshold 50, 55 and 60 are identical (+19.02); 65
        gives +11.96. Stop 50-150 are identical (it never
        fires); 40 gives +12.44. Time 420, 600 and 900 are
        identical; 300 gives +17.06, 240 gives +7.35. Cooldown
        0-20 identical. Lookback 240, 360, 480 identical;
        120/180 give +12.96. RSI entry level 30 and 32 are
        identical; 35 gives +17.81, 28 gives +7.76, 25 +1.77.
  * Entry forms: cross-up beats the pure level form at every
    depth tested. At the shipped point the pure form nets +9.03
    with the stabilisation bar (3 trades, one closed by the
    end-of-window flatten at a loss) and +9.22 without (5
    trades, one stop-out) — it buys mid-fall and pays for it.
    With the earlier proven exit (floor 50) the cross-up form
    nets +13.04 at depth 120, +13.12 at 150, +9.77 at 180.
  * The stabilisation bar: at every cross-up cell measured,
    PnL is identical with it on or off — every depth-gated
    cross-up bar on this window already closed at or above the
    previous close. It is kept, disclosed as a no-cost guard
    carried from the proven scalper entry, not as a measured
    improvement.
  * Honest limits: 3 trades is a small sample. The design is
    selective the way the +14.07 sibling was — it waits for
    washouts and does nothing on a quiet or rising tape (on a
    rising tape his armed ATH rule is the exit that would do
    the work, and it is untested by this falling window). The
    dev window is one day; the race is another.

Deterministic: no wall clock, no randomness, no environment
reads; the only inputs are the hello and the batches. All
arithmetic is integer, identical every run.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))

import makefun_bars  # noqa: E402

SYMBOL = "CBBTC"

PARAMS = {
    "rsi_period": 14,       # Wilder RSI period (Rev: RSI(14))
    "rsi_entry": 30,        # oversold threshold (Rev: below 30)
    "depth_bps": 150,       # depth gate: bps below the trailing high
    "depth_lookback": 240,  # trailing bars for the high of highs
    "recovery_thr": 60,     # RSI recovery exit threshold
    "recovery_floor_bps": 75,  # recovery exit only at/above this
                            # gain vs the buy fill price
    "stop_bps": 70,         # hard stop below the buy fill price
    "time_stop": 420,       # max bars held
    "cooldown": 5,          # bars after an exit before re-entry
    "size_pct": 100,
    "buy_slip_bps": 10000,
    "sell_slip_bps": 10000,
}


class Bot:
    def __init__(self, hello):
        self.p = dict(PARAMS)
        self.min_notional = int(hello["fees"]["min_notional_quote_units"])
        self.closes = []
        self.highs = []
        self.avg_gain = 0       # Wilder RSI state, scaled by 10**6
        self.avg_loss = 0
        self.rsi_bars = 0
        self.prev_rsi = None
        self.running_high = 0   # highest high since the window start
        self.ref_high = 0       # standing high recorded at the entry
        self.entry_fill_price = 0
        self.entry_fill_bar = -1
        self.ath_armed = False  # a bar printed above ref_high
        self.last_exit = -10 ** 9
        self.pending = None
        self.order_n = 0

    def _next_id(self, tag):
        self.order_n += 1
        return "%s%d" % (tag, self.order_n)

    def _update_rsi(self, close, prev_close):
        if prev_close is None:
            return
        chg = close - prev_close
        gain = chg if chg > 0 else 0
        loss = -chg if chg < 0 else 0
        n = self.p["rsi_period"]
        if self.rsi_bars < n:
            self.avg_gain += gain * 10 ** 6 // n
            self.avg_loss += loss * 10 ** 6 // n
        else:
            self.avg_gain = (self.avg_gain * (n - 1) + gain * 10 ** 6) // n
            self.avg_loss = (self.avg_loss * (n - 1) + loss * 10 ** 6) // n
        self.rsi_bars += 1

    def _rsi(self):
        total = self.avg_gain + self.avg_loss
        if total == 0 or self.rsi_bars < self.p["rsi_period"]:
            return 100
        return 100 * self.avg_gain // total

    def _depth_bps(self, close):
        window = self.highs[-self.p["depth_lookback"]:]
        hi = max(window) if window else 0
        if hi <= 0:
            return 0
        return (hi - close) * 10000 // hi

    def on_batch(self, state, batch):
        prev_close = self.closes[-1] if self.closes else None
        for bar in batch["bars"]:
            if bar["symbol"] == SYMBOL:
                self.closes.append(int(bar["c"]))
                self.highs.append(int(bar["h"]))
        if not self.closes:
            return None
        i = len(self.closes) - 1
        close = self.closes[-1]
        if self.highs[-1] > self.running_high:
            self.running_high = self.highs[-1]
        for fill in batch["fills"]:
            if self.pending == "buy" and fill["side"] == "buy":
                self.pending = None
                self.entry_fill_price = int(fill["price"])
                self.entry_fill_bar = i
            elif self.pending == "sell" and fill["side"] == "sell":
                self.pending = None
        self._update_rsi(close, prev_close)
        rsi = self._rsi()
        p = self.p
        if state.warming_up:
            self.prev_rsi = rsi
            return None
        holding = state.positions.get(SYMBOL)

        if holding is not None and self.pending is None:
            cause = False
            if self.ath_armed:
                cause = True                # his exit: +1 bar
            elif (self.entry_fill_price > 0
                  and (close - self.entry_fill_price) * 10000
                  // self.entry_fill_price <= -p["stop_bps"]):
                cause = True                # hard stop
            elif (rsi >= p["recovery_thr"]
                  and self.entry_fill_price > 0
                  and (close - self.entry_fill_price) * 10000
                  // self.entry_fill_price >= p["recovery_floor_bps"]):
                cause = True                # RSI recovery, at a gain
            elif (self.entry_fill_bar >= 0
                  and i - self.entry_fill_bar >= p["time_stop"]):
                cause = True                # time stop
            if cause:
                self.pending = "sell"
                self.last_exit = i
                self.ath_armed = False
                self.prev_rsi = rsi
                return [{
                    "side": "sell",
                    "client_id": self._next_id("s"),
                    "symbol": SYMBOL,
                    "qty": holding.qty,
                    "max_slippage_bps": p["sell_slip_bps"],
                }]
            # No exit decided: watch for the new-high print (his rule).
            if self.highs[-1] > self.ref_high:
                self.ath_armed = True
            self.prev_rsi = rsi
            return None

        if holding is not None or self.pending is not None:
            self.prev_rsi = rsi
            return None
        if i - self.last_exit < p["cooldown"]:
            self.prev_rsi = rsi
            return None
        if self.rsi_bars < p["rsi_period"]:
            self.prev_rsi = rsi
            return None

        # Entry: his RSI cross-up, the depth gate, the
        # stabilisation bar — all on this decision bar.
        signal = (self.prev_rsi is not None
                  and self.prev_rsi < p["rsi_entry"] <= rsi)
        if signal and self._depth_bps(close) < p["depth_bps"]:
            signal = False                  # dip too shallow: refuse
        if signal and prev_close is not None and close < prev_close:
            signal = False                  # still falling: refuse
        if not signal:
            self.prev_rsi = rsi
            return None

        notional = state.cash * p["size_pct"] // 100
        room = state.weight_room(SYMBOL)
        if room < notional:
            notional = room
        if notional < self.min_notional:
            self.prev_rsi = rsi
            return None
        self.pending = "buy"
        self.ref_high = self.running_high
        self.ath_armed = False
        self.entry_fill_price = 0
        self.entry_fill_bar = -1
        self.prev_rsi = rsi
        return [{
            "side": "buy",
            "client_id": self._next_id("b"),
            "symbol": SYMBOL,
            "notional_quote_units": notional,
            "max_slippage_bps": p["buy_slip_bps"],
        }]


def main():
    holder = {}

    def on_batch(state, batch):
        bot = holder.get("bot")
        if bot is None:
            bot = holder["bot"] = Bot(state.hello)
        return bot.on_batch(state, batch)

    makefun_bars.run(on_batch)


if __name__ == "__main__":
    main()
