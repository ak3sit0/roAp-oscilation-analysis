"""
Configuration and constants for roAp asteroseismic analysis.
"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
CSV_DIR = PROJECT_ROOT / "csv"
SEQUENCES_DIR = PROJECT_ROOT / "sequences"
FIGURES_DIR = PROJECT_ROOT / "figures"
RESULTS_DIR = PROJECT_ROOT / "results"

# Ensure directories exist
for directory in [FIGURES_DIR, RESULTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Stellar evolution track configurations
TRACK_MASSES = [1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.5]
TRACK_METALLICITY = "z019"  # Z ≈ 0.019, solar metallicity

# roAp frequency ranges (in µHz and 1/days)
ROAP_FREQ_RANGE_UHHZ = (100, 5000)  # typical range in microhertz
ROAP_FREQ_RANGE_D1 = (0.001, 0.057)  # typical range in 1/days
D1_TO_UHZ = 1e6 / 86400.0  # ≈ 11.57407 µHz per (day⁻¹)

# SNR threshold for significant peaks
SNR_THRESHOLD = 4.0

# Periodogram parameters
LOMBSCARGLE_OVERSAMPLE = 5
AMPLITUDE_NORMALIZATION = 'amplitude'  # Return amplitudes in ppm

# HR Diagram parameters
TEFF_COLOR = "#E74C3C"  # Red
TRACK_COLOR = "#34495E" # Dark gray
TRACK_ALPHA = 0.4
