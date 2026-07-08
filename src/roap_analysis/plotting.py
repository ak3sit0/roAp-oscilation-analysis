"""
Publication-quality plotting functions for roAp asteroseismic analysis.

Handles HR diagrams, periodograms, and evolution tracks with consistent styling.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import warnings

from .config import FIGURES_DIR, TRACK_COLOR, TRACK_ALPHA, TEFF_COLOR


def set_publication_style():
    """Apply publication-quality matplotlib style."""
    plt.rcParams['font.size'] = 11
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['figure.figsize'] = (10, 8)
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 13
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['lines.linewidth'] = 1.5
    plt.rcParams['patch.linewidth'] = 0.5
    plt.rcParams['axes.grid'] = True
    plt.rcParams['axes.grid.alpha'] = 0.3
    plt.rcParams['axes.axisbelow'] = True


def plot_periodogram(lightcurve, periodogram, peaks_idx=None, 
                     amplitude_ppm=None, ax=None, title=None):
    """
    Plot amplitude periodogram with peak annotations.
    
    Parameters
    ----------
    lightcurve : lightkurve.LightCurve
        Input light curve
    periodogram : lightkurve.Periodogram
        Computed periodogram
    peaks_idx : np.ndarray, optional
        Indices of significant peaks
    amplitude_ppm : np.ndarray, optional
        Amplitude array in ppm
    ax : matplotlib.axes.Axes, optional
        Existing axis for plotting
    title : str, optional
        Plot title
        
    Returns
    -------
    ax : matplotlib.axes.Axes
        Axes object
    """
    set_publication_style()
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 5))
    
    # Plot periodogram
    frequencies = periodogram.frequency.value
    if amplitude_ppm is None:
        amplitude_ppm = periodogram.power.value * 1e6
    
    ax.plot(frequencies, amplitude_ppm, 'k-', linewidth=0.8, label='Amplitude Spectrum')
    
    # Mark significant peaks
    if peaks_idx is not None and len(peaks_idx) > 0:
        peak_freqs = frequencies[peaks_idx]
        peak_amps = amplitude_ppm[peaks_idx]
        
        ax.scatter(peak_freqs, peak_amps, color=TEFF_COLOR, s=80, 
                  zorder=5, label=f'Peaks (N={len(peaks_idx)})', marker='*')
        
        # Annotate dominant peak
        dom_idx = np.argmax(peak_amps)
        ax.annotate(f'{peak_freqs[dom_idx]:.2f} d$^{{-1}}$',
                   xy=(peak_freqs[dom_idx], peak_amps[dom_idx]),
                   xytext=(10, 10), textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    ax.set_xlabel('Frequency (d$^{-1}$)')
    ax.set_ylabel('Amplitude (ppm)')
    if title:
        ax.set_title(title)
    ax.legend(loc='upper right', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    
    return ax


def plot_hr_diagram(teff_list, logg_list, e_teff=None, e_logg=None,
                    track_data=None, tic_ids=None, output_file=None):
    """
    Create publication-quality HR diagram with evolutionary tracks.
    
    Parameters
    ----------
    teff_list : list or array
        Effective temperatures (K)
    logg_list : list or array
        Surface gravities (dex)
    e_teff : list or array, optional
        Temperature uncertainties (K)
    e_logg : list or array, optional
        Gravity uncertainties (dex)
    track_data : list of tuples, optional
        List of (DataFrame, label) pairs for evolutionary tracks
    tic_ids : list, optional
        TIC identifiers for annotations
    output_file : str, optional
        Filename for saving figure (PDF format)
        
    Returns
    -------
    fig, ax : matplotlib figure and axes objects
    """
    set_publication_style()
    
    fig, ax = plt.subplots(figsize=(11, 9))
    
    # Plot evolutionary tracks
    if track_data:
        for track_df, mass_label in track_data:
            teff_track = 10 ** track_df['logTeff']
            logg_track = track_df['grav']
            
            # Filter valid data
            valid = np.isfinite(teff_track) & np.isfinite(logg_track)
            
            if np.any(valid):
                ax.plot(teff_track[valid], logg_track[valid], 
                       color=TRACK_COLOR, alpha=TRACK_ALPHA, linewidth=1.2)
                
                # Label the track
                idx = np.where(valid)[0][0]
                ax.text(teff_track.iloc[idx], logg_track.iloc[idx] - 0.15,
                       mass_label, fontsize=9, alpha=0.7)
    
    # Plot observed stars with error bars
    if len(teff_list) > 0:
        if e_teff is None:
            e_teff = np.ones_like(teff_list) * 50  # Default error
        if e_logg is None:
            e_logg = np.ones_like(logg_list) * 0.05  # Default error
        
        ax.errorbar(teff_list, logg_list, xerr=e_teff, yerr=e_logg,
                   fmt='*', markersize=15, color=TEFF_COLOR, 
                   ecolor='black', elinewidth=1.5, capsize=4,
                   label='roAp Stars (TESS)', zorder=5)
        
        # Annotate with TIC IDs if provided
        if tic_ids and len(tic_ids) == len(teff_list):
            for i, (t, g, tic) in enumerate(zip(teff_list, logg_list, tic_ids)):
                tic_num = tic.replace("TIC ", "")
                ax.annotate(tic_num, xy=(t, g), xytext=(5, 5),
                           textcoords='offset points', fontsize=7, alpha=0.6)
    
    # Formatting
    ax.invert_xaxis()
    ax.invert_yaxis()
    ax.set_xlabel(r'Effective Temperature $T_{\mathrm{eff}}$ (K)', fontsize=12)
    ax.set_ylabel(r'Surface Gravity $\log g$ (dex)', fontsize=12)
    ax.set_title('Hertzsprung-Russell Diagram: roAp Stars from TESS', fontsize=13)
    ax.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax.grid(True, alpha=0.4, linestyle='--')
    
    # Add ZAMS and TAMS annotations if applicable
    ax.text(0.98, 0.02, 'Main Sequence', transform=ax.transAxes,
           ha='right', va='bottom', fontsize=9, alpha=0.6, style='italic')
    
    plt.tight_layout()
    
    # Save figure
    if output_file:
        output_path = FIGURES_DIR / output_file
        fig.savefig(output_path, dpi=300, bbox_inches='tight', format='pdf')
        print(f"HR diagram saved to {output_path}")
    
    return fig, ax


def plot_light_curves(lightcurves, tic_id, output_file=None):
    """
    Plot multiple light curves for a single star.
    
    Parameters
    ----------
    lightcurves : list
        List of lightkurve.LightCurve objects
    tic_id : str
        Star identifier
    output_file : str, optional
        Filename for saving figure
        
    Returns
    -------
    fig : matplotlib figure
    """
    set_publication_style()
    
    n_lc = len(lightcurves)
    fig, axes = plt.subplots(n_lc, 1, sharex=False, figsize=(12, 3 * n_lc))
    
    if n_lc == 1:
        axes = [axes]
    
    for i, lc in enumerate(lightcurves):
        ax = axes[i]
        lc.plot(ax=ax, color='navy', linewidth=0.7)
        ax.set_ylabel('Normalized Flux')
        ax.grid(True, alpha=0.3)
        ax.set_title(f'{tic_id} - Sector {i+1}')
    
    axes[-1].set_xlabel('Time (days)')
    fig.suptitle(f'Light Curves: {tic_id}', fontsize=13, y=1.00)
    plt.tight_layout()
    
    if output_file:
        output_path = FIGURES_DIR / output_file
        fig.savefig(output_path, dpi=300, bbox_inches='tight', format='pdf')
        print(f"Light curve figure saved to {output_path}")
    
    return fig
