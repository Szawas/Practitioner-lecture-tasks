"""Studi kasus GIS: analisis jarak fasilitas dan peta interaktif.

Semua koordinat pada data/fasilitas.csv adalah DATA SIMULASI, bukan data lokasi resmi.
"""
import argparse
import math
from pathlib import Path

import folium
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "fasilitas.csv"
OUTPUT = ROOT / "output"


def haversine_km(lat1, lon1, lat2, lon2):
    """Jarak garis lurus antara dua koordinat bumi, dalam kilometer."""
    radius = 6371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    return 2 * radius * math.asin(min(1, math.sqrt(a)))


def analyze(latitude, longitude, radius_km):
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        raise ValueError("Koordinat titik acuan tidak valid.")
    if radius_km <= 0:
        raise ValueError("Radius harus lebih besar dari nol.")

    df = pd.read_csv(DATA)
    required = {"id", "nama", "kategori", "latitude", "longitude"}
    if not required.issubset(df.columns):
        raise ValueError(f"Kolom CSV wajib: {', '.join(sorted(required))}")
    if df.empty or df[["latitude", "longitude"]].isnull().any().any():
        raise ValueError("Data fasilitas kosong atau koordinat tidak lengkap.")
    if not df["latitude"].between(-90, 90).all() or not df["longitude"].between(-180, 180).all():
        raise ValueError("Ada koordinat fasilitas yang tidak valid.")

    df["jarak_km"] = df.apply(
        lambda r: haversine_km(latitude, longitude, r["latitude"], r["longitude"]), axis=1
    )
    df["dalam_radius"] = df["jarak_km"] <= radius_km
    df = df.sort_values("jarak_km").reset_index(drop=True)

    OUTPUT.mkdir(exist_ok=True)
    df.to_csv(OUTPUT / "hasil_analisis.csv", index=False, float_format="%.4f")

    peta = folium.Map(location=[latitude, longitude], zoom_start=12, control_scale=True, tiles=None)
    folium.Marker(
        [latitude, longitude], tooltip="Titik acuan",
        popup="Titik acuan analisis", icon=folium.Icon(color="red", icon="home")
    ).add_to(peta)
    folium.Circle(
        [latitude, longitude], radius=radius_km * 1000,
        color="#117f7b", fill=True, fill_opacity=0.08,
        tooltip=f"Radius {radius_km:g} km"
    ).add_to(peta)

    for _, r in df.iterrows():
        color = "green" if r["dalam_radius"] else "gray"
        popup = (f"<b>{r['nama']}</b><br>Kategori: {r['kategori']}"
                 f"<br>Jarak garis lurus: {r['jarak_km']:.2f} km"
                 f"<br>Dalam radius: {'Ya' if r['dalam_radius'] else 'Tidak'}")
        folium.Marker(
            [r["latitude"], r["longitude"]], tooltip=str(r["nama"]),
            popup=folium.Popup(popup, max_width=280),
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(peta)

    peta.save(OUTPUT / "peta_fasilitas.html")
    print("=== HASIL ANALISIS FASILITAS (DATA SIMULASI) ===")
    print(f"Titik acuan: ({latitude:.5f}, {longitude:.5f}) | Radius: {radius_km:g} km")
    print(df[["nama", "kategori", "jarak_km", "dalam_radius"]].to_string(index=False, formatters={"jarak_km": "{:.2f}".format}))
    print(f"\nTotal fasilitas: {len(df)} | Dalam radius: {int(df['dalam_radius'].sum())}")
    print("Output: output/hasil_analisis.csv dan output/peta_fasilitas.html")
    print("Catatan: jarak merupakan jarak garis lurus, bukan jarak tempuh jalan.")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analisis lokasi fasilitas berbasis GIS sederhana")
    parser.add_argument("--lat", type=float, default=-3.8004, help="Latitude titik acuan")
    parser.add_argument("--lon", type=float, default=102.2655, help="Longitude titik acuan")
    parser.add_argument("--radius", type=float, default=3.0, help="Radius analisis (km)")
    args = parser.parse_args()
    analyze(args.lat, args.lon, args.radius)
