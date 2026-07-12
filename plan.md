# Plan de rescate — roAp (pulido, NO reconstrucción)

> **Diagnóstico central:** este repo tiene el problema OPUESTO al de MCMC.
> No falta estructura — **sobra andamiaje y sobra inflado**. La regla aquí es
> **restar, no sumar.**
>
> **Reencuadre de identidad:** hacia física estadística → *análisis espectral y
> de series de tiempo de señales estocásticas*. La asterosismología es el caso
> de aplicación. El titular académico (si aplica) es científico, no de marketing.

## Lo que YA está bien (no tocar)
- Paquete real `src/roap_analysis/` (config, frequency_analysis, stellar_params, plotting — ~630 líneas).
- Métodos sólidos: Lomb-Scargle vía lightkurve, estimación de ruido con MAD (robusta), SNR.
- Datos reales: 6 estrellas TIC con curvas de luz TESS + trazas evolutivas + cross-match Gaia DR3.

## Los problemas (por orden de gravedad)

| Problema | Gravedad | Acción |
|----------|----------|--------|
| **110 MB de `csv/` curvas de luz en git** | Alto (límites GitHub, repo pesado) | Purgar del historial; `.gitignore`; script de descarga o release/Zenodo |
| **`calculate_large_separation` es ingenuo** — promedia diferencias de picos vecinos; NO es así como se calcula Δν (se usa autocorrelación / échelle) | **Científico real** | Corregir (autocorrelación) o etiquetar honestamente como estimación cruda |
| **`identify_mode_spectrum` es un stub** — mete todos los picos en `l=0`, presentado como "advanced feature" | Inflado / deshonesto | Implementar de verdad (échelle) o borrar y no prometerlo |
| **Notebooks duplicados**: `main/main.ipynb`, `notebooks/main.ipynb`, `notebooks/01_main_analysis.py`, `main/Borrador_Ensenada_2024.ipynb`, `figures/Ensenada_2024.ipynb` | Medio (caos, señal de desorden) | Dejar UNO canónico narrado; borrar borradores |
| **Bloat de docs**: REFACTORING_SUMMARY.md, QUICKSTART.md, CONTRIBUTING.md, docs/METHODS.md para un repo de 1 autor | Medio | Consolidar en README + docs/METHODS.md; borrar el resto |
| **README inflado**: emojis a mansalva, badges "300 dpi / Production Ready", `yourusername` sin reemplazar, promete 12 modos/figuras | Alto (mata credibilidad con pares) | Reescribir sobrio |

## Fases (esfuerzo BAJO — es pulido)
- **Fase 1 — Desinflar (bajo):** reescribir README en tono sobrio (fuera badges falsos, arreglar `yourusername`), una figura killer arriba (diagrama HR real o échelle), tabla de las 6 estrellas con parámetros.
- **Fase 2 — De-duplicar (bajo):** un solo notebook canónico narrado (demostración del pipeline), borrar borradores y notebooks redundantes; consolidar docs.
- **Fase 3 — Honestidad científica (bajo-medio):** corregir o etiquetar `calculate_large_separation` (Δν por autocorrelación); implementar de verdad `identify_mode_spectrum` (diagrama échelle) o eliminarlo. No prometer lo que no hace.
- **Fase 4 — Peso del repo (bajo):** sacar los 110 MB de `csv/` del historial git; `.gitignore`; añadir `scripts/download_lightcurves.py` (lightkurve) o enlazar datos en release/Zenodo.
- **Fase 5 (opcional, alto valor académico):** verificar si alguna de las 6 estrellas TIC **no ha sido publicada con TESS**. Si es así → ese es el titular real y el repo pasa de "demo" a "contribución".

## Criterio de "hecho"
Repo honesto y limpio que a un par académico le dice "análisis espectral riguroso de series de tiempo TESS" y no levanta banderas rojas de inflado. Estructura ya está; el valor es la sobriedad + corrección científica.
