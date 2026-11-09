# Sistem Temu Kembali Informasi (STKI) - DisasterInfo Retrieval

Mesin pencari informasi bencana (tweet kejadian bencana) berbahasa Inggris.
Menerapkan pemrosesan teks, pembobotan **TF-IDF** (implementasi manual), dan pemeringkatan
**Cosine Similarity** melalui *inverted index*, dengan antarmuka web Flask.
Proyek mata kuliah Sistem Temu Kembali Informasi.

## Progres plan
- [x] Tahap 1 - Dataset: `src/prepare_dataset.py` -> `data/processed/disaster_clean.csv` (500 tweet)
- [x] Tahap 2 - EDA: `src/eda.py` (grafik di `docs/eda.png`)
- [x] Tahap 3 - Preprocessing: `src/preprocessing.py` (cleaning, case folding, tokenizing, stopword NLTK, Porter stemmer)
- [] Tahap 4 - TF-IDF manual + inverted index: `src/tfidf.py`, `src/build_index.py`
- [] Tahap 5 - Cosine similarity + ranking: `src/search_engine.py`, `src/cli.py`
- [] Tahap 6 - Web Flask: `app/`
- [] Tahap 7 - Evaluasi: `src/evaluation.py`, laporan di `docs/evaluasi.md`

## Struktur Direktori
```
stki-disaster-retrieval/
├── data/
│   ├── processed/disaster_clean.csv   # 500 tweet relevan, sampling berstrata per event
│   ├── raw/                           # data mentah (tidak di-commit)
│   └── index/                         # indeks hasil build (dibuat otomatis, tidak di-commit)
├── src/
│   ├── config.py            # path & parameter
│   ├── prepare_dataset.py   # membuat disaster_clean.csv dari data mentah
│   ├── eda.py               # eksplorasi data
│   ├── preprocessing.py     # pipeline teks
│   ├── tfidf.py             # TF, IDF, vektor, inverted index, cosine
│   ├── search_engine.py     # build/load indeks, ranking, snippet, filter
│   ├── build_index.py       # skrip membangun indeks
│   ├── cli.py               # pencarian lewat terminal
│   └── evaluation.py        # Precision/Recall/MAP/MRR/nDCG
├── app/                     # aplikasi web Flask (app.py, templates/, static/)
├── notebooks/               # analisis & penjelasan langkah demi langkah (sudah dijalankan)
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing_tfidf_cosine.ipynb
│   └── 03_evaluasi.ipynb
├── tests/                   # 37 uji otomatis (pytest)
├── docs/                    # arsitektur.md, evaluasi.md, grafik & tangkapan layar
├── requirements.txt
└── README.md
```

## Cara Menjalankan
Semua perintah dijalankan dari **root proyek**.
```
python -m venv venv
venv\Scripts\activate            # Windows  (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt

python -m src.eda                # (opsional) ringkasan dataset
python -m src.build_index        # bangun indeks
python -m src.cli "earthquake nepal"   # cari lewat terminal
python -m app.app                # web di http://127.0.0.1:5000
python -m src.evaluation         # evaluasi kualitas pencarian
python -m pytest                 # uji otomatis
jupyter notebook notebooks/      # buka notebook analisis (opsional)
```
`disaster_clean.csv` sudah disertakan. Untuk membuatnya ulang dari data mentah:
`python -m src.prepare_dataset data/raw/incident-tweets`.

## Alur Sistem
1. **Preprocessing**: buang URL/mention/simbol/angka -> case folding -> tokenizing -> stopword removal -> stemming Porter.
2. **Pembobotan TF-IDF**: `TF = 1 + log10(f)`, `IDF = log10(N/df) + 1`, vektor dokumen dinormalisasi L2.
3. **Pencarian**: query melewati pipeline yang sama; skor cosine dihitung lewat inverted index lalu diurutkan.
4. **Tampilan**: 10 hasil teratas dengan skor, kata query disorot, filter jenis bencana dan tahun,
   halaman detail dengan dokumen terkait, serta endpoint JSON `/api/search?q=...`.

Detail rumus dan alasan desain: `docs/arsitektur.md`.

## Hasil Evaluasi (28 query, kunci jawaban dari label `event`)
| Metrik | TF-IDF | TF saja |
|---|---|---|
| P@5 | 0.893 | 0.893 |
| P@10 | 0.739 | 0.714 |
| MAP | 0.608 | 0.598 |
| MRR | 0.964 | 0.982 |
| nDCG@10 | 0.798 | 0.785 |

Selisih TF-IDF dan TF saja kecil sehingga belum cukup untuk menyimpulkan IDF unggul.
Analisis kesalahan dan keterbatasan lengkap ada di `docs/evaluasi.md`.

## Catatan Dataset
Sumber: *Disaster Tweet Filtering - incident tweets* (48 event, 163.718 tweet berbahasa Inggris, label `relevance`).
Diambil 500 tweet relevan dengan sampling berstrata per event (seed 42); satu event tidak punya
tweet yang lolos penyaringan sehingga koleksi memuat 47 event. Tweet sudah dalam huruf kecil dengan
placeholder (`<URL>`, `<HASHTAG>`, ...) yang dibuang pada tahap pembersihan.

## Keterbatasan
Pencarian bersifat leksikal (tidak memahami sinonim), tagar bersambung tidak dipecah, query harus
berbahasa Inggris, dan kunci jawaban evaluasi dibuat otomatis dari label dataset.
