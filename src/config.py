"""Path dan parameter proyek."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_CSV = os.path.join(ROOT, "data", "processed", "disaster_clean.csv")
INDEX_DIR = os.path.join(ROOT, "data", "index")
DOCS_DIR = os.path.join(ROOT, "docs")

TEXT_COLUMN = "text_clean"
TOP_K = 10
