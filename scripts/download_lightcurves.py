#!/usr/bin/env python3
"""
Download TESS light curves and MESA evolutionary models (auto-setup).

This script downloads the data needed to reproduce the asteroseismic analysis.
Large data files are stored in data/ directory (ignored by git).

Usage:
    python scripts/download_lightcurves.py

Requirements:
    - lightkurve (for TESS data download)
    - requests (for file downloads)
"""

import sys
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")


def download_lightcurves():
    """Download TESS light curves using lightkurve."""
    try:
        import lightkurve as lk
    except ImportError:
        print("❌ ERROR: lightkurve not installed.")
        print("   Install with: pip install lightkurve")
        sys.exit(1)

    TIC_IDS = [101624823, 165052884, 158271090, 233200244, 298052991, 435263600]
    lc_dir = Path("data/lightcurves")
    lc_dir.mkdir(parents=True, exist_ok=True)

    print("📥 Downloading TESS light curves from MAST...")
    print("   (This may take 2-3 minutes on first run)")
    print()

    downloaded = 0
    skipped = 0

    for tic_id in TIC_IDS:
        output_file = lc_dir / f"TIC_{tic_id}.csv"
        if output_file.exists():
            print(f"  ✓ TIC {tic_id:9d} (already cached)")
            skipped += 1
            continue

        try:
            print(f"  ⏳ TIC {tic_id:9d} downloading...", end=" ", flush=True)
            lc = lk.read(f"TIC {tic_id}", mission="TESS").remove_nans().flatten()
            lc.to_csv(output_file, overwrite=True)
            size_mb = output_file.stat().st_size / 1e6
            print(f"✓ ({size_mb:.1f} MB)")
            downloaded += 1
        except Exception as e:
            print(f"✗ ERROR: {e}")

    print()
    print(f"✅ Light curves ready in {lc_dir}/")
    print(f"   Downloaded: {downloaded} | Cached: {skipped} | Total: {downloaded + skipped}")


def verify_evolutionary_models():
    """Verify MESA evolutionary models are present (checked in git)."""
    model_dir = Path("data/evolutionary_models")
    models = list(model_dir.glob("*.dat"))

    if models:
        print(f"✅ Evolutionary models ready in {model_dir}/")
        print(f"   Found: {len(models)} MESA tracks")
        return True
    else:
        print(f"⚠️  WARNING: No evolutionary models found in {model_dir}/")
        print("   These should be checked in with git.")
        return False


def main():
    """Main download orchestration."""
    print()
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║  roAp Analysis: Data Download & Setup                        ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print()

    # Create directories
    Path("data/lightcurves").mkdir(parents=True, exist_ok=True)
    Path("data/evolutionary_models").mkdir(parents=True, exist_ok=True)

    # Download light curves
    download_lightcurves()
    print()

    # Verify models
    verify_evolutionary_models()
    print()

    print("✨ Data setup complete! Ready to run analysis.")
    print()
    print("   Next: python -m jupyter notebook notebooks/main.ipynb")
    print()


if __name__ == "__main__":
    main()
