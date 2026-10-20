# Session 06 — Forest Disturbance Classification

**Praktikum:** Informatics Practitioner Lecture Series, Sesi 6  
**Materi:** *Attributing Direct Drivers to Deforestation Alerts with Satellite Imagery and AI*  
**Narasumber:** Dr. Bart Slachter, Wageningen University & Research

## Tujuan

Mensimulasikan klasifikasi penyebab langsung gangguan hutan dengan Machine Learning dan mengevaluasi hasil klasifikasinya. Proyek ini terinspirasi dari pemaparan tentang *deforestation alerts*, penggabungan Sentinel-1/Sentinel-2, klasifikasi penyebab gangguan, dan pentingnya evaluasi model.

> **Batasan penting:** Data pada proyek ini 100% **sintetis**, bukan data satelit Sentinel atau hasil observasi lapangan. Model menggunakan **Random Forest** dan **Decision Tree**, bukan CNN seperti pada penelitian narasumber. Kategori, nilai fitur, dan hasil evaluasi hanya untuk latihan teknis. Jangan gunakan hasilnya sebagai bukti deforestasi nyata atau sebagai dasar keputusan lingkungan.

## Fitur

- Membuat 700 sampel sintetis secara otomatis (140 sampel per kelas).
- Lima kategori: **Pertanian, Pertambangan, Penebangan, Kebakaran, Banjir**.
- Enam fitur ilustratif: luas gangguan (ha), indeks vegetasi, indikasi panas, jarak ke jalan (km), kelembapan, dan perubahan sinyal radar.
- Membandingkan **Decision Tree** dan **Random Forest** memakai **accuracy** dan **macro F1-score**.
- Menghasilkan **confusion matrix**, **feature importance**, tabel prediksi, dan CSV perbandingan model.

## Persiapan

Pastikan Python 3.10+ tersedia. Buka terminal pada folder proyek.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src/main.py
```

Jika aktivasi PowerShell dibatasi, jalankan tanpa aktivasi:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/main.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/main.py
```

## Output

Program otomatis membuat folder `outputs/` berisi:

| File | Isi |
|---|---|
| `data_simulasi.csv` | Dataset sintetis beserta label penyebab |
| `perbandingan_model.csv` | Accuracy dan macro F1 masing-masing model |
| `hasil_prediksi.csv` | Label aktual, prediksi, dan benar/salah |
| `confusion_matrix.png` | Visualisasi prediksi Random Forest |
| `feature_importance.png` | Ilustrasi kontribusi fitur pada Random Forest |

## Kaitan dengan materi

Dalam penelitian yang dipaparkan narasumber, citra satelit digunakan untuk mengidentifikasi *direct drivers* gangguan hutan dengan CNN. Studi kasus ini menyederhanakan proses tersebut menjadi klasifikasi data tabular sintetis. Tujuannya memahami alur **data → pelatihan model → prediksi → evaluasi**, termasuk mengapa *macro F1-score* penting untuk menilai kinerja setiap kelas.

## Struktur

```text
session-06-deforestation-ai/
├── src/
│   └── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── outputs/              # dibuat otomatis ketika program dijalankan
```

## Dokumentasi tugas

Ambil tangkapan layar terminal hasil perbandingan model dan gambar `outputs/confusion_matrix.png` setelah program dijalankan. Sertakan penjelasan bahwa hasil berasal dari data simulasi.
