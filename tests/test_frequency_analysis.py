"""Smoke tests for the frequency-analysis core.

These are lightweight sanity checks (no network, no TESS downloads) covering
unit conversion, peak detection, and the Δν guard clauses.
"""
import numpy as np
import pytest

from roap_analysis import estimate_snr, calculate_large_separation, to_microhertz


def test_to_microhertz_scalar():
    # 1 cycle/day = 1/86400 Hz = 11.57407... µHz
    assert to_microhertz(1.0) == pytest.approx(1e6 / 86400.0, rel=1e-9)


def test_to_microhertz_array():
    out = to_microhertz(np.array([1.0, 2.0]))
    assert out.shape == (2,)
    assert out[1] == pytest.approx(2 * 1e6 / 86400.0, rel=1e-9)


def test_estimate_snr_detects_injected_peak():
    rng = np.random.default_rng(0)
    amplitude = np.abs(rng.normal(0.0, 1.0, size=500)) + 0.1
    spike = 250
    amplitude[spike] = 100.0  # unambiguous peak well above the noise floor

    peaks = estimate_snr(amplitude, height_factor=4.0)
    assert spike in np.asarray(peaks)


def test_calculate_large_separation_needs_five_peaks():
    dv, err = calculate_large_separation(np.array([1.0, 2.0, 3.0]))
    assert np.isnan(dv) and np.isnan(err)


def test_calculate_large_separation_returns_finite_for_comb():
    freqs = np.array([10.0, 12.0, 14.0, 16.0, 18.0, 20.0])
    dv, err = calculate_large_separation(freqs)
    assert np.isfinite(dv)
    assert dv > 0
