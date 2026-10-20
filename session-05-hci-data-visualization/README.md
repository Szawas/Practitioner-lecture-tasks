# Sales Insight Dashboard

**Tugas 3 — Practitioner Lecture Series, Sesi 5**  
**Materi:** Human-Computer Interaction & Data Visualization  
**Narasumber:** Arafat Febrian Dirza (BRIN)

Dashboard penjualan interaktif yang menerapkan prinsip *User-Centered Design*, konsistensi antarmuka, *visibility*, *feedback*, dan visualisasi data yang sesuai konteks. Dibuat menggunakan Vue 3, Tailwind CSS, dan Chart.js.

## Fitur
- Statistik total penjualan, transaksi, unit terjual, dan produk terlaris.
- Grafik garis tren penjualan bulanan dan grafik batang perbandingan kategori.
- Filter bulan, kategori, serta pencarian ID/nama produk.
- Tabel transaksi yang mengikuti filter, pesan saat hasil kosong, dan reset filter.
- Ekspor transaksi hasil filter ke CSV.
- Tampilan responsif dan label input yang jelas.

## Menjalankan aplikasi

Persyaratan: **Node.js 20.19+ atau 22.12+** dan npm.

```powershell
npm install
npm run dev
```

Buka alamat lokal yang muncul di terminal (biasanya `http://localhost:5173`). Untuk build produksi:

```powershell
npm run build
npm run preview
```

## Struktur proyek

```text
session-05-hci-data-visualization/
├── src/
│   ├── components/SalesChart.vue
│   ├── data/transactions.js
│   ├── utils/format.js
│   ├── App.vue
│   ├── main.js
│   └── style.css
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## Hubungan dengan materi

| Prinsip HCI / Visualisasi | Implementasi |
|---|---|
| User-Centered Design | Alur sederhana untuk pengguna yang ingin memantau transaksi |
| Visibility | KPI dan filter ditampilkan di bagian atas |
| Feedback | Jumlah hasil, KPI, grafik, dan tabel diperbarui saat filter berubah |
| Consistency | Warna, tata letak, dan komponen konsisten |
| Overview first, details on demand | KPI dan grafik dahulu, lalu detail transaksi |
| Pemilihan grafik | Line chart untuk tren waktu; bar chart untuk perbandingan kategori |
| Error prevention | Filter menggunakan pilihan yang valid; hasil kosong memiliki pesan jelas |

## Dataset dan batasan

Data pada `src/data/transactions.js` adalah **120 transaksi simulasi deterministik** selama Januari–Juni 2026. Data tidak mewakili transaksi toko sungguhan. Proyek ini adalah demonstrasi penerapan HCI dan visualisasi, **bukan penelitian usability formal**. Untuk mengukur usability secara ilmiah, perlu pengujian pengguna dengan tugas dan metrik yang ditentukan.

## Mengunggah ke GitHub

Letakkan folder ini di dalam repositori `Practitioner-lecture-tasks`, sejajar dengan folder sesi sebelumnya. Jangan unggah `node_modules` atau `dist` (sudah diabaikan oleh `.gitignore`).
