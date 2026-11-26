import json, joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from .config import MODEL_PATH, METRICS_PATH
from .data_service import load_data, clean_data, validate_dataset

TARGET = "Attrition"
DROP_COLS = ["EmployeeCount", "Over18", "StandardHours", "EmployeeNumber"]

def prepare(df):
    df, log = clean_data(df)
    validate_dataset(df)
    y = df[TARGET].astype(str).str.strip().str.title().map({"No": 0, "Yes": 1})
    X = df.drop(columns=[TARGET] + [c for c in DROP_COLS if c in df.columns], errors="ignore")
    nums = X.select_dtypes(include=["number"]).columns.tolist()
    cats = [c for c in X.columns if c not in nums]
    return X, y, nums, cats, log

def train_models():
    X, y, nums, cats, clean_log = prepare(load_data())
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    numeric = Pipeline([("imputer", SimpleImputer(strategy="median")),
                        ("scale", StandardScaler())])
    categorical = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                            ("onehot", OneHotEncoder(handle_unknown="ignore"))])
    prep = ColumnTransformer([("num", numeric, nums), ("cat", categorical, cats)])
    models = {
        # liblinear avoids the iprint option warning from the lbfgs/SciPy
        # combination in some environments and supports this binary target.
        "Logistic Regression": LogisticRegression(solver="liblinear", max_iter=2000,
                                                   class_weight="balanced"),
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42, class_weight="balanced"),
        "Random Forest": RandomForestClassifier(n_estimators=250, min_samples_leaf=3,
                                                 random_state=42, class_weight="balanced")
    }
    results, fitted = [], {}
    for name, estimator in models.items():
        pipe = Pipeline([("preprocess", prep), ("model", estimator)])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        prob = pipe.predict_proba(X_test)[:, 1]
        results.append({
            "model": name,
            "accuracy": round(float(accuracy_score(y_test, pred)), 4),
            "precision": round(float(precision_score(y_test, pred, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, pred, zero_division=0)), 4),
            "f1": round(float(f1_score(y_test, pred, zero_division=0)), 4),
            "roc_auc": round(float(roc_auc_score(y_test, prob)), 4),
            "confusion_matrix": confusion_matrix(y_test, pred).tolist()
        })
        fitted[name] = pipe
    best = max(results, key=lambda x: x["f1"])
    joblib.dump({"pipeline": fitted[best["model"]], "features": X.columns.tolist(),
                 "model_name": best["model"]}, MODEL_PATH)
    payload = {"results": results, "best_model": best["model"],
               "cleaning": clean_log, "test_size": 0.2, "random_state": 42}
    METRICS_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload

def predict_one(values):
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Hãy huấn luyện mô hình trước.")
    saved = joblib.load(MODEL_PATH)
    row = pd.DataFrame([{c: values.get(c, np.nan) for c in saved["features"]}])
    p = float(saved["pipeline"].predict_proba(row)[0, 1])
    level = "Cần quan tâm" if p >= .60 else ("Theo dõi" if p >= .30 else "Chưa có tín hiệu cao")
    return {"model": saved["model_name"], "attrition_probability": round(p, 4),
            "risk_level": level,
            "note": "Xác suất thống kê, không phải kết luận chắc chắn về cá nhân."}
