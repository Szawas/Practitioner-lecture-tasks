# Analisis Penjualan dan Prediksi Keterlambatan Pembayaran

Studi kasus edukasi yang terinspirasi dari materi **Make Sense of Data with Analytics and AI** pada Informatics Practitioner Lecture Series. Studi kasus ini **bukan** data atau implementasi asli PT Maju Bersama.

## Tujuan
- Mempraktikkan data understanding, data preparation, analisis deskriptif, dan pemodelan sederhana.
- Melihat tren pendapatan dan estimasi laba kotor pada data sintetis.
- Memprediksi apakah sebuah faktur akan dibayar **lebih dari 30 hari setelah tanggal jatuh tempo**.
- Memahami mengapa recall dan confusion matrix penting pada data dengan kelas tidak seimbang.

## Cara menjalankan
```bash
pip install -r requirements.txt
python main.py
```

Program membuat `transaksi_simulasi.csv` serta folder `output/` berisi:
- `ringkasan_bulanan.csv`
- `tren_bulanan.png`
- `evaluasi_model.txt`
- `confusion_matrix.png`

## Tahapan
1. **Business understanding:** memahami pola transaksi dan risiko pembayaran terlambat.
2. **Data understanding:** memeriksa struktur dan missing value.
3. **Data preparation:** menghapus duplikasi ID, menyiapkan variabel laba dan bulan.
4. **Modeling:** Logistic Regression dengan pembagian data latih/uji terstratifikasi.
5. **Evaluation:** precision, recall, F1-score, dan confusion matrix.
6. **Communication:** menyimpan ringkasan dan visualisasi sebagai bahan interpretasi.

## Catatan penting
- Semua transaksi **dibuat secara sintetis** dengan bilangan acak yang dapat direproduksi (`seed=42`). Tidak mewakili kinerja perusahaan nyata.
- `estimated_cost` digunakan menghitung **estimasi laba kotor**, bukan laba bersih; tidak ada biaya operasional, pajak, atau arus kas.
- Label `late_over_30_days` adalah hasil simulasi. `days_after_due_paid` hanya dicatat untuk ilustrasi hasil pembayaran, **tidak** dipakai sebagai fitur prediksi karena baru diketahui setelah pembayaran (data leakage).
- Model menggunakan fitur yang diasumsikan tersedia ketika faktur diterbitkan: nominal faktur, tenor, segmen pelanggan, dan jumlah keterlambatan historis.
- Dataset simulasi dan pemisahan acak hanya untuk latihan. Untuk penelitian nyata, validasi berdasarkan waktu dan pengelompokan pelanggan dapat lebih sesuai.
- Kinerja model tidak boleh ditafsirkan sebagai akurasi di dunia nyata.

## Keterkaitan dengan materi
Proyek ini menunjukkan proses **data → information → insight → decision**, prinsip **garbage in, garbage out**, CRISP-DM, serta pentingnya evaluasi lebih dari sekadar accuracy.
