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


def calculate_large_separation(frequencies):
    """
    Calculate the large frequency separation (Δν) using autocorrelation.

    The large separation is the average frequency difference between consecutive
    modes of the same spherical degree (l) and consecutive radial order (n).
    This fundamental asteroseismic parameter relates directly to mean stellar density.

    Uses autocorrelation of the frequency spectrum for robust estimation (standard
    method in asteroseismology). For roAp stars: typically 30-100 µHz.

    Parameters
    ----------
    frequencies : np.ndarray
        Array of detected peak frequencies

    Returns
    -------
    delta_nu : float
        Large frequency separation from autocorrelation peak
    delta_nu_err : float
        Uncertainty in Δν from autocorrelation peak width
    """
    if len(frequencies) < 5:
        warnings.warn("Insufficient peaks for Δν calculation (need ≥5 peaks).")
        return np.nan, np.nan

    freq_sorted = np.sort(frequencies)

    # Compute autocorrelation of frequency spectrum
    from scipy.signal import correlate
    auto = correlate(freq_sorted, freq_sorted, mode='full')
    auto = auto / auto.max()  # Normalize

    lags = np.arange(-len(freq_sorted) + 1, len(freq_sorted))

    # Find peaks in positive lag region (where Δν appears as secondary peak)
    positive_lags_idx = lags > 0
    auto_positive = auto[positive_lags_idx]
    lags_positive = lags[positive_lags_idx]

    # Find peaks in autocorrelation
    peaks_idx, properties = find_peaks(auto_positive, height=0.1, distance=2)

    if len(peaks_idx) < 1:
        warnings.warn("No autocorrelation peaks found. Using peak spacing fallback.")
        seps = np.diff(freq_sorted)
        delta_nu = np.median(seps[seps > 0.001])
        delta_nu_err = np.std(seps[seps > 0.001])
        return float(delta_nu), float(delta_nu_err)

    # First secondary peak gives Δν (most robust estimate)
    delta_nu_idx = peaks_idx[0]
    delta_nu = float(lags_positive[delta_nu_idx])

    # Error estimation: width of autocorrelation peak at half height
    peak_height = auto_positive[delta_nu_idx]
    half_height = peak_height / 2
    above_half = auto_positive > half_height

    # Find contiguous region around peak
    diffs = np.diff(above_half.astype(int))
    starts = np.where(diffs == 1)[0]
    ends = np.where(diffs == -1)[0]

    if len(starts) > 0 and len(ends) > 0:
        peak_region = ends[0] - starts[0] if starts[0] < ends[0] else len(above_half)
        delta_nu_err = float(peak_region / np.sqrt(len(frequencies)))
    else:
        delta_nu_err = float(np.std(np.diff(freq_sorted)))

    return float(delta_nu), float(delta_nu_err)


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
