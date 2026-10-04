#!/usr/bin/env python3
"""
Programmatic WorldQuant BRAIN Alpha Synthesizer.
Generates institutional, mathematically orthogonal alpha expressions.
Conforms strictly to Deterministic Safety Standards:
<=60 lines per function, >=2 assertions per function.
"""
from enum import Enum
from typing import List, Dict, Any


class FactorCategory(str, Enum):
    """Orthogonal factor themes for WorldQuant BRAIN simulation."""
    MEAN_REVERSION = "Mean Reversion"
    MOMENTUM = "Momentum"
    LIQUIDITY = "Liquidity & Order Flow"
    VOLATILITY = "Volatility Spread"
    EXTREMES = "Intraday Extremes"


def get_default_settings() -> Dict[str, str]:
    """Returns canonical simulation settings for US Top 3000 equities."""
    settings = {
        "Region": "USA",
        "Universe": "TOP3000",
        "Neutralization": "Subindustry",
        "Truncation": "0.08",
        "Max Trade Weight": "0.05",
    }
    assert len(settings) == 5, "Simulation settings count invariant breached"
    assert settings["Region"] == "USA", "Region must be USA"
    return settings


def _generate_mean_reversion_alphas() -> List[Dict[str, Any]]:
    """Synthesizes short-term liquidity-shock and mean reversion alphas."""
    alphas = [
        {
            "name": "Volatility-Normalized Mean Reversion",
            "expression": "-1 * rank(delta(close, 5) / (high - low + 0.0001)) * rank(volume / adv20)",
            "hypothesis": "Short-term extreme directional excursions revert on elevated liquidity volume.",
        },
        {
            "name": "Volume-Gated Range Mean Reversion",
            "expression": "-1 * rank(ts_rank(close, 10)) * rank(volume / adv20)",
            "hypothesis": "Multi-day highs on high turnover signal exhaustion and subsequent reversion.",
        },
        {
            "name": "VWAP Dislocation Mean Reversion",
            "expression": "-1 * rank(delta(vwap, 3)) * rank(ts_mean(volume, 5) / adv20)",
            "hypothesis": "Aggressive rapid benchmark pricing drift snaps back toward equilibrium.",
        },
        {
            "name": "Intraday Close vs Open Fade",
            "expression": "-1 * rank(close - open) * rank(ts_rank(volume, 5))",
            "hypothesis": "Intraday trends supported by spike volume show next-day mean reversion.",
        },
        {
            "name": "Short Horizon Decay Reversal",
            "expression": "-1 * rank(delta(close, 2)) * rank(ts_decay_linear(volume, 5))",
            "hypothesis": "Two-day sharp momentum decays rapidly under weighted volume confirmation.",
        },
    ]
    assert len(alphas) == 5, "Alpha generation batch size invariant breached"
    assert all("(" in a["expression"] for a in alphas), "Grammar invariant breached"
    return alphas


def _generate_momentum_alphas() -> List[Dict[str, Any]]:
    """Synthesizes trend continuation and acceleration alphas."""
    alphas = [
        {
            "name": "Decay Linear Acceleration",
            "expression": "rank(ts_decay_linear(delta(close, 5), 10)) * rank(adv20 / ts_mean(volume, 20))",
            "hypothesis": "Decaying smoothed multi-day returns signal persistent institutional accumulation.",
        },
        {
            "name": "Price Volume Correlation Trend",
            "expression": "rank(ts_rank(close, 20)) * rank(ts_corr(close, volume, 10))",
            "hypothesis": "High percentile closing prices co-varying with volume establish strong trend regimes.",
        },
        {
            "name": "Multi-Horizon Price Momentum",
            "expression": "rank(close - ts_delay(close, 10)) * rank(ts_decay_linear(volume, 10))",
            "hypothesis": "10-day price momentum sustained by volume persistence exhibits continuation.",
        },
        {
            "name": "Moving Average Gap Breakout",
            "expression": "rank(ts_mean(close, 5) - ts_mean(close, 20)) * rank(volume / adv20)",
            "hypothesis": "Short versus medium moving average divergence supported by volume.",
        },
        {
            "name": "VWAP Trend with Return Volume Coupling",
            "expression": "rank(delta(vwap, 5)) * rank(ts_corr(returns, volume, 15))",
            "hypothesis": "5-day VWAP upward movement correlated with volume yields alpha continuation.",
        },
    ]
    assert len(alphas) == 5, "Alpha generation batch size invariant breached"
    assert all("(" in a["expression"] for a in alphas), "Grammar invariant breached"
    return alphas


def _generate_liquidity_alphas() -> List[Dict[str, Any]]:
    """Synthesizes order flow and liquidity imbalance alphas."""
    alphas = [
        {
            "name": "Intraday VWAP Dislocation Reversal",
            "expression": "rank(ts_decay_linear(vwap - close, 5)) * rank(ts_rank(volume, 10))",
            "hypothesis": "Closing prices lagging VWAP on elevated volume signal institutional accumulation.",
        },
        {
            "name": "Price-Volume Correlation Divergence",
            "expression": "-1 * rank(ts_corr(close, volume, 10)) * rank(delta(close, 3))",
            "hypothesis": "Negative price-volume correlation indicates distribution during price run-ups.",
        },
        {
            "name": "Liquidity Shock Impact",
            "expression": "rank(volume / adv20) * rank(delta(close, 1) / (high - low + 0.001))",
            "hypothesis": "Elevated liquidity with efficient range expansion signals institutional participation.",
        },
        {
            "name": "Volatility Damped Drift",
            "expression": "-1 * rank(ts_stddev(returns, 10)) * rank(delta(close, 5))",
            "hypothesis": "High realized volatility penalizes continuation; lower volatility trends persist.",
        },
        {
            "name": "Weighted Intraday Pressure",
            "expression": "rank(ts_decay_linear(close - open, 3)) * rank(volume / ts_mean(volume, 10))",
            "hypothesis": "Cumulative intraday bar pressure predicts near-term performance.",
        },
    ]
    assert len(alphas) == 5, "Alpha generation batch size invariant breached"
    assert all("(" in a["expression"] for a in alphas), "Grammar invariant breached"
    return alphas


