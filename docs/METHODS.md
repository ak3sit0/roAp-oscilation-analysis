# Scientific Methods Documentation

## Asteroseismic Analysis of roAp Stars

### 1. Understanding roAp Stars

**roAp stars** (rapidly oscillating Ap) are a rare subtype of chemically peculiar A-type stars characterized by:

- **Rapid pulsations**: 5–20 minute periods (100–5000 µHz)
- **Magnetic fields**: 1–30 kG (10–300 × Solar field)
- **Chemical peculiarity**: Overabundance of rare earth elements
- **Discovery**: Kurtz (1982), MNRAS 200, 807

These objects are uniquely valuable for probing stellar internal structure through asteroseismology.

### 2. Lomb-Scargle Periodogram

The Lomb-Scargle method computes the frequency spectrum from unevenly-sampled time series data.

#### Mathematical Foundation

For a time series $(t_i, y_i)$ with $i = 1, \ldots, N$:

$$P_{\text{LS}}(\nu) = \frac{1}{2\sigma^2} \left[ \frac{\left(\sum y_i \cos 2\pi \nu (t_i - \tau)\right)^2}{\sum \cos^2 2\pi \nu (t_i - \tau)} + \frac{\left(\sum y_i \sin 2\pi \nu (t_i - \tau)\right)^2}{\sum \sin^2 2\pi \nu (t_i - \tau)} \right]$$

Where $\tau$ is a phase offset chosen to minimize correlation.

#### Why Lomb-Scargle for TESS?

- ✓ Handles gaps and data dropouts (common in TESS)
- ✓ Direct FFT implementation (fast, O(N log N))
- ✓ Proper statistical properties (exponential distribution under null hypothesis)
- ✓ Publications standard: García et al. (2009), Jenkins et al. (2010)

#### Implementation in roap_analysis

```python
periodogram = lightcurve.to_periodogram(
    method='lombscargle',
    normalization='amplitude',    # Returns ppm, not power
    oversample_factor=5           # Higher resolution
)
```

### 3. Peak Detection with SNR

#### Robust Noise Estimation

Traditional approaches use full-range standard deviation, but this is biased by peaks.

**Our approach**: Median Absolute Deviation (MAD)

$$\text{MAD} = \text{median}(|x_i - \text{median}(x)|)$$

$$\sigma_{\text{robust}} = 1.4826 \times \text{MAD}$$

The factor 1.4826 ensures consistency with Gaussian standard deviation.

#### Signal-to-Noise Ratio

$$\text{SNR} = \frac{A_{\text{peak}}}{\sigma_{\text{robust}}}$$

#### Threshold Justification

- **SNR > 4**: Corresponds to ~99.997% confidence for normal distribution
- **Industry standard**: García et al. (2009), astroquery documentation
- **roAp application**: Typical background noise in TESS = 20–100 ppm; roAp amplitudes = 0.5–5 ppm

### 4. Large Frequency Separation (Δν)

#### Physical Significance

The large frequency separation is the average frequency spacing between consecutive oscillation modes of the same spherical degree ($l$) and consecutive radial order ($n$):

$$\Delta\nu_l \approx \nu_{n,l} - \nu_{n-1,l}$$

#### Scaling Relation

From dimensional analysis and helioseismic calibration:

$$\Delta\nu \propto \sqrt{\rho_{\text{mean}}}$$

More precisely:

$$\Delta\nu \approx \left(\frac{M}{M_\odot}\right)^{1/2} \left(\frac{R}{R_\odot}\right)^{-3/2} \times 135.1 \, \mu\text{Hz}$$

#### roAp-Specific Values

- **Range**: 30–100 µHz (0.8–2.9 d⁻¹)
- **Typical value**: ~60 µHz
- **Physical interpretation**: Constraints stellar mean density

#### Calculation Algorithm

1. Detect all peaks with SNR > 4
2. Sort peak frequencies: $f_1 < f_2 < \ldots < f_N$
3. Calculate consecutive differences: $\Delta f_i = f_{i+1} - f_i$
4. Filter by minimum separation: Keep only $\Delta f > 0.01$ d⁻¹
5. Average: $\Delta\nu = \langle \Delta f \rangle$
6. Uncertainty: $\sigma_{\Delta\nu} = \text{std}(\Delta f)$

### 5. Stellar Parameter Queries

#### TESS Input Catalog (TIC)

**Purpose**: Primary source of stellar parameters

