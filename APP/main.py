from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import random

app = FastAPI(
    title='Suframa Digital - Motor Risco',
    description='API para análise de risco de Notas Fiscais e PINs',
    version='1.0.0'
)

class RiskAnalysisRequest(BaseModel):
    pin_id: str 
    company_name: str 
    merchandise_value: float = Field(gt=0, example=150000.00)
    origin_state : str = Field(min_length=2, max_length=2, example="SP")
    destination_state : str = Field(min_length=2, max_length=2, example="AM")
    has_previous_infractions: bool

class RiskAnalysisResponse(BaseModel): 
    pin_id: str
    risk_score: int
    risk_level: str
    analysis_timestamp: datetime


def calculate_risk_score(value: float, has_infractions: bool):
    # CANAL VERMELHO
    if has_infractions or value > 500000:
        channel = "VERMELHO"
        if has_infractions:
            score = random.randint(90, 100)
        else:
            base_score = 80
            extra = min((value - 500000) / 50000, 20) 
            score = int(base_score + extra)
    elif 100000 <= value <= 500000 and not has_infractions:
        channel = "AMARELO"
        percentual_na_faixa = (value - 100000) / (500000 - 100000)
        score = int(40 + (percentual_na_faixa * 39))

    else:
        channel = "VERDE"
        percentual_na_faixa = value / 100000
        score = int(percentual_na_faixa * 39)
    
    return score, channel


@app.get("/")
def read_root():
    return {"message": "Motor de Risco SUFRAMA Digital esta online!"}

@app.post("/api/v1/risk-score", response_model=RiskAnalysisResponse)
async def analyze_risk(payload: RiskAnalysisRequest):
    score, channel = calculate_risk_score(
        payload.merchandise_value, 
        payload.has_previous_infractions
    )

    return {
        "pin_id": payload.pin_id,  
        "risk_score": score,
        "risk_level": channel,
        "analysis_timestamp": datetime.now()
    }

        

