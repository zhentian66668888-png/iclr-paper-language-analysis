"""Offline checks using synthetic features; no original data, downloads, or NLP corpora."""
from pathlib import Path
import ast
import contextlib
import io
import json
import tempfile

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


def main():
    notebook = json.loads((Path(__file__).parent / 'main.ipynb').read_text(encoding='utf-8'))
    cells = [''.join(c['source']) for c in notebook['cells'] if c['cell_type'] == 'code']
    assert len(cells) == 18, 'All original analysis sections must be retained.'
    for i, source in enumerate(cells):
        compile(source, f'notebook-cell-{i}', 'exec')
    assert all(not c.get('outputs') and c.get('execution_count') is None
               for c in notebook['cells'] if c['cell_type'] == 'code')
    assert 'nltk.download(' not in '\n'.join(cells), 'Notebook execution must not download resources.'

    rng = np.random.default_rng(2026)
    size = 600
    labels = np.array(['poster', 'oral'] * (size // 2))
    frame = pd.DataFrame({
        'abstract': ['graph learning benchmark model'] * size,
        'accept_type': labels,
        'max_h_index': rng.uniform(1, 100, size),
        'avg_citations': rng.uniform(1, 1000, size),
        'author_count': rng.integers(1, 10, size),
        'year': rng.choice([2024, 2025], size),
        'authors': ['synthetic-placeholder'] * size,
        'paper_id': ['synthetic-placeholder'] * size,
    })
    target = pd.Series((labels == 'oral').astype(int))
    expected_train, expected_test = train_test_split(frame.index, test_size=0.25,
                                                    random_state=42, stratify=target)
    frame.loc[expected_test, 'abstract'] += ' heldoutonlytoken'
    frame.loc[expected_test, 'max_h_index'] += 1000

    # Extract the actual notebook loader without triggering file loading or NLP setup.
    tree = ast.parse(cells[1])
    loader_nodes = [node for node in tree.body
                    if isinstance(node, ast.FunctionDef)
                    or (isinstance(node, ast.Assign) and
                        any(isinstance(t, ast.Name) and t.id == 'REQUIRED_COLUMNS' for t in node.targets))]
    env = dict(globals())
    exec(compile(ast.Module(body=loader_nodes, type_ignores=[]), '<notebook-loader>', 'exec'), env)
    with tempfile.TemporaryDirectory(prefix='.validation-', dir=Path(__file__).resolve().parent) as temporary:
        output = Path(temporary)
        csv_path = output / 'synthetic.csv'
        frame.to_csv(csv_path, index=False)
        loaded = env['load_dataset'](csv_path)
        assert list(loaded.columns) == env['REQUIRED_COLUMNS']
        assert 'authors' not in loaded and 'paper_id' not in loaded
        for bad_frame in [frame.drop(columns='year'), frame.assign(accept_type='rejected'),
                          frame.assign(author_count=-1), frame.assign(abstract='')]:
            bad_frame.to_csv(csv_path, index=False)
            try:
                env['load_dataset'](csv_path)
            except ValueError:
                pass
            else:
                raise AssertionError('Invalid data was accepted.')

        # Synthetic linguistic features isolate and exercise the actual model-preparation code.
        for column in ['word_count', 'sent_count', 'pos_score', 'neg_score',
                       'certainty', 'achievement', 'promotional_ratio']:
            loaded[column] = rng.uniform(0.01, 1, size)
        env.update(df=loaded, OUTPUT_DIR=output)
        before = loaded['max_h_index'].copy()
        with contextlib.redirect_stdout(io.StringIO()):
            for index in range(4, 12):
                exec(compile(cells[index], f'notebook-cell-{index}', 'exec'), env)
        assert set(env['train_idx']).isdisjoint(env['test_idx'])
        assert set(env['train_idx']) | set(env['test_idx']) == set(loaded.index)
        assert 'heldoutonlytoken' not in env['tfidf'].vocabulary_
        np.testing.assert_allclose(env['scaler'].mean_,
                                   loaded.loc[env['train_idx'], env['feature_cols']].mean())
        assert env['scaler'].mean_[env['feature_cols'].index('max_h_index')] < 100
        np.testing.assert_allclose(env['X_train_core'].mean(), 0, atol=1e-12)
        pd.testing.assert_series_equal(loaded['max_h_index'], before)
        assert len(env['tfidf_cols']) < 150, 'A small vocabulary must work without a hard-coded width.'
        assert env['X_train_full'].index.equals(env['y_train'].index)
        assert env['X_test_full'].index.equals(env['y_test'].index)
        assert env['model_table']['Test_AUC'].between(0, 1).all()
        assert env['model_table']['Test_Accuracy'].between(0, 1).all()
        assert len(env['matching_table']) == 3
        for name in ['regression_results.csv', 'matching_results.csv',
                     'model_comparison.csv', 'yearly_associations.csv', 'model_comparison.png']:
            assert (output / name).is_file(), name
        plt.close('all')
    print('PASS: 18 code cells compile; clean notebook; strict data allowlist and invalid-input checks.')
    print('PASS: disjoint holdout; training-only vocabulary/scaler; dynamic vocabulary size; aligned labels.')
    print('PASS: synthetic logistic/random-forest fitting, covariate matching, yearly analysis, and aggregate exports.')
    print('Not exercised here: real-data findings, VADER/tokenization, WordCloud, or the remaining plots.')


if __name__ == '__main__':
    main()
