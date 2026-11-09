"""Tahap 1 - Menyiapkan dataset disasterinfo.

Membaca seluruh file .ndjson (incident-tweets), membersihkan placeholder dan
karakter rusak, membuang duplikat, lalu mengambil 500 tweet relevan dengan
sampling berstrata per event (seed tetap) dan menyimpannya ke
data/processed/disaster_clean.csv

Pemakaian (dari root proyek):
    python -m src.prepare_dataset data/raw/incident-tweets
"""
import json, re, glob, os, sys
import pandas as pd

RAW_DIR = sys.argv[1] if len(sys.argv) > 1 else "data/raw/incident-tweets"
OUT = "data/processed/disaster_clean.csv"
N_DOCS, SEED = 500, 42


def load(raw_dir):
    rows = []
    for f in sorted(glob.glob(os.path.join(raw_dir, "*.ndjson"))):
        event = os.path.basename(f)[:-len(".ndjson")]
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                d = json.loads(line)
                if not d.get("id") or not d.get("text"):
                    continue  # lewati baris tanpa id/teks
                rows.append({
                    "tweet_id": d["id"].strip("'"),
                    "event": event,
                    "disaster_type": event.split("-")[0],
                    "year": int(event.split("-")[-1]),
                    "text_raw": d["text"],
                    "relevance": d["relevance"],
                })
    return pd.DataFrame(rows)


def clean(t):
    t = t.replace("&amp;", "&")
    t = re.sub(r"<(URL|USER|SMILE|REPEAT|NUMBER|HASHTAG)>", " ", t)
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"[^\x20-\x7E]", " ", t)  # karakter rusak, emoji, kontrol
    return re.sub(r"\s+", " ", t).strip()


if __name__ == "__main__":
    df = load(RAW_DIR)
    df["text_clean"] = df["text_raw"].map(clean)
    df = df[df["text_clean"].str.split().str.len() >= 5]
    df = df.drop_duplicates("text_clean").drop_duplicates("tweet_id")
    rel = df[df["relevance"] == 1]
    per = N_DOCS // rel["event"].nunique() + 1
    parts = [g.sample(min(len(g), per), random_state=SEED)
             for _, g in rel.groupby("event")]
    sample = (pd.concat(parts).sample(N_DOCS, random_state=SEED)
              .reset_index(drop=True))
    sample.insert(0, "doc_id", range(1, len(sample) + 1))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    sample.to_csv(OUT, index=False, encoding="utf-8")
    print(sample.shape)
    print(sample["disaster_type"].value_counts())