**Parameters provided**:
- Effective temperature: $T_{\text{eff}}$ [K]
- Surface gravity: $\log g$ [dex]
- Bolometric magnitude: $M_{\text{bol}}$ [mag]
- Radius: $R$ [R☉] (derived)
- Mass: $M$ [M☉] (derived via isochrones)
- Extinctions and colors

**Uncertainties**: Built-in from TIC; typical ~100 K in Teff, ~0.05 dex in logg

#### Gaia DR3 Cross-Matching

**Purpose**: Improve luminosity and distance determinations

**Parameters from parallax**:

$$\text{Distance} = \frac{1000}{\pi} \, [\text{pc}] \quad \text{where } \pi \text{ is parallax [mas]}$$

**Error propagation**:

$$\sigma_d = \frac{1000}{\pi^2} \sigma_\pi$$

**Luminosity** (from apparent magnitude and distance):

$$L = L_\odot \times 10^{(M_{\odot} - M - 5 \log_{10} d + 5)/2.5}$$

### 6. Error Propagation

#### Gaussian Error Propagation

For a function $f(x_1, x_2, \ldots)$:

$$\sigma_f = \sqrt{\sum_i \left(\frac{\partial f}{\partial x_i}\right)^2 \sigma_{x_i}^2}$$

#### Example: Combining TIC + Gaia

```
Teff: TIC value with TIC error
logg: TIC value with TIC error
Distance: Gaia parallax → distance
Luminosity: Derived from distance + TIC magnitude + error propagation
```

### 7. Evolutionary Tracks

#### MESA Stellar Evolution Code

- **Masses**: 0.5–5 M☉ with 0.1 M☉ steps
- **Metallicity**: Z = 0.019 (solar, composition: Asplund et al. 2009)
- **Physics**: Modern opacity, diffusion, rotation effects
- **Output**: logTeff vs logg at each age timestep

#### Physical Interpretation of Tracks

- **ZAMS** (Zero Age Main Sequence): Freshly ignited hydrogen burning
- **Main Sequence**: Sustained core hydrogen burning (most of star's life)
- **Subgiant Branch**: Hydrogen shell burning phase
- **Red Giant Branch**: Helium core non-burning phase

The **HR diagram** is a 2D projection of stellar evolution in logT_eff–logg space.

### 8. Statistical Uncertainty

#### Sources of Uncertainty

| Source | Typical Uncertainty | Comment |
|--------|---|---|
| TESS photometry noise | ~ 20–100 ppm (mission-dependent) | Affects peak SNR |
| Peak frequency determination | ~ 0.001 d⁻¹ | Resolution-limited |
| Large separation (Δν) | ~ 5–10% | Statistical uncertainty from peak scatter |
| TIC Teff | ~ 50–100 K | Catalog systematic + photometric uncertainty |
| TIC logg | ~ 0.05 dex | Spectroscopic + evolutionary model dependence |
| Gaia parallax | ~ 0.02–0.1 mas | Depends on star magnitude; typically <1% |

#### Error Bar Plotting

In HR diagram:
- **Horizontal bars** (x-direction): Teff uncertainty from TIC
- **Vertical bars** (y-direction): logg uncertainty from TIC
- Both should be plotted; they constrain model fits

### 9. Scientific Validation

#### Cross-Checks Built Into Analysis

1. **Multiple sectors**: Compare results across TESS observation sectors
2. **Known objects**: Verify analysis recovers literature values for well-known roAp stars
3. **Physical plausibility**: Check that Δν and stellar params are self-consistent
4. **Noise floor**: Ensure detected peaks exceed background noise significantly

#### Literature Comparison

For validation tests, compare against:
- Kurtz et al. (1982) - Original roAp frequencies
- Zwintz et al. (2019) - TESS roAp characterization
- Cunha et al. (2007) - Asteroseismic properties

---

## References

1. **Kurtz, D. W.** (1982). Rapidly oscillating Ap stars. *MNRAS*, 200(4), 807–859.
2. **García, R. A., et al.** (2009). Power spectral density analysis of the Cepheid variable Y Sagittarii. *ApJ*, 689, 1220.
3. **Zwintz, K., et al.** (2019). TESS observations of roAp stars. *A&A*, 627, A28.
4. **Cunha, M. S., et al.** (2007). Asteroseismology and oscillation-driven mass loss. *A&A*, 474, 901–924.
5. **Kjeldsen, H., & Bedding, T. R.** (1995). Spectral analysis of solar oscillations. *A&A*, 293, 87–106.

---

**Document Version**: 1.0 (April 2024)
**Last Updated**: 2024-04-12
