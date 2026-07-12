"""
roap_analysis: Asteroseismic Analysis of Rapidly Oscillating Ap Stars

A professional Python package for analyzing TESS light curves of roAp stars,
including frequency analysis, stellar characterization, and HR diagram generation.

References:
    Kurtz, D. W. (1982). Rapidly oscillating Ap stars. MNRAS, 200(4), 807-859.
    Cunha, M. S., et al. (2007). Asteroseismology and Oscillation-Driven Mass Loss in Hot Stars.
"""

__version__ = "1.0.0"
__author__ = "José Ake"

from .frequency_analysis import (
    estimate_snr,
    calculate_large_separation,
    periodogram_analysis,
    to_microhertz,
)
from .stellar_params import get_star_params_professional
from .plotting import plot_periodogram, plot_hr_diagram

__all__ = [
    'estimate_snr',
    'calculate_large_separation',
    'periodogram_analysis',
    'to_microhertz',
    'get_star_params_professional',
    'plot_periodogram',
    'plot_hr_diagram',
]
