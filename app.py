from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
from triage_model import TriageModel, ChatBot, PredictionEngine

app = FastAPI(title="Sehtak AI Service v2.0", version="2.0.0")

triage_model = TriageModel()
chatbot = ChatBot()
prediction_engine = PredictionEngine()

class TriageRequest(BaseModel):
    symptoms: str
    body_part: Optional[str] = None

class TriageResponse(BaseModel):
    specialization: str
    urgency: str
    recommended_action: str
    timeframe: str
    confidence: float
    seasonal_risks: list = []

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict] = None

class ChatResponse(BaseModel):
    response: str
    type: str
    create_ticket: bool = False
    ticket_priority: str = "normal"
    timestamp: str = ""

class RiskRequest(BaseModel):
    age: int = 30
    smoking: bool = False
    bmi: float = 25
    family_history: bool = False

@app.get("/health")
async def health():
    return {"status": "ok", "service": "Sehtak AI v2.0", "endpoints": 6}

@app.post("/triage", response_model=TriageResponse)
async def triage(req: TriageRequest):
    try:
        result = triage_model.predict(req.symptoms, req.body_part)
        return TriageResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/symptom-checker")
async def symptom_checker(req: TriageRequest):
    try:
        result = triage_model.predict(req.symptoms, req.body_part)
        conditions = triage_model.get_possible_conditions(req.symptoms, req.body_part)
        return {
            "possible_conditions": conditions,
            "recommended_specialist": result["specialization"],
            "urgency": result["urgency"],
            "timeframe": result["timeframe"],
            "seasonal_risks": result["seasonal_risks"],
            "notes": "⚠️ هذا تشخيص اولي فقط ولا يعوض عن الاستشارة الطبية"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chatbot", response_model=ChatResponse)
async def chatbot_endpoint(req: ChatRequest):
    try:
        result = chatbot.respond(req.message, req.context)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/assess-risk")
async def assess_risk(req: RiskRequest):
    try:
        data = req.dict()
        result = prediction_engine.assess_risk(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/follow-up")
async def follow_up(consultation_id: str, patient_response: str):
    if "أسوأ" in patient_response or "worse" in patient_response.lower():
        return {"action": "alert_doctor", "message": "المريض يشعر بتساخن الحالة - تنبيه الطبيب"}
    elif "حسنت" in patient_response or "better" in patient_response.lower():
        return {"action": "close_case", "message": "تم إغلاق الحالة"}
    return {"action": "continue_monitoring", "message": "استمر في المتابعة"}

@app.post("/marketing-recommend")
async def marketing_recommend(user_history: Dict):
    consultations = user_history.get("consultations", [])
    chronic_keywords = ["سكري", "ضغط", "قلب", "رئة"]
    has_chronic = any(any(k in c.get("symptoms", "") for k in chronic_keywords) for c in consultations)

    if has_chronic and len(consultations) > 3:
        return {"recommendation": "family_plan", "message": "بما أنك تستخدم المنصة بكثرة، نوصيك بباقة عائلية"}
    elif len(consultations) > 5:
        return {"recommendation": "premium_plan", "message": "اشترك في الباقة الممتازة لاستشارات غير محدودة"}
    return {"recommendation": "basic_plan", "message": "استمر في الباقة الاساسية"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
