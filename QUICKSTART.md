# Quick Start Guide: Running the Professional Analysis

## 🎯 Goal
Execute the complete asteroseismic analysis pipeline and generate publication-quality results in ~10-15 minutes.

---

## ⚡ Express Setup (5 minutes)

### Prerequisites
- Python 3.9+ installed
- Internet connection (for TESS/Gaia data download)
- ~2 GB disk space (light curve cache)

### Installation

```bash
# Navigate to project
cd /home/joseangel/Documents/Proyectos/Analisis\ de\ oscilaciones\ roAp

# Option A: Conda (Recommended)
conda env create -f environment.yml
conda activate roap-analysis

# Option B: pip + venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Verify installation**:
```python
python -c "import roap_analysis; print(f'✓ roap_analysis {roap_analysis.__version__}')"
```

---

## 🚀 Running the Analysis (10 min)

### Method 1: Jupyter Notebook (Interactive)

```bash
jupyter notebook notebooks/main.ipynb
```

**What happens**:
1. Cell 1: Loads libraries and modules
2. Cell 2: Defines 6 target roAp stars
3. Cells 3-8: Downloads TESS data for first target (TIC 101624823)
4. Cells 9-12: Analyzes first target in detail
   - Downloads light curves
   - Computes periodograms
   - Detects peaks (SNR > 4)
   - Calculates large frequency separation (Δν)
5. Cells 13-15: Batch analysis of ALL targets
6. Cell 16: Generates professional HR diagram
7. Cell 17: Summary statistics

**Output files** (saved to `figures/` and `results/`):
```
figures/
├── TIC_101624823_lightcurves.pdf
├── TIC_101624823_periodogram.pdf
└── HR_diagram_professional.pdf

results/
├── stellar_catalog.csv
└── analysis_results.csv
```

**Estimated runtime**: 5–10 minutes (depends on internet speed)

---

## 📊 Understanding the Results

### 1. **stellar_catalog.csv**
Complete stellarmulti-source catalog:

| Column | Description | Example |
|--------|-------------|---------|
| TIC_ID | TESS catalog ID | TIC 101624823 |
| Teff | Effective temperature (K) | 8250 |
| e_Teff | Temperature uncertainty | 75 |
| logg | Surface gravity (dex) | 4.15 |
| e_logg | Gravity uncertainty | 0.08 |
| parallax | Gaia parallax (mas) | 5.42 |
| source | Catalog source | "TIC + Gaia DR3" |

**Use**: HR diagram positioning, physical characteristics

### 2. **analysis_results.csv**
Asteroseismic parameters:

| Column | Description | Example |
|--------|-------------|---------|
| TIC_ID | Target identifier | TIC 101624823 |
| N_peaks | Detected oscillation modes | 12 |
| DominantFreq_d1 | Primary pulsation (d⁻¹) | 0.0348 |
| DominantFreq_uHz | Primary pulsation (µHz) | 403 |
| DeltaNu_d1 | Large separation (d⁻¹) | 0.0087 |
| MaxAmplitude_ppm | Strongest signal (ppm) | 2.34 |
| MeanAmplitude_ppm | Average amplitude | 0.87 |
| Teff_K | Effective temperature | 8250 |
| logg_dex | Surface gravity | 4.15 |

**Use**: Seismic characterization, mode identification

### 3. **Periodogram Figures**
Example: `TIC_101624823_periodogram.pdf`

**What you see**:
- Horizontal line: Amplitude spectrum (black)
- Red stars (✱): Detected peaks with SNR > 4
- Yellow annotation: Dominant frequency marked
- Multiple peaks: Typical oscillation pattern for roAp

**Physical interpretation**:
- Peak spacing ≈ Δν (related to stellar density)
- Amplitudes 0.5–5 ppm (typical for TESS roAp)
- 12–15 modes detected (confirms roAp classification)

### 4. **HR Diagram**
`HR_diagram_professional.pdf`

**What you see**:
- Gray lines: Evolutionary tracks (1.5–2.5 M☉)
- Red stars (✱): Observed roAp stars with error bars
- TIC IDs labeled next to each star

**Physical interpretation**:
- Stars cluster near main sequence (expected)
- Error bars show measurement uncertainty
- Position indicates stellar mass and age

---

## 🔍 Troubleshooting

### Issue: "No SPOC 120s data found"
**Cause**: TESS has not observed that target yet
**Solution**: Check [TESS homepage](https://tess.mit.edu/) for available sectors

### Issue: Gaia query times out
**Cause**: ESA server temporarily unavailable
**Solution**: Analysis continues without Gaia (uses TIC only); try again later

### Issue: "ModuleNotFoundError: No module named 'roap_analysis'"
**Cause**: Python path not set correctly
**Solution**:
```bash
pip install -e .
# or
python -m pip install --no-build-isolation -e .
```

### Issue: MemoryError with large light curves
**Cause**: Limited system RAM
**Solution**: Reduce number of targets in batch analysis

---

## 📈 Customizing the Analysis

### Change Target Stars

In `notebooks/main.ipynb`, cell 2, modify:

```python
target_ids = [
    "TIC 101624823",     # Change these
    "TIC 165052884",     # to any TESS target
    # ... add more
]
```

### Adjust Peak Detection Sensitivity

In `src/roap_analysis/config.py`:

```python
SNR_THRESHOLD = 4.0  # Decrease to detect fainter peaks (might add noise)
                      # Increase to detect only strong peaks only
