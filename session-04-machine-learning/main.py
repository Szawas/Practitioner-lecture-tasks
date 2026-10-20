from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'output'
OUTPUT.mkdir(exist_ok=True)
RNG = np.random.default_rng(42)

# Dataset SIMULASI: label dibangkitkan dari aturan probabilistik, bukan data mahasiswa nyata.
n = 500
jam_belajar = RNG.uniform(0, 20, n)
kehadiran = RNG.uniform(45, 100, n)
nilai_tugas = RNG.uniform(35, 100, n)
akses_internet = RNG.choice(['Ada', 'Terbatas'], n, p=[0.7, 0.3])
skor = (-8 + 0.16 * jam_belajar + 0.055 * kehadiran
        + 0.045 * nilai_tugas + 0.3 * (akses_internet == 'Ada'))
probabilitas = 1 / (1 + np.exp(-skor))
lulus = RNG.binomial(1, probabilitas)
df = pd.DataFrame({
    'jam_belajar': jam_belajar.round(1),
    'kehadiran_persen': kehadiran.round(1),
    'nilai_tugas': nilai_tugas.round(1),
    'akses_internet': akses_internet,
    'lulus': lulus,
})
# Simulasikan sebagian data yang kosong agar preprocessing terlihat.
for kolom in ['jam_belajar', 'nilai_tugas']:
    idx = RNG.choice(n, size=12, replace=False)
    df.loc[idx, kolom] = np.nan

df.to_csv(OUTPUT / 'dataset_simulasi.csv', index=False)
X = df.drop(columns='lulus')
y = df['lulus']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

numerik = ['jam_belajar', 'kehadiran_persen', 'nilai_tugas']
kategori = ['akses_internet']
preprocessor = ColumnTransformer([
    ('numerik', Pipeline([
        ('isi_kosong', SimpleImputer(strategy='median')),
        ('skala', StandardScaler()),
    ]), numerik),
    ('kategori', Pipeline([
        ('isi_kosong', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore')),
    ]), kategori),
])

model = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(max_depth=4, random_state=42),
}
hasil = []
for nama, algoritma in model.items():
    pipeline = Pipeline([('preprocessing', preprocessor), ('model', algoritma)])
    pipeline.fit(X_train, y_train)
    prediksi = pipeline.predict(X_test)
    hasil.append({
        'model': nama,
        'accuracy': accuracy_score(y_test, prediksi),
        'precision': precision_score(y_test, prediksi, zero_division=0),
        'recall': recall_score(y_test, prediksi, zero_division=0),
        'f1_score': f1_score(y_test, prediksi, zero_division=0),
    })
    ConfusionMatrixDisplay.from_predictions(y_test, prediksi, display_labels=['Tidak Lulus', 'Lulus'], cmap='Blues')
    plt.title(f'Confusion Matrix - {nama}')
    plt.tight_layout()
    plt.savefig(OUTPUT / f'confusion_matrix_{nama.lower().replace(" ", "_")}.png', dpi=150)
    plt.close()

hasil_df = pd.DataFrame(hasil)
hasil_df.to_csv(OUTPUT / 'hasil_evaluasi.csv', index=False)
print('\nPERBANDINGAN MODEL (DATA SIMULASI)')
print(hasil_df.to_string(index=False, float_format=lambda v: f'{v:.3f}'))
print('\nFile tersimpan di:', OUTPUT)
