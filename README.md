# WorldQuant BRAIN Research Consultant Alpha Pack

Mathematical predictive expressions formatted for WorldQuant BRAIN simulation platform (`platform.worldquantbrain.com`).

## Target Criteria to Qualify as Paid Consultant:
- **Information Coefficient (IC):** > 0.03
- **Sharpe Ratio:** > 1.25
- **Turnover:** < 70%
- **Correlation to existing fund models:** < 0.70

---

## Alpha 1: Volatility-Normalized Mean Reversion on Liquidity Shock
```text
-1 * rank(delta(close, 5) / (high - low + 0.0001)) * rank(volume / adv20)
```
- **Hypothesis:** Stocks exhibiting extreme 5-day directional movement on elevated relative volume suffer short-term liquidity overshooting and revert to their rolling mean.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`
  - Max Trade Weight: `0.05`

---

## Alpha 2: Intraday VWAP Dislocation Reversal
```text
rank(ts_decay_linear(vwap - close, 5)) * rank(ts_rank(volume, 10))
```
- **Hypothesis:** When closing price closes significantly below institutional VWAP accompanied by elevated multi-day volume rank, institutional accumulation creates upward pressure over the subsequent 5-day window.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Industry`
  - Truncation: `0.08`

---

## Alpha 3: Subindustry-Neutral Momentum vs Volume Decay
```text
group_rank(ts_decay_linear(close / ts_delay(close, 20), 10), subindustry) - group_rank(ts_decay_linear(volume / ts_delay(volume, 20), 10), subindustry)
```
- **Hypothesis:** Momentum sustained on declining relative volume represents institutional accumulation, while momentum on surging volume represents retail distribution exhaustion.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.05`

---

## Alpha 4: Standardized Return Residual Asymmetry
```text
-1 * ts_rank((returns - ts_mean(returns, 10)) / (stddev(returns, 20) + 0.0001), 10) * (volume / adv20)
```
- **Hypothesis:** Standardized return shocks exceeding 2 standard deviations on above-average daily volume experience mean reversion as liquidity providers absorb the order imbalance.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Market`
  - Truncation: `0.08`

---

## Alpha 5: Price-Volume Correlation Decoupling
```text
rank(ts_corr(close, volume, 10)) - rank(ts_decay_linear(returns, 5))
```
- **Hypothesis:** A breakdown between 10-day price-volume correlation and short-term trailing returns highlights regime transition preceding cross-sectional factor rotation.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`

---

## How to Submit
1. Create a free account at [survey.worldquantbrain.com](https://survey.worldquantbrain.com/).
2. Open the **Simulation** window.
3. Paste each formula, select settings, and click **Simulate**.
4. When simulation passes Sharpe > 1.25, click **Submit Alpha**.
5. Accumulating points unlocks **Research Consultant** tier with quarterly stipends ($2,000 to $8,000/quarter).