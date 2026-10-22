# Publication preparation

## 2026-10-22

- Kept the complete 18-section analysis notebook as `main.ipynb`. The two equivalent full versions were consolidated; the shorter earlier draft was not included as a second main workflow.
- Removed historical outputs, execution counts, and cell metadata; replaced notebook metadata with a minimal generic Python kernel description. No raw CSV, author names, titles, identifiers, or local machine paths are distributed.
- Added an allowlisted CSV loader, explicit data validation, a relative default data path, and optional `ICLR_DATA_PATH` configuration.
- Moved TF-IDF fitting and numeric scaling after the shared train/test split, fitting both on training rows only. Preserved raw feature units in the exploratory dataframe. Fixed the TF-IDF dataframe width to follow the learned vocabulary rather than assuming exactly 150 terms.
- Made handcrafted dictionary counts case-insensitive and described them accurately instead of presenting them as official LIWC features.
- Replaced automatic NLTK downloads with explicit setup instructions and missing-resource checks. Removed global warning suppression.
- Corrected the outcome description to Oral/Spotlight versus Poster among accepted papers, rather than acceptance versus rejection.
- Renamed the former PSM/ATT section as nearest-neighbor covariate matching and a descriptive rate contrast. Preserved nearest-neighbor matching with replacement and standardized covariates separately for that descriptive analysis. No propensity-score or causal-effect claim remains.
- Retained groupwise trend plots while replacing unsupported significance/moderation conclusions with descriptive slope differences. Corrected year-by-year interpretation and made failed fits visible.
- Separated held-out AUC/accuracy and training pseudo-R-squared into distinct columns; added an always-Poster baseline and explained that the models use different feature sets.
- Added data documentation, requirements, ignores for local data/results/credentials, an offline synthetic validation script, and aggregate-only report exports. No model performance was copied from an old notebook output.
