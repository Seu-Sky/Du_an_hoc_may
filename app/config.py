from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
ARTIFACT_DIR = ROOT / "artifacts"
DATA_PATH = DATA_DIR / "hr_data.csv"
MODEL_PATH = ARTIFACT_DIR / "best_model.joblib"
METRICS_PATH = ARTIFACT_DIR / "metrics.json"
DATA_DIR.mkdir(exist_ok=True)
ARTIFACT_DIR.mkdir(exist_ok=True)
