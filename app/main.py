import pandas as pd, json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .config import ROOT, DATA_PATH, METRICS_PATH
from .data_service import load_data, clean_data, validate_dataset
from .ml_service import train_models, predict_one
from .strategy_service import build_recommendations
from .database import save_dataframe, get_database_info

app = FastAPI(title="ABC HR Intelligence API")
app.mount("/static", StaticFiles(directory=str(ROOT/"static")), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    return (ROOT/"static"/"index.html").read_text(encoding="utf-8")

@app.get("/api/health")
def health():
    return {"status":"ok"}

@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Chỉ nhận file CSV.")
    try:
        df = pd.read_csv(file.file)
        validate_dataset(df)
        df.to_csv(DATA_PATH, index=False)
        save_dataframe(df)
        cleaned, log = clean_data(df)
        return {"message":"Tải dữ liệu thành công","shape":list(cleaned.shape),"cleaning":log, "database":get_database_info()}
    except Exception as e:
        raise HTTPException(400, str(e))

@app.get("/api/overview")
def overview():
    try:
        df, log = clean_data(load_data()); validate_dataset(df)
        yes = int((df.Attrition.astype(str).str.title()=="Yes").sum())
        n = len(df)
        return {"rows":n,"columns":len(df.columns),"attrition_yes":yes,
                "attrition_no":n-yes,"attrition_rate":yes/n if n else 0,"cleaning":log, "database":get_database_info()}
    except Exception as e:
        raise HTTPException(400,str(e))

@app.get("/api/eda")
def eda():
    try:
        df, _ = clean_data(load_data()); validate_dataset(df)
        df["flag"]=(df.Attrition.astype(str).str.title()=="Yes").astype(int)
        # These fields are useful for EDA, but not every valid Attrition CSV
        # contains all of them. Return empty series/maps for missing fields.
        dept=(df.groupby("Department").flag.mean().sort_values(ascending=False)
              if "Department" in df.columns else pd.Series(dtype=float))
        ot=(df.groupby("OverTime").flag.mean().to_dict()
            if "OverTime" in df.columns else {})
        sat=(df.groupby("JobSatisfaction").flag.mean().to_dict()
             if "JobSatisfaction" in df.columns else {})
        return {"attrition_rate":float(df.flag.mean()),
          "department_labels":dept.index.astype(str).tolist(),
          "department_rates":[float(x) for x in dept.values],
          "overtime_labels":[str(k) for k in ot],
          "overtime_rates":[float(v) for v in ot.values],
          "satisfaction_labels":[str(k) for k in sat],
          "satisfaction_rates":[float(v) for v in sat.values],
          "overtime_attrition_rate":float(ot.get("Yes",0)),
          "no_overtime_attrition_rate":float(ot.get("No",0)),
          "low_satisfaction_attrition_rate":float(sat.get(1,0)),
          "high_satisfaction_attrition_rate":float(sat.get(4,0))}
    except Exception as e:
        raise HTTPException(400,str(e))

@app.post("/api/train")
def train():
    try: return train_models()
    except Exception as e: raise HTTPException(400,str(e))

class PredictionInput(BaseModel):
    values: dict

@app.post("/api/predict")
def predict(body: PredictionInput):
    try: return predict_one(body.values)
    except Exception as e: raise HTTPException(400,str(e))

@app.get("/api/strategies")
def strategies():
    try: return {"basis":"EDA + bộ quy tắc giải thích được","recommendations":build_recommendations(eda())}
    except Exception as e: raise HTTPException(400,str(e))
