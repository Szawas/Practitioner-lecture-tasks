# Session 02 — High Performance Computing

**Lecture:** Bridging Global Infrastructure to Address Local Challenges in High Performance Computing  
**Speaker:** Dr. Warawan, Thammasat University, Thailand

## Studi kasus
**Perbandingan Komputasi Sekuensial dan Paralel untuk Estimasi Pi Menggunakan Monte Carlo**

Materi membahas simulasi numerik, penggunaan banyak prosesor, dan evaluasi kinerja pada HPC. Proyek ini mengilustrasikan **paralelisme CPU lokal**, bukan menggunakan superkomputer. Metode Monte Carlo dipilih sebagai contoh tambahan untuk mempraktikkan konsep tersebut; bukan demonstrasi khusus yang ditunjukkan pemateri.

Program membangkitkan titik acak di persegi satuan dan menghitung proporsi titik di dalam seperempat lingkaran: `pi ≈ 4 × (jumlah titik di dalam / total titik)`. Metode sekuensial dan paralel menjalankan **chunk data acak identik** sehingga hasil estimasi sama. Paralelisme menggunakan `concurrent.futures.ProcessPoolExecutor`.

## Menjalankan di VS Code / PowerShell

Pastikan Python tersedia (`python --version`). Tidak ada dependensi tambahan.

```powershell
python main.py
```

Eksperimen lain:

```powershell
python main.py --samples 4000000 --workers 4 --chunks 16
```

Output berupa ringkasan terminal dan `output/hasil_benchmark.csv`.

## Analisis

- **Waktu sekuensial**: total waktu komputasi satu proses.
- **Waktu paralel**: total waktu komputasi beberapa proses, termasuk overhead.
- **Speedup**: waktu sekuensial dibagi waktu paralel.
- **Efisiensi worker**: speedup dibagi jumlah worker, dikali 100%.
- **Galat absolut**: selisih estimasi pi dengan `math.pi`.

Ulangi percobaan beberapa kali, dan bandingkan jumlah worker/sampel. Paralelisme **tidak selalu lebih cepat**, terutama untuk tugas kecil atau pada komputer dengan keterbatasan inti CPU. Hasil dipengaruhi beban komputer, OS, dan overhead proses. Proyek ini bukan pengukuran FLOPS atau HPC terdistribusi.
