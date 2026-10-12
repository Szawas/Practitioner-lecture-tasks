"""Studi kasus edukasi: analisis transaksi dan prediksi pembayaran terlambat."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)
RNG = np.random.default_rng(42)
N = 1500

# Data sintetis: fitur tersedia saat faktur diterbitkan.
customers = RNG.integers(1, 151, N)
dates = pd.to_datetime("2025-01-01") + pd.to_timedelta(RNG.integers(0, 365, N), unit="D")
amount = np.round(RNG.lognormal(14.1, 0.65, N), -3)
cost = np.round(amount * RNG.uniform(0.65, 0.94, N), -3)
terms = RNG.choice([14, 30, 45], size=N, p=[0.25, 0.6, 0.15])
segment = RNG.choice(["Retail", "Grosir", "Korporat"], size=N, p=[0.55, 0.3, 0.15])
prior_late = RNG.poisson(0.8, N)
# Label dibentuk dari probabilitas sintetis, bukan hasil prediksi model.
logit = -2.8 + 0.52 * prior_late + 0.4 * (terms == 45) + 0.25 * (amount > 2_000_000) + 0.2 * (segment == "Retail")
prob = 1 / (1 + np.exp(-logit))
late = RNG.binomial(1, prob)
payment_delay = np.where(late == 1, RNG.integers(31, 91, N), RNG.integers(0, 31, N))

df = pd.DataFrame({
    "invoice_id": [f"INV-{i:05d}" for i in range(1, N + 1)],
    "customer_id": customers,
    "invoice_date": dates,
    "segment": segment,
    "invoice_amount": amount,
    "estimated_cost": cost,
    "payment_term_days": terms,
    "previous_late_payments": prior_late,
    "days_after_due_paid": payment_delay,  # Hanya untuk membentuk label, bukan fitur!
    "late_over_30_days": late,
})
df.to_csv(ROOT / "transaksi_simulasi.csv", index=False)

# Data understanding & cleaning
print("Jumlah baris awal:", len(df))
print("Missing values:\n", df.isna().sum())
df = df.drop_duplicates(subset="invoice_id").copy()
df["invoice_date"] = pd.to_datetime(df["invoice_date"])
df["profit_estimate"] = df["invoice_amount"] - df["estimated_cost"]
df["month"] = df["invoice_date"].dt.to_period("M").astype(str)
monthly = df.groupby("month", as_index=False).agg(
    revenue=("invoice_amount", "sum"),
    estimated_profit=("profit_estimate", "sum"),
    invoice_count=("invoice_id", "count"),
)
monthly.to_csv(OUT / "ringkasan_bulanan.csv", index=False)
print("\nTotal pendapatan: Rp{:,.0f}".format(df["invoice_amount"].sum()))
print("Total estimasi laba kotor: Rp{:,.0f}".format(df["profit_estimate"].sum()))
print("Persentase terlambat >30 hari: {:.1%}".format(df["late_over_30_days"].mean()))

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly["month"], monthly["revenue"] / 1e6, marker="o", label="Pendapatan")
ax.plot(monthly["month"], monthly["estimated_profit"] / 1e6, marker="o", label="Estimasi laba kotor")
ax.set(xlabel="Bulan", ylabel="Juta rupiah", title="Tren transaksi simulasi")
ax.tick_params(axis="x", rotation=45)
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "tren_bulanan.png", dpi=160)
plt.close(fig)

# Hindari data leakage: jangan masukkan tanggal pembayaran, hari keterlambatan,
# atau status pembayaran sebagai fitur.
features = ["invoice_amount", "payment_term_days", "previous_late_payments", "segment"]
X = df[features]
y = df["late_over_30_days"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
preprocess = ColumnTransformer([
    ("numeric", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler())]),
     ["invoice_amount", "payment_term_days", "previous_late_payments"]),
    ("category", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                           ("onehot", OneHotEncoder(handle_unknown="ignore"))]), ["segment"]),
])
model = Pipeline([("prepare", preprocess),
                  ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))])
model.fit(X_train, y_train)
pred = model.predict(X_test)
report = classification_report(y_test, pred, digits=3, zero_division=0)
print("\nEvaluasi model (data uji):\n", report)
(OUT / "evaluasi_model.txt").write_text(report, encoding="utf-8")
cm = confusion_matrix(y_test, pred, labels=[0, 1])
ConfusionMatrixDisplay(cm, display_labels=["Tidak terlambat", "Terlambat >30 hari"]).plot(cmap="Blues", values_format="d")
plt.title("Confusion matrix - data uji")
plt.tight_layout()
plt.savefig(OUT / "confusion_matrix.png", dpi=160)
plt.close()
print("\nSelesai. Lihat folder output/.")
