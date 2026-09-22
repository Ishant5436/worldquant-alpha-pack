# WorldQuant BRAIN Research Consultant Alpha Pack

Mathematical predictive expressions formatted for the WorldQuant BRAIN simulation platform (`platform.worldquantbrain.com`).

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

## Alpha 6: Roll Spread Liquidity Discrepancy
```text
-1 * rank(ts_decay_linear(abs(close - ts_delay(close, 1)) / (volume / adv20 + 0.0001), 5))
```
- **Hypothesis:** High price dislocation per unit volume relative to 20-day average signals temporary liquidity evaporation that mean-reverts over 5 days.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`

---

## Alpha 7: Parkinson High-Low Volatility Shock Mean Reversion
```text
-1 * rank((high - low) / (abs(close - open) + 0.0001)) * rank(returns)
```
- **Hypothesis:** When intraday range (high-low) expands dramatically relative to body (close-open) on positive return days, buying power is exhausted and sets up negative reversal.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`

---

## Alpha 8: Subindustry Momentum Acceleration Divergence
```text
group_rank(delta(close, 5) - delta(close, 20) / 4, subindustry) - group_rank(returns, subindustry)
```
- **Hypothesis:** Accelerating short-term return differentials over longer trailing baselines identify strong institutional momentum accumulation before broader market awareness.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.05`

---

## Alpha 9: Volume-Weighted Price Dislocation Mean Reversion
```text
-1 * rank(vwap - close) * rank(adv20 / (volume + 0.0001))
```
- **Hypothesis:** Large discounts of closing price beneath VWAP on subdued trading volume indicate temporary liquidity vacuum rather than fundamental re-rating.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.08`

---

## Alpha 10: Multi-Scale Price-Volume Skewness Asymmetry
```text
rank(ts_corr(returns, volume, 20)) - rank(ts_corr(returns, volume, 5))
```
- **Hypothesis:** Short-term divergence where 5-day return-volume correlation flips relative to 20-day baseline flags institutional rotation regimes.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Industry`
  - Truncation: `0.08`

---

## Alpha 11: Decayed Residual Volatility Spread
```text
-1 * group_rank(stddev(returns, 20) - stddev(returns, 5), subindustry) * sign(returns)
```
- **Hypothesis:** Compressing volatility following large return swings precedes continuation in the direction of the dominant institutional trend.
- **Simulation Settings:**
  - Region: `USA`
  - Universe: `TOP3000`
  - Neutralization: `Subindustry`
  - Truncation: `0.05`

---

## Alpha 12: Intraday Range Exhaustion Reversion
```text
-1 * rank(ts_decay_linear(high - vwap, 5)) * rank(volume / adv20)
```
- **Hypothesis:** Extended high-to-VWAP stretch accompanied by heavy trading volume signals upward buying exhaustion and institutional profit-taking.
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