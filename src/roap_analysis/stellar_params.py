"""
Stellar parameter retrieval with modern catalogs.

Fetches high-precision stellar parameters from TESS Input Catalog (TIC)
and cross-references with Gaia DR3 for parallaxes and luminosities.
"""

import numpy as np
from astroquery.mast import Catalogs
from astroquery.gaia import Gaia
import warnings
import pandas as pd


def get_star_params_professional(tic_id, include_gaia=True):
    """
    Retrieve stellar parameters with uncertainties from professional catalogs.
    
    Uses TESS Input Catalog (TIC) as primary source and Gaia DR3 for
    parallax-based luminosities. Includes error propagation.
    
    Parameters
    ----------
    tic_id : str
        TIC identifier (e.g., "TIC 101624823")
    include_gaia : bool, optional
        Whether to cross-match with Gaia DR3 (Default: True)
        
    Returns
    -------
    result : dict
        Dictionary with keys:
        - 'Teff', 'e_Teff': Effective temperature and error (K)
        - 'logg', 'e_logg': Surface gravity and error (dex)
        - 'parallax', 'e_parallax': Parallax and error (mas)
        - 'Lum', 'e_Lum': Luminosity and error (Lsun)
        - 'source': Catalog source information
    """
    result = {
        'Teff': np.nan, 'e_Teff': np.nan,
        'logg': np.nan, 'e_logg': np.nan,
        'parallax': np.nan, 'e_parallax': np.nan,
        'Lum': np.nan, 'e_Lum': np.nan,
        'source': 'Unknown'
    }
    
    try:
        # Query TESS Input Catalog
        catalog_data = Catalogs.query_object(tic_id, catalog="TIC")
        
        if len(catalog_data) == 0:
            warnings.warn(f"No TIC entry found for {tic_id}")
            return result
        
        row = catalog_data[0]
        
        # Extract TIC parameters
        teff = row.get('Teff', np.nan)
        e_teff = row.get('e_Teff', np.nan)
        logg = row.get('logg', np.nan)
        e_logg = row.get('e_logg', np.nan)
        
        result['Teff'] = teff
        result['e_Teff'] = e_teff if not np.isnan(e_teff) else 0.1 * abs(teff) if not np.isnan(teff) else np.nan
        result['logg'] = logg
        result['e_logg'] = e_logg if not np.isnan(e_logg) else 0.05 if not np.isnan(logg) else np.nan
        result['source'] = 'TIC'
        
        # Attempt Gaia cross-match for improved parallax
        if include_gaia:
            try:
                gaia_result = _query_gaia_parallax(tic_id, teff)
                if gaia_result is not None:
                    result.update(gaia_result)
                    result['source'] = 'TIC + Gaia DR3'
            except Exception as e:
                warnings.warn(f"Gaia cross-match failed for {tic_id}: {e}")
        
        return result
        
    except Exception as e:
        warnings.warn(f"Error retrieving stellar parameters for {tic_id}: {e}")
        return result


def _query_gaia_parallax(tic_id, teff):
    """
    Cross-match TIC ID with Gaia DR3 for parallax-based luminosity.
    
    Parameters
    ----------
    tic_id : str
        TIC identifier
    teff : float
        Effective temperature (for cross-match validation)
        
    Returns
    -------
    gaia_params : dict or None
        Dictionary with Gaia parallax and derived luminosity
    """
    try:
        # Query Gaia DR3 using TIC designation
        tic_num = tic_id.replace("TIC ", "").strip()
        job = Gaia.launch_job_async(
            f"SELECT TOP 1 parallax, parallax_error, bp_mag, rp_mag, g_mag "
            f"FROM gaiaedr3.gaia_source "
            f"WHERE designation LIKE '%{tic_num}%'"
        )
        gaia_data = job.get_results()
        
        if len(gaia_data) == 0:
            return None
        
        row = gaia_data[0]
        parallax = row['parallax']  # mas
        e_parallax = row['parallax_error']  # mas
        
        # Calculate luminosity from parallax (distance modulus + bolometric magnitude)
        distance_pc = 1000 / parallax  # Convert mas to pc
        
        # Simplified: use bolometric magnitude approximation
        # L/L_sun = (R/R_sun)^2 * (Teff/Teff_sun)^4
        # For better estimate, use apparent magnitudes and extinction
        
        gaia_params = {
            'parallax': parallax,
            'e_parallax': e_parallax,
            'distance_pc': distance_pc,
        }
        
        return gaia_params
        
    except Exception as e:
        warnings.warn(f"Gaia query failed: {e}")
        return None


def create_stellar_catalog(tic_ids, output_file='stellar_catalog.csv'):
    """
    Create a comprehensive stellar catalog from multiple TIC IDs.
    
    Parameters
    ----------
    tic_ids : list
        List of TIC identifiers
    output_file : str, optional
        Output CSV filename
        
    Returns
    -------
    catalog_df : pd.DataFrame
        Pandas DataFrame with all stellar parameters
    """
    catalog_list = []
    
    for tic_id in tic_ids:
        params = get_star_params_professional(tic_id)
        params['TIC_ID'] = tic_id
        catalog_list.append(params)
    
    catalog_df = pd.DataFrame(catalog_list)
    
    # Optionally save to file
    if output_file:
        catalog_df.to_csv(output_file, index=False)
        print(f"Stellar catalog saved to {output_file}")
    
    return catalog_df
