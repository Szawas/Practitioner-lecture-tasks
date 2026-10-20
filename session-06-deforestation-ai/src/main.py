"""Educational simulation of forest-disturbance driver classification.

All samples are synthetic, NOT satellite observations or field-validated alerts.
"""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, ConfusionMatrixDisplay

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'
FEATURES = ['luas_ha', 'indeks_vegetasi', 'indikasi_panas', 'jarak_jalan_km', 'kelembapan', 'perubahan_radar']
CLASSES = ['Pertanian', 'Pertambangan', 'Penebangan', 'Kebakaran', 'Banjir']


def generate_dataset(n_per_class=140, seed=42):
    """Create distinct but overlapping synthetic feature profiles for 5 classes."""
    rng = np.random.default_rng(seed)
    profiles = {
        'Pertanian':    ([9.0, .38, .16, 2.0, .43, .57], [6.0, .12, .13, 1.5, .14, .16]),
        'Pertambangan': ([5.5, .15, .25, 3.5, .29, .77], [3.5, .10, .15, 2.0, .13, .13]),
        'Penebangan':   ([2.5, .56, .12, 1.0, .57, .40], [1.5, .13, .10, 1.0, .15, .15]),
        'Kebakaran':   ([12., .20, .85, 4.5, .18, .67], [7.0, .12, .12, 2.5, .10, .17]),
        'Banjir':      ([8.0, .43, .10, 5.0, .91, .72], [5.0, .14, .10, 3.0, .08, .16]),
    }
    rows = []
    for label, (means, stds) in profiles.items():
        values = rng.normal(means, stds, size=(n_per_class, len(FEATURES)))
        values[:, 0] = np.clip(values[:, 0], .1, None)
        values[:, 3] = np.clip(values[:, 3], 0, None)
        values[:, [1, 2, 4, 5]] = np.clip(values[:, [1, 2, 4, 5]], 0, 1)
        for vector in values:
            rows.append(dict(zip(FEATURES, np.round(vector, 3)), penyebab=label))
    df = pd.DataFrame(rows).sample(frac=1, random_state=seed).reset_index(drop=True)
    df.insert(0, 'id_alert', [f'ALT-{i:04d}' for i in range(1, len(df)+1)])
    return df


def main():
    parser = argparse.ArgumentParser(description='Simulasi klasifikasi penyebab gangguan hutan')
    parser.add_argument('--samples-per-class', type=int, default=140)
    args = parser.parse_args()
    if args.samples_per_class < 10:
        parser.error('--samples-per-class minimal 10')
    OUT.mkdir(exist_ok=True)
    df = generate_dataset(args.samples_per_class)
    df.to_csv(OUT / 'data_simulasi.csv', index=False)
    X_train, X_test, y_train, y_test = train_test_split(
        df[FEATURES], df['penyebab'], test_size=.25, stratify=df['penyebab'], random_state=42
    )
    models = {
        'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=120, max_depth=8, random_state=42, n_jobs=-1),
    }
    metrics = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        metrics.append({'model': name, 'accuracy': accuracy_score(y_test, pred),
                        'macro_f1': f1_score(y_test, pred, average='macro')})
        if name == 'Random Forest':
            print('\nLAPORAN KLASIFIKASI RANDOM FOREST\n')
            print(classification_report(y_test, pred, labels=CLASSES, zero_division=0))
            fig, ax = plt.subplots(figsize=(8, 6))
            ConfusionMatrixDisplay.from_predictions(y_test, pred, labels=CLASSES,
                                                     xticks_rotation=35, cmap='Blues', ax=ax)
            ax.set_title('Confusion Matrix - Random Forest (Data Simulasi)')
            fig.tight_layout()
            fig.savefig(OUT / 'confusion_matrix.png', dpi=160)
            plt.close(fig)
            fig, ax = plt.subplots(figsize=(8, 4.5))
            pd.Series(model.feature_importances_, index=FEATURES).sort_values().plot.barh(ax=ax)
            ax.set_title('Feature Importance - Random Forest')
            ax.set_xlabel('Importance')
            fig.tight_layout()
            fig.savefig(OUT / 'feature_importance.png', dpi=160)
            plt.close(fig)
            results = X_test.copy()
            results.insert(0, 'aktual', y_test.to_numpy())
            results.insert(1, 'prediksi', pred)
            results['benar'] = results['aktual'] == results['prediksi']
            results.to_csv(OUT / 'hasil_prediksi.csv', index=False)
    summary = pd.DataFrame(metrics)
    summary.to_csv(OUT / 'perbandingan_model.csv', index=False)
    print('\nPERBANDINGAN MODEL (DATA SIMULASI)\n')
    print(summary.to_string(index=False, float_format=lambda x: f'{x:.3f}'))
    print(f'\nFile hasil tersimpan di: {OUT}')


if __name__ == '__main__':
    main()