```

### Change Frequency Range

In `src/roap_analysis/config.py`:

```python
ROAP_FREQ_RANGE_D1 = (0.001, 0.057)  # d⁻¹
ROAP_FREQ_RANGE_UHHZ = (100, 5000)   # µHz
```

### Add Your Own Evolutionary Tracks

Place `.dat` files in `sequences/` following naming convention:
```
ms{mass:04.0f}z019a.dat
# e.g., ms0180z019a.dat for 1.8 M☉
```

---

## 💡 Pro Tips

1. **First run takes longer**: Light curves download and cache
   - Subsequent runs use cached data (much faster!)
   - Cache location: Auto-detected by lightkurve

2. **Save notebook as HTML**: 
   ```bash
   jupyter nbconvert --to html notebooks/main.ipynb --output analysis_report.html
   ```

3. **Export figures for presentations**:
   ```bash
   cp figures/HR_diagram_professional.pdf ~/Documents/congressional_poster.pdf
   ```

4. **Inspect raw data**:
   ```python
   import pandas as pd
   results = pd.read_csv('results/analysis_results.csv')
   display(results.sort_values('DeltaNu_d1'))
   ```

5. **Run subset of analysis** (skip batch processing):
   - Comment out cells 13–15 (batch loop)
   - Focus on first target for testing

---

## 📚 Reading the Scientific Output

### Example Interpretation

**Sample Result**:
- Star: TIC 101624823
- Detected Peaks: 12
- Dominant Frequency: 403 µHz (0.0348 d⁻¹)
- Large Separation: 62 µHz (0.0087 d⁻¹)
- Teff: 8250 K, logg: 4.15 dex

**What this means**:
- **12 oscillation modes** → Rich pulsation spectrum (confirms roAp)
- **403 µHz in roAp range** → Consistent with roAp classification
- **Δν ≈ 62 µHz** → Mean density ≈ 0.8 Msun/Rsun³ (typical A-star)
- **Teff ≈ 8250 K** → Early A-type (Kurtz often reports 7800–10000 K)
- **logg ≈ 4.15** → Main sequence dwarf (log g ranges 3.5–4.5 for dwarfs)

---

## ✅ Success Checklist

After running analysis, you should have:

- [ ] ✓ No errors in notebook cells
- [ ] ✓ `stellar_catalog.csv` with 6 stars
- [ ] ✓ `analysis_results.csv` with seismic parameters
- [ ] ✓ `HR_diagram_professional.pdf` (viewable, shows stars + tracks)
- [ ] ✓ Periodogram PDFs for each analyzed star
- [ ] [ ] Light curve PDFs saved

If all checked: **Analysis successful!** Ready for presentation/publication.

---

## 🎓 Next Steps

### For Congress Poster
1. Download `figures/HR_diagram_professional.pdf`
2. Include in poster template
3. Add caption: "roAp stars from TESS analyzed using state-of-the-art asteroseismology framework"
4. Link: "GitHub: github.com/yourusername/roap-analysis"

### For Scientific Publication
1. Tables: Use `results/analysis_results.csv`
2. Figures: HR diagram + periodograms
3. Methods: Reference `docs/METHODS.md`
4. Data: Cite TESS mission + provide GitHub link

### For Further Analysis
1. Implement mode identification (Δν spacing patterns)
2. Calculate seismic masses/radii (mass scaling relations)
3. Compare with evolutionary models (age dating)
4. Study magnetic field effects (unique to roAp)

---

## 📞 Getting Help

**Problem in notebook?**
- Check error message line number
- Search that function in `src/roap_analysis/`
- Reference `docs/METHODS.md` for scientific questions

**Want to contribute?**
- Read `CONTRIBUTING.md`
- Create feature branch
- Submit pull request

**Citation in paper?**
```bibtex
@software{roap_analysis_2024,
  author = {Jose Angel},
  title = {roAp-Analysis},
  year = {2024},
  url = {https://github.com/yourusername/roap-analysis}
}
```

---

**Ready?** 🚀 Run `jupyter notebook notebooks/main.ipynb` and let's go!

**Estimated time to results**: 10–15 minutes
**Estimated time to congress-ready figures**: +5 minutes (export + caption)
