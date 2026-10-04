# WorldQuant BRAIN Research Consultant Alpha Pack

Mathematical predictive expressions formatted for the WorldQuant BRAIN simulation platform (`platform.worldquantbrain.com`).

## Target Criteria to Qualify as Paid Consultant:
- **Information Coefficient (IC):** > 0.03
- **Sharpe Ratio:** > 1.25
- **Turnover:** < 70%
- **Correlation to existing fund models:** < 0.70

---
## Alpha 1: Volatility-Normalized Mean Reversion
```text
-1 * rank(delta(close, 5) / (high - low + 0.0001)) * rank(volume / adv20)
```
- **Hypothesis:** Short-term extreme directional excursions revert on elevated liquidity volume.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 2: Volume-Gated Range Mean Reversion
```text
-1 * rank(ts_rank(close, 10)) * rank(volume / adv20)
```
- **Hypothesis:** Multi-day highs on high turnover signal exhaustion and subsequent reversion.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 3: VWAP Dislocation Mean Reversion
```text
-1 * rank(delta(vwap, 3)) * rank(ts_mean(volume, 5) / adv20)
```
- **Hypothesis:** Aggressive rapid benchmark pricing drift snaps back toward equilibrium.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 4: Intraday Close vs Open Fade
```text
-1 * rank(close - open) * rank(ts_rank(volume, 5))
```
- **Hypothesis:** Intraday trends supported by spike volume show next-day mean reversion.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 5: Short Horizon Decay Reversal
```text
-1 * rank(delta(close, 2)) * rank(ts_decay_linear(volume, 5))
```
- **Hypothesis:** Two-day sharp momentum decays rapidly under weighted volume confirmation.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 6: Decay Linear Acceleration
```text
rank(ts_decay_linear(delta(close, 5), 10)) * rank(adv20 / ts_mean(volume, 20))
```
- **Hypothesis:** Decaying smoothed multi-day returns signal persistent institutional accumulation.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 7: Price Volume Correlation Trend
```text
rank(ts_rank(close, 20)) * rank(ts_corr(close, volume, 10))
```
- **Hypothesis:** High percentile closing prices co-varying with volume establish strong trend regimes.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 8: Multi-Horizon Price Momentum
```text
rank(close - ts_delay(close, 10)) * rank(ts_decay_linear(volume, 10))
```
- **Hypothesis:** 10-day price momentum sustained by volume persistence exhibits continuation.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 9: Moving Average Gap Breakout
```text
rank(ts_mean(close, 5) - ts_mean(close, 20)) * rank(volume / adv20)
```
- **Hypothesis:** Short versus medium moving average divergence supported by volume.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 10: VWAP Trend with Return Volume Coupling
```text
rank(delta(vwap, 5)) * rank(ts_corr(returns, volume, 15))
```
- **Hypothesis:** 5-day VWAP upward movement correlated with volume yields alpha continuation.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 11: Intraday VWAP Dislocation Reversal
```text
rank(ts_decay_linear(vwap - close, 5)) * rank(ts_rank(volume, 10))
```
- **Hypothesis:** Closing prices lagging VWAP on elevated volume signal institutional accumulation.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 12: Price-Volume Correlation Divergence
```text
-1 * rank(ts_corr(close, volume, 10)) * rank(delta(close, 3))
```
- **Hypothesis:** Negative price-volume correlation indicates distribution during price run-ups.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 13: Liquidity Shock Impact
```text
rank(volume / adv20) * rank(delta(close, 1) / (high - low + 0.001))
```
- **Hypothesis:** Elevated liquidity with efficient range expansion signals institutional participation.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 14: Volatility Damped Drift
```text
-1 * rank(ts_stddev(returns, 10)) * rank(delta(close, 5))
```
- **Hypothesis:** High realized volatility penalizes continuation; lower volatility trends persist.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 15: Weighted Intraday Pressure
```text
rank(ts_decay_linear(close - open, 3)) * rank(volume / ts_mean(volume, 10))
```
- **Hypothesis:** Cumulative intraday bar pressure predicts near-term performance.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 16: Dispersion Normalized Trend Fade
```text
-1 * rank(ts_stddev(close, 20) / ts_mean(close, 20)) * rank(delta(close, 5))
```
- **Hypothesis:** High relative dispersion over 20 days anticipates trend exhaustion.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 17: True Range Expansion with Volume
```text
rank(ts_rank(high - low, 10)) * rank(delta(volume, 3))
```
- **Hypothesis:** Expanding high-low range on surging volume precedes breakout continuation.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 18: Range Contraction Reversal
```text
-1 * rank(delta(high - low, 5)) * rank(ts_corr(close, vwap, 10))
```
- **Hypothesis:** Sharp volatility contraction with VWAP alignment predicts impending reversal.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 19: Volume Volatility Premium
```text
rank(ts_decay_linear(returns, 5)) * rank(ts_stddev(volume, 10) / adv20)
```
- **Hypothesis:** Return momentum amplified by volume volatility premium.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 20: Upper Range Exhaustion
```text
-1 * rank(ts_max(high, 10) - close) * rank(ts_rank(volume, 5))
```
- **Hypothesis:** Closeness to 10-day high under spike volume indicates resistance.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 21: Overnight Gap Fade
```text
-1 * rank(open - ts_delay(close, 1)) * rank(volume / adv20)
```
- **Hypothesis:** Overnight opening gaps fade when volume does not validate the move.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 22: Shadow Asymmetry Pressure
```text
rank(ts_rank(close - low, 5) - ts_rank(high - close, 5))
```
- **Hypothesis:** Persistent bottom-shadow buying dominance predicts bullish drift.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 23: Gap Decay Mean Reversion
```text
-1 * rank(ts_delay(close, 1) - open) * rank(ts_stddev(returns, 5))
```
- **Hypothesis:** Under high volatility, opening gap down experiences short-covering bounce.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 24: VWAP Relative Stretch
```text
rank(close - vwap) * rank(ts_decay_linear(volume, 5) / adv20)
```
- **Hypothesis:** Moderate VWAP extension with persistent volume confirms institutional demand.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 25: Extreme One-Day Volume Exhaustion
```text
-1 * rank(delta(close, 1)) * rank(ts_max(volume, 5) / adv20)
```
- **Hypothesis:** Single-day price surge on peak 5-day volume suffers profit-taking.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`