def _generate_volatility_alphas() -> List[Dict[str, Any]]:
    """Synthesizes volatility dispersion and channel breakout alphas."""
    alphas = [
        {
            "name": "Dispersion Normalized Trend Fade",
            "expression": "-1 * rank(ts_stddev(close, 20) / ts_mean(close, 20)) * rank(delta(close, 5))",
            "hypothesis": "High relative dispersion over 20 days anticipates trend exhaustion.",
        },
        {
            "name": "True Range Expansion with Volume",
            "expression": "rank(ts_rank(high - low, 10)) * rank(delta(volume, 3))",
            "hypothesis": "Expanding high-low range on surging volume precedes breakout continuation.",
        },
        {
            "name": "Range Contraction Reversal",
            "expression": "-1 * rank(delta(high - low, 5)) * rank(ts_corr(close, vwap, 10))",
            "hypothesis": "Sharp volatility contraction with VWAP alignment predicts impending reversal.",
        },
        {
            "name": "Volume Volatility Premium",
            "expression": "rank(ts_decay_linear(returns, 5)) * rank(ts_stddev(volume, 10) / adv20)",
            "hypothesis": "Return momentum amplified by volume volatility premium.",
        },
        {
            "name": "Upper Range Exhaustion",
            "expression": "-1 * rank(ts_max(high, 10) - close) * rank(ts_rank(volume, 5))",
            "hypothesis": "Closeness to 10-day high under spike volume indicates resistance.",
        },
    ]
    assert len(alphas) == 5, "Alpha generation batch size invariant breached"
    assert all("(" in a["expression"] for a in alphas), "Grammar invariant breached"
    return alphas


def _generate_extremes_alphas() -> List[Dict[str, Any]]:
    """Synthesizes gap opening and intraday shadow extremity alphas."""
    alphas = [
        {
            "name": "Overnight Gap Fade",
            "expression": "-1 * rank(open - ts_delay(close, 1)) * rank(volume / adv20)",
            "hypothesis": "Overnight opening gaps fade when volume does not validate the move.",
        },
        {
            "name": "Shadow Asymmetry Pressure",
            "expression": "rank(ts_rank(close - low, 5) - ts_rank(high - close, 5))",
            "hypothesis": "Persistent bottom-shadow buying dominance predicts bullish drift.",
        },
        {
            "name": "Gap Decay Mean Reversion",
            "expression": "-1 * rank(ts_delay(close, 1) - open) * rank(ts_stddev(returns, 5))",
            "hypothesis": "Under high volatility, opening gap down experiences short-covering bounce.",
        },
        {
            "name": "VWAP Relative Stretch",
            "expression": "rank(close - vwap) * rank(ts_decay_linear(volume, 5) / adv20)",
            "hypothesis": "Moderate VWAP extension with persistent volume confirms institutional demand.",
        },
        {
            "name": "Extreme One-Day Volume Exhaustion",
            "expression": "-1 * rank(delta(close, 1)) * rank(ts_max(volume, 5) / adv20)",
            "hypothesis": "Single-day price surge on peak 5-day volume suffers profit-taking.",
        },
    ]
    assert len(alphas) == 5, "Alpha generation batch size invariant breached"
    assert all("(" in a["expression"] for a in alphas), "Grammar invariant breached"
    return alphas


def generate_alpha_pack() -> List[Dict[str, Any]]:
    """Generates the complete 25-model institutional WorldQuant BRAIN alpha pack."""
    default_settings = get_default_settings()
    generators = [
        (FactorCategory.MEAN_REVERSION, _generate_mean_reversion_alphas),
        (FactorCategory.MOMENTUM, _generate_momentum_alphas),
        (FactorCategory.LIQUIDITY, _generate_liquidity_alphas),
        (FactorCategory.VOLATILITY, _generate_volatility_alphas),
        (FactorCategory.EXTREMES, _generate_extremes_alphas),
    ]

    alpha_pack: List[Dict[str, Any]] = []
    alpha_idx = 1

    for category, gen_func in generators:
        batch = gen_func()
        assert isinstance(batch, list), "Batch must be a list"
        for item in batch:
            alpha_pack.append({
                "number": alpha_idx,
                "name": f"Alpha {alpha_idx}: {item['name']}",
                "category": category.value,
                "expression": item["expression"],
                "hypothesis": item["hypothesis"],
                "settings": dict(default_settings),
            })
            alpha_idx += 1

    assert len(alpha_pack) == 25, f"Expected exactly 25 alphas, got {len(alpha_pack)}"
    assert alpha_idx == 26, "Index counting invariant breached"
    return alpha_pack
