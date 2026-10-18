# Sesi 03 — Analisis Lokasi Fasilitas Umum Berbasis GIS

**Informatics Practitioner Lecture Series 2026 — Session 3**  
Tema: *Career and Competition in Industrial Era with GIS*

## Gambaran studi kasus

Proyek sederhana ini memperlihatkan bagaimana **data spasial** digunakan untuk membantu analisis lokasi. Program menghitung jarak garis lurus (*Haversine*) dari satu titik acuan ke beberapa fasilitas, mengidentifikasi fasilitas dalam radius tertentu, lalu menampilkan hasil pada **peta web interaktif**.

**Penting:** Nama fasilitas dan seluruh koordinat dalam `data/fasilitas.csv` adalah **data simulasi untuk latihan**, bukan data fasilitas resmi atau hasil survei. Posisi contoh berada di sekitar Kota Bengkulu dan tidak boleh dipakai untuk keputusan operasional.

## Kaitan dengan materi kuliah praktisi

Narasumber membahas pemanfaatan GIS untuk analisis lokasi, pengelolaan aset, dan pengambilan keputusan. Studi kasus ini menerapkan konsep dasar **data spasial + analisis jarak + web map**. Proyek ini **belum menggunakan cloud computing**; peta dibuat secara lokal dan memerlukan internet untuk memuat tile peta dasar dari OpenStreetMap saat dibuka.

## Teknologi

- Python
- pandas untuk membaca dan mengolah data CSV
- folium untuk peta interaktif berbasis Leaflet
- Rumus Haversine untuk jarak permukaan bumi (garis lurus)

## Struktur folder

```text
session-03-gis-location-analysis/
├── data/
│   └── fasilitas.csv
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

Folder `output/` dibuat otomatis setelah program dijalankan.

## Cara menjalankan di VS Code (Windows PowerShell)

Buka terminal pada folder proyek ini, lalu jalankan:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Jika aktivasi PowerShell diblokir, jalankan langsung tanpa aktivasi:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Untuk mengganti titik acuan dan radius:

```powershell
python main.py --lat -3.8004 --lon 102.2655 --radius 5
```

Buka `output/peta_fasilitas.html` menggunakan browser. File `output/hasil_analisis.csv` berisi tabel jarak dan status radius.

## Alur program

1. Baca data koordinat fasilitas dari CSV.
2. Validasi data dan koordinat.
3. Hitung jarak Haversine terhadap titik acuan.
4. Urutkan fasilitas dari yang terdekat.
5. Tentukan apakah tiap fasilitas masuk radius yang ditetapkan.
6. Simpan tabel hasil dan peta interaktif.

## Interpretasi

- **Marker merah**: titik acuan.
- **Marker hijau**: fasilitas di dalam radius.
- **Marker abu-abu**: fasilitas di luar radius.
- **Lingkaran teal**: batas radius analisis.

**Batasan:** Jarak Haversine tidak memperhitungkan jaringan jalan, kemacetan, atau waktu tempuh. Untuk analisis aksesibilitas yang lebih realistis, dapat digunakan data jaringan jalan dan perhitungan rute.

## Ide pengembangan

- Mengganti data simulasi dengan data terbuka yang valid dan menyertakan sumbernya.
- Menambahkan filter kategori fasilitas.
- Menggunakan PostGIS untuk penyimpanan data spasial.
- Membuat aplikasi web dengan backend API dan frontend Vue.
- Menerapkan sinkronisasi cloud untuk pengumpulan data lapangan, seperti contoh dalam kuliah.

## Sumber konsep

Materi sesi ketiga *Informatics Practitioner Lecture Series 2026*, disampaikan oleh Widi Primadeva. Kode merupakan studi kasus latihan mandiri, bukan kode atau dataset dari narasumber.
