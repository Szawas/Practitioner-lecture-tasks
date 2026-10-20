# Session 04 — Machine Learning: Prediksi Kelulusan Mahasiswa

Studi kasus klasifikasi **menggunakan data simulasi**, bukan data mahasiswa sungguhan. Proyek ini dibuat untuk mempraktikkan tahapan machine learning yang dibahas dalam Practitioner Lecture Series sesi 4.

## Materi yang diterapkan
- Dataset dan fitur/label
- Data preprocessing: missing value, scaling, one-hot encoding
- Train/test split (80:20)
- Logistic Regression vs Decision Tree
- Evaluasi: accuracy, precision, recall, F1-score, confusion matrix

## Menjalankan (Windows PowerShell)
```powershell
py -m pip install -r requirements.txt
py main.py
```

## Output
Program membuat folder `output/` berisi:
- `dataset_simulasi.csv`
- `hasil_evaluasi.csv`
- `confusion_matrix_logistic_regression.png`
- `confusion_matrix_decision_tree.png`

## Catatan
Label kelulusan dibangkitkan dengan rumus probabilistik buatan untuk demonstrasi. Hasil evaluasi **tidak dapat digunakan untuk menyimpulkan faktor penentu kelulusan mahasiswa nyata**. Preprocessing dimasukkan ke dalam pipeline sehingga parameter imputasi dan scaling dipelajari hanya dari data latih (menghindari data leakage).
