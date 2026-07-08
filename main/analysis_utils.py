import numpy as np
import pandas as pd
from astroquery.mast import Catalogs
from scipy.signal import find_peaks

def get_star_params_professional(tic_id):
    """
    Fetches stellar parameters from TIC with errors.
    """
    catalog_data = Catalogs.query_object(f"{tic_id}", catalog="TIC")
    if len(catalog_data) > 0:
        teff = catalog_data[0]['Teff']
        e_teff = catalog_data[0]['e_Teff']
        logg = catalog_data[0]['logg']
        e_logg = catalog_data[0]['e_logg']
        return teff, e_teff, logg, e_logg
    return None, None, None, None

def calculate_large_separation(peak_freqs):
    """
    Calculates the large frequency separation (Delta nu) from detected peaks.
    Standardized to microHertz (uHz) for roAp research.
    """
    if len(peak_freqs) < 2:
        return np.nan
    
    # Sort peaks
    sorted_freqs = np.sort(peak_freqs)
    # Convert from 1/day to microHertz (uHz)
    # 1/day = 11.574 microHz
    freqs_uhz = sorted_freqs * 11.574
    
    diffs = np.diff(freqs_uhz)
    # Return mean difference as Delta Nu (rough estimate)
    return np.mean(diffs)

def estimate_snr(power, threshold=4):
    """
    Identifies peaks with a S/N ratio above standard research threshold.
    """
    median_power = np.median(power)
    peaks, _ = find_peaks(power, height=median_power * threshold)
    return peaks
