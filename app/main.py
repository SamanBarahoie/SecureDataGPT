# app/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import io
from .analyzer import analyze_dataset


app = FastAPI(title="SecureDataGPT", description="AI-powered Data Privacy and Analysis Assistant")

@app.get("/")
def root():
    return {"message": "Welcome to SecureDataGPT 🚀 - Upload your data for analysis."}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """
    Endpoint for analyzing uploaded datasets (CSV, Excel, JSON).
    """
    try:
        contents = await file.read()

        # Detect file type
        if file.filename.endswith(".csv"):
            df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(contents))
        elif file.filename.endswith(".json"):
            df = pd.read_json(io.StringIO(contents.decode("utf-8")))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload CSV, Excel, or JSON.")

        report = analyze_dataset(df)
        return JSONResponse(content=report)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
