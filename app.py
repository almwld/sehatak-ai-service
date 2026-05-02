from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
import numpy as np
from triage_model import TriageModel, ChatBot, PredictionEngine
from neural_medical_model import MedicalNeuralNetwork, DeepHealthAnalyzer, TensorFlowMedicalModel

app = FastAPI(title="Sehtak AI Service v4.0 - Neural", version="4.0.0")

triage_model = TriageModel()
chatbot = ChatBot()
prediction_engine = PredictionEngine()
neural_net = MedicalNeuralNetwork()
deep_analyzer = DeepHealthAnalyzer()

class TriageRequest(BaseModel):
    symptoms: str
    body_part: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict] = None

class DeepAnalysisRequest(BaseModel):
    symptoms: str
    age: int = 35
    gender: str = "ذكر"

class RiskRequest(BaseModel):
    age: int = 30
    smoking: bool = False
    bmi: float = 25
    family_history: bool = False

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "Sehtak AI v4.0 Neural",
        "models": ["Triage", "ChatBot", "Neural Network", "TensorFlow", "Embeddings"],
        "endpoints": 10
    }

@app.post("/triage")
async def triage(req: TriageRequest):
    result = triage_model.predict(req.symptoms, req.body_part)
    return result

@app.post("/neural-diagnosis")
async def neural_diagnosis(req: TriageRequest):
    """تشخيص باستخدام الشبكة العصبية"""
    result = neural_net.predict(req.symptoms)
    deep = neural_net.analyze_symptoms_deep(req.symptoms)
    return {"neural_prediction": result, "symptom_analysis": deep}

@app.post("/deep-analysis")
async def deep_analysis(req: DeepAnalysisRequest):
    """تحليل صحي شامل بكل النماذج"""
    result = deep_analyzer.comprehensive_analysis(req.symptoms, req.age, req.gender)
    return result

@app.post("/symptom-checker")
async def symptom_checker(req: TriageRequest):
    triage_result = triage_model.predict(req.symptoms, req.body_part)
    neural_result = neural_net.predict(req.symptoms)
    conditions = triage_model.get_possible_conditions(req.symptoms, req.body_part)
    
    return {
        "possible_conditions": conditions,
        "triage_specialist": triage_result["specialization"],
        "neural_network_specialist": neural_result["top_prediction"]["specialty"],
        "urgency": triage_result["urgency"],
        "timeframe": triage_result["timeframe"],
        "notes": "⚠️ هذا تشخيص اولي فقط ولا يعوض عن الاستشارة الطبية"
    }

@app.post("/chatbot")
async def chatbot_endpoint(req: ChatRequest):
    result = chatbot.respond(req.message, req.context)
    return result

@app.post("/assess-risk")
async def assess_risk(req: RiskRequest):
    return prediction_engine.assess_risk(req.dict())

@app.post("/drug-info")
async def drug_info(drug_name: str):
    info = triage_model.get_drug_info(drug_name)
    if not info:
        raise HTTPException(status_code=404, detail="Drug not found")
    return info

@app.post("/disease-info")
async def disease_info(disease_name: str):
    info = triage_model.get_disease_info(disease_name)
    if not info:
        raise HTTPException(status_code=404, detail="Disease not found")
    return info

@app.post("/lab-test-info")
async def lab_test_info(test_name: str):
    info = triage_model.get_lab_test_info(test_name)
    if not info:
        raise HTTPException(status_code=404, detail="Test not found")
    return info

@app.get("/health-tip")
async def health_tip():
    return {"tip": triage_model.get_random_tip()}

@app.post("/follow-up")
async def follow_up(consultation_id: str, patient_response: str):
    if "أسوأ" in patient_response or "worse" in patient_response.lower():
        return {"action": "alert_doctor", "message": "المريض يشعر بتساخن الحالة"}
    elif "حسنت" in patient_response or "better" in patient_response.lower():
        return {"action": "close_case", "message": "تم إغلاق الحالة"}
    return {"action": "continue_monitoring", "message": "استمر في المتابعة"}

@app.post("/marketing-recommend")
async def marketing_recommend(user_history: Dict):
    consultations = user_history.get("consultations", [])
    chronic_keywords = ["سكري", "ضغط", "قلب", "رئة"]
    has_chronic = any(any(k in c.get("symptoms", "") for k in chronic_keywords) for c in consultations)
    
    if has_chronic and len(consultations) > 3:
        return {"recommendation": "family_plan", "message": "نوصيك بباقة عائلية"}
    elif len(consultations) > 5:
        return {"recommendation": "premium_plan", "message": "الباقة الممتازة مناسبة لك"}
    return {"recommendation": "basic_plan", "message": "استمر في الباقة الاساسية"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
