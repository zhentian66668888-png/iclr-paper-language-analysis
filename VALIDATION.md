# Validation record

Verified locally on 2026-10-22 with Python 3.12.14. No external model API was used. This record separates synthetic code checks from execution on the private local dataset.

## Offline synthetic check

Command: `python validate.py` after installing dependencies.

Passed:

- All 18 code cells compile and the notebook has no historical outputs or execution counts.
- The CSV loader selects exactly six permitted analysis fields and excludes extra name/identifier columns.
- Missing columns, unsupported presentation labels, negative author counts, and empty abstracts are rejected.
- Train/test indices are disjoint and cover the sample; feature/label indices remain aligned.
- A test-only token cannot enter the fitted TF-IDF vocabulary. Scaler means equal training-row means even when held-out rows are shifted substantially.
- Vocabularies smaller than 150 terms work. Exploratory raw feature units remain unchanged.
- Actual notebook code fits logistic regression and random forest, performs descriptive nearest-neighbor matching and yearly fits, and creates expected aggregate export files using synthetic features.

The synthetic check does not exercise VADER/tokenization, WordCloud, all plots, or validate substantive findings.

## Full local-data execution

All 18 code cells executed sequentially in a fresh Python process using a noninteractive Matplotlib backend. This included NLTK tokenization/VADER, WordCloud, and the remaining exploratory plots. Historical outputs remain cleared in the distributed notebook.

Input: 5,963 accepted-paper rows, years 2024 and 2025; 4,917 Poster, 747 Spotlight, 299 Oral. One stratified split (seed 42) produced 4,472 training and 1,491 test rows; the fitted TF-IDF vocabulary contained 150 terms. Both year-specific fits completed.

| Configuration | Held-out ROC AUC | Held-out accuracy |
| --- | ---: | ---: |
| Logistic regression, numeric core | 0.5305 | 0.8236 |
| Random forest, numeric core + TF-IDF | 0.5327 | 0.8236 |
| Always predict Poster | 0.5000 | 0.8243 |

The two learned configurations show weak discrimination in this split and do not improve accuracy over the constant baseline. This is not a future-year evaluation, a causal result, or a general performance guarantee. Synthetic metrics are not used as research results.

The curated `reports/` exports include only model-level metrics, regression summaries, three matched-group summary rows, two year-level summary rows, histograms/densities, and a correlation matrix. No raw dataset, individual predictions, author names, titles, identifiers, text excerpts, word-cloud image, or scatter-plot image is distributed.

## Verified package versions

| Package | Version |
| --- | --- |
| numpy | 2.5.4 |
| pandas | 3.0.6 |
| scipy | 1.18.1 |
| scikit-learn | 1.9.1 |
| statsmodels | 0.15.0 |
| matplotlib | 3.11.2 |
| seaborn | 0.13.2 |
| nltk | 3.10.4 |
| wordcloud | 1.9.6 |

The repository provides compatible version ranges rather than an exact environment lock. NLTK `punkt_tab` and `vader_lexicon` were obtained separately from official NLTK resources and are not redistributed. The local dataset is not redistributed; a reader needs their own compatible data to repeat the full analysis. Upstream data provenance and metric collection timing remain undocumented, as described in DATA_SCHEMA.md.
