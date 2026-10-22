# Aggregate results

Generated from the documented local run of main.ipynb; see ../VALIDATION.md for the data scope and environment.

- model_comparison.csv / .png: one row per model configuration or constant-class baseline; held-out AUC/accuracy and training pseudo-R-squared kept separate.
- regression_results.csv: numeric-feature logistic regression summary. Coefficients are in training-standardized units; rounded p-values and significance symbols are exploratory.
- matching_results.csv: above-median group, matched comparison group, and descriptive rate contrast. No propensity scores or causal effects are estimated.
- yearly_associations.csv: one aggregate regression summary per year, in raw numeric-feature units.
- feature_distributions.png: aggregated histograms/densities, displaying values at or below the 99th percentile for each feature.
- correlation_matrix.png: full-sample correlations between the binary presentation label, language features, and author metrics.

These files contain no raw paper rows, names, titles, IDs, abstract text, individual predictions, or individual scatter points. Feature distributions and correlations are descriptive; they are not held-out model evaluations. Word clouds and pairwise/groupwise scatter plots remain in the clean notebook as code, but their rendered images are not distributed.
