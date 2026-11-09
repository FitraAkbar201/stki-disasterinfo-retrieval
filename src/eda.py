"""Tahap 2 - Eksplorasi data (EDA).

Jalankan dari root proyek:  python -m src.eda
Menampilkan ringkasan dan menyimpan grafik ke docs/.
"""
import os
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.config import DATA_CSV, DOCS_DIR, TEXT_COLUMN
from src.preprocessing import preprocess


def main():
    df = pd.read_csv(DATA_CSV)
    os.makedirs(DOCS_DIR, exist_ok=True)

    print("Jumlah dokumen :", len(df))
    print("Jumlah event   :", df["event"].nunique())
    print("Nilai kosong   :\n", df.isna().sum().to_string())

    df["n_char"] = df[TEXT_COLUMN].str.len()
    df["n_word"] = df[TEXT_COLUMN].str.split().str.len()
    print("\nPanjang dokumen (kata):\n", df["n_word"].describe().round(1).to_string())

    print("\nJenis bencana:\n", df["disaster_type"].value_counts().to_string())
    print("\nTahun:\n", df["year"].value_counts().sort_index().to_string())

    tokens = [t for text in df[TEXT_COLUMN] for t in preprocess(text)]
    freq = Counter(tokens)
    print("\nTotal token setelah preprocessing:", len(tokens))
    print("Ukuran vocabulary                :", len(freq))
    print("20 term terbanyak:", freq.most_common(20))

    fig, ax = plt.subplots(1, 3, figsize=(16, 4.5))
    df["disaster_type"].value_counts().plot.barh(ax=ax[0], color="#c0392b")
    ax[0].set_title("Dokumen per jenis bencana"); ax[0].invert_yaxis()
    ax[1].hist(df["n_word"], bins=20, color="#2980b9")
    ax[1].set_title("Distribusi panjang dokumen (kata)")
    top = freq.most_common(15)
    ax[2].barh([w for w, _ in top][::-1], [c for _, c in top][::-1], color="#27ae60")
    ax[2].set_title("15 term terbanyak")
    plt.tight_layout()
    out = os.path.join(DOCS_DIR, "eda.png")
    plt.savefig(out, dpi=130)
    print("\nGrafik disimpan ke", out)


if __name__ == "__main__":
    main()
