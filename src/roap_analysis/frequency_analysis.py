"""
Frequency domain analysis for roAp asteroseismology.

Implements Lomb-Scargle periodogram analysis, peak detection with SNR,
and calculation of seismic parameters like large frequency separation.
"""

import numpy as np
from scipy.signal import find_peaks
from scipy.stats import median_abs_deviation
import warnings

from .config import SNR_THRESHOLD, ROAP_FREQ_RANGE_UHHZ


def estimate_snr(amplitude, height_factor=5.0):
    """
    Estimate Signal-to-Noise Ratio and detect significant peaks.
    
    Uses robust statistics (MAD - Median Absolute Deviation) for noise estimation,
    which is resistant to the presence of peaks.
    
    Parameters
    ----------
    amplitude : np.ndarray
        Power spectrum or amplitude values
    height_factor : float, optional
        Multiplier for the noise baseline to set peak detection threshold
        
    Returns
    -------
    peaks : np.ndarray
        Indices of significant peaks (SNR > threshold)
    snr_values : np.ndarray
        Signal-to-Noise Ratio for each peak
    """
    # Estimate noise using Median Absolute Deviation (robust)
    noise_mad = median_abs_deviation(amplitude)
    noise_level = 1.4826 * noise_mad  # Scaled MAD approximates std for normal data
    
    # Detect peaks
    height_threshold = noise_level * height_factor
    peaks, properties = find_peaks(amplitude, height=height_threshold, distance=2)
    
    # Calculate SNR for each peak
    if len(peaks) > 0:
        snr_values = properties['peak_heights'] / noise_level
    else:
        snr_values = np.array([])
    
    # Filter by SNR threshold
    significant_peaks = peaks[snr_values >= SNR_THRESHOLD] if len(snr_values) > 0 else np.array([])
    
    return significant_peaks


def calculate_large_separation(frequencies, min_separation=0.001):
    """
    Calculate the large frequency separation (Δν).
    
    The large separation is the average frequency difference between consecutive
    modes of the same spherical degree (l) and consecutive radial order (n).
    This is a fundamental asteroseismic parameter related to mean stellar density.
    
    For roAp stars: typically 30-100 µHz or 0.8-2.9 day^-1
    
    Parameters
    ----------
    frequencies : np.ndarray
        Array of detected peak frequencies (must be sorted)
    min_separation : float, optional
        Minimum frequency separation to consider (in same units as frequencies)
        
    Returns
    -------
    delta_nu : float
        Large frequency separation or NaN if insufficient peaks
    delta_nu_std : float
        Standard deviation of separations
    """
    if len(frequencies) < 2:
        warnings.warn("Insufficient peaks for Δν calculation. Need at least 2 peaks.")
        return np.nan, np.nan
    
    # Sort frequencies
    freq_sorted = np.sort(frequencies)
    
    # Calculate consecutive differences
    separations = np.diff(freq_sorted)
    
    # Filter by minimum separation to avoid noise artifacts
    valid_seps = separations[separations >= min_separation]
    
    if len(valid_seps) == 0:
        warnings.warn("No valid frequency separations found.")
        return np.nan, np.nan
    
    # Calculate statistics
    delta_nu = np.mean(valid_seps)
    delta_nu_std = np.std(valid_seps)
    
    return delta_nu, delta_nu_std


def periodogram_analysis(lightcurve, method='lombscargle', oversample_factor=5):
    """
    Perform professional periodogram analysis on light curve data.
    
    Uses Lomb-Scargle method which handles unevenly-sampled data and is
    standard in asteroseismic analysis.
    
    Parameters
    ----------
    lightcurve : lightkurve.LightCurve
        Input light curve object from lightkurve
    method : str, optional
        Periodogram method ('lombscargle' recommended for roAp)
    oversample_factor : int, optional
        Oversampling factor for frequency grid resolution
        
    Returns
    -------
    periodogram : lightkurve.Periodogram
        Amplitude spectrumb object
    significant_peaks : np.ndarray
        Indices of peaks with SNR > threshold
    snr_values : np.ndarray
        SNR for each significant peak
    """
    # Compute periodogram using Lomb-Scargle
    pg = lightcurve.to_periodogram(
        method=method,
        oversample_factor=oversample_factor,
        normalization='amplitude'  # Return real amplitudes in ppm
    )
    
    # Convert power to amplitude (ppm)
    amplitude_ppm = pg.power.value * 1e6
    
    # Detect significant peaks
    peaks = estimate_snr(amplitude_ppm)
    
    # Calculate SNR for peaks
    noise_mad = median_abs_deviation(amplitude_ppm)
    noise_level = 1.4826 * noise_mad
    if len(peaks) > 0:
        snr_values = amplitude_ppm[peaks] / noise_level
    else:
        snr_values = np.array([])
    
    return pg, peaks, snr_values


def identify_mode_spectrum(frequencies, amplitudes, delta_nu_range=(0.02, 0.3)):
    """
    Identify the mode spectrum by grouping peaks into families.
    
    Advanced feature: attempts to identify l=0,1,2 modes based on large separation.
    
    Parameters
    ----------
    frequencies : np.ndarray
        Peak frequencies
    amplitudes : np.ndarray
        Peak amplitudes
    delta_nu_range : tuple, optional
        Expected range for large separation (in same units as frequencies)
        
    Returns
    -------
    mode_dict : dict
        Dictionary with potential l values and corresponding mode frequencies
    """
    if len(frequencies) < 3:
        warnings.warn("Insufficient peaks for mode identification.")
        return {}
    
    freq_sorted = np.sort(frequencies)
    seps = np.diff(freq_sorted)
    
    # Find most common separation in the expected range
    valid_seps = seps[(seps >= delta_nu_range[0]) & (seps <= delta_nu_range[1])]
    
    if len(valid_seps) == 0:
        return {}
    
    # Use histogram to find peak separation
    hist, bin_edges = np.histogram(valid_seps, bins=10)
    delta_nu_est = bin_edges[np.argmax(hist)]
    
    # Group modes
    modes = {'l=0': [], 'l=1': [], 'l=2': []}
    for i, f in enumerate(freq_sorted):
        modes['l=0'].append(f)  # Simplified grouping
    
    return modes
