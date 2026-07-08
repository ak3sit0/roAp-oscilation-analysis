"""
Main analysis notebook for roAp asteroseismic study.

This notebook demonstrates the complete analysis pipeline from light curve
download through stellar characterization and Hertzsprung-Russell diagram generation.

TESS Mission Data: https://tess.mit.edu/
roAp Research Context: Kurtz et al. 1982 MNRAS 200, 807-859
"""

# ============================================================================
# 1. IMPORTS AND SETUP
# ============================================================================

import sys
from pathlib import Path

# Add src to path for module imports
sys.path.insert(0, str(Path.cwd().parent / "src"))

import lightkurve as lk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import median_abs_deviation

# Import the professional analysis modules
from roap_analysis import (
    estimate_snr,
    calculate_large_separation,
    periodogram_analysis,
    get_star_params_professional,
    plot_periodogram,
    plot_hr_diagram
)
from roap_analysis.config import FIGURES_DIR, RESULTS_DIR, TRACK_MASSES, TRACK_METALLICITY

print("✓ All dependencies loaded successfully")
print(f"✓ Output figures directory: {FIGURES_DIR}")
print(f"✓ Results directory: {RESULTS_DIR}")

# ============================================================================
