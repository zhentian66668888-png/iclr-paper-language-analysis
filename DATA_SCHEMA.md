# Input data contract

The analysis expects a UTF-8 CSV. By default its relative path is `data/iclr_cleaned_v1_20250322.csv`; `ICLR_DATA_PATH` can select another local path. Raw data is intentionally not included in this repository.

## Required fields

| Column | Meaning | Accepted values |
| --- | --- | --- |
| `abstract` | English paper abstract | Nonmissing, nonempty text |
| `accept_type` | Presentation type of an accepted paper | `poster`, `oral`, or `spotlight`; case/outer whitespace normalized |
| `max_h_index` | Maximum author H-index recorded for the paper | Finite, nonnegative numeric value |
| `avg_citations` | Average author citation measure recorded for the paper | Finite, nonnegative numeric value |
| `author_count` | Number of authors | Positive integer |
| `year` | Conference year | Nonnegative integer |

Both binary presentation groups require at least four observations for the stratified holdout. A usable vocabulary must occur in at least two training abstracts; logistic fitting and matching also need sufficiently varied, nonsingular features and nonempty promotional-ratio groups. The loader rejects missing fields, unsupported presentation labels, and invalid numeric values rather than silently imputing them.

Additional columns are excluded by the loader. In particular, names, paper titles, paper/forum IDs, and individual author records are neither needed nor exported. The analysis does not perform author name resolution or construct bibliometric metrics from raw author data.

## Derived variables

- `is_high_level`: legacy internal variable name for Oral/Spotlight (1) versus Poster (0), among accepted papers.
- `promotional_ratio`: number of whitespace-separated tokens matching the specified promotional vocabulary, divided by whitespace token count.
- `word_count` / `sent_count`: NLTK token and sentence counts.
- `pos_score` / `neg_score`: VADER positive/negative proportions.
- `certainty` / `achievement`: case-insensitive counts from small handcrafted lists.
- `tfidf_*`: training-vocabulary TF-IDF features, capped at 150 terms with `min_df=2` and English stop words.

## Provenance and scope

The original project used a precleaned local file with this schema. A verified upstream collection URL, bibliometric measurement date, and dataset license were not documented in the supplied project materials; this repository therefore does not redistribute the dataset or provide an unverified download link.

The available local copy contains 5,963 accepted-paper rows from 2024 and 2025: 4,917 Poster, 747 Spotlight, and 299 Oral. These are aggregate descriptions of the local reproduction input, not a claim that this file is a complete conference archive. A new dataset with the same schema may produce different results. Obtain data through a source you can access and document its provenance before interpreting a rerun.
