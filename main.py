from fastapi import FastAPI
from pydantic import BaseModel
from analyzer import analyze_text

app = FastAPI()

class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    secured_text: str
    log: list

@app.get("/")
def health_check():
    return {"message": "Sensitive Info Analyzer is running."}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    result = analyze_text(request.text)
    return {
        "secured_text": result["secured_text"],
        "log": result["log"]
    }
