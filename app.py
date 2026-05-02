from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
from triage_model import TriageModel, ChatBot

app = FastAPI(title="Sehtak AI Service", version="1.0.0")

triage_model = TriageModel()
chatbot = ChatBot()

class TriageRequest(BaseModel):
    symptoms: str
    body_part: Optional[str] = None

class TriageResponse(BaseModel):
    specialization: str
    urgency: str
    recommended_action: str
    confidence: float

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    type: str
    create_ticket: bool = False

@app.get("/health")
async def health():
    return {"status": "ok", "service": "Sehtak AI"}

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
            "notes": "\u0647\u0630\u0627 \u062a\u0634\u062e\u064a\u0635 \u0627\u0648\u0644\u064a \u0641\u0642\u0637 \u0648\u0644\u0627 \u064a\u0639\u0648\u0636 \u0639\u0646 \u0627\u0644\u0627\u0633\u062a\u0634\u0627\u0631\u0629 \u0627\u0644\u0637\u0628\u064a\u0629"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chatbot", response_model=ChatResponse)
async def chatbot_endpoint(req: ChatRequest):
    try:
        result = chatbot.respond(req.message)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/follow-up")
async def follow_up(consultation_id: str, patient_response: str):
    if "\u0623\u0633\u0648\u0623" in patient_response or "worse" in patient_response.lower():
        return {"action": "alert_doctor", "message": "\u0627\u0644\u0645\u0631\u064a\u0636 \u064a\u0634\u0639\u0631 \u0628\u062a\u0633\u0627\u062e\u0646 \u0627\u0644\u062d\u0627\u0644\u0629"}
    elif "\u062d\u0633\u0646\u062a" in patient_response or "better" in patient_response.lower():
        return {"action": "close_case", "message": "\u062a\u0645 \u0625\u063a\u0644\u0627\u0642 \u0627\u0644\u062d\u0627\u0644\u0629"}
    return {"action": "continue_monitoring", "message": "\u0627\u0633\u062a\u0645\u0631 \u0641\u064a \u0627\u0644\u0645\u062a\u0627\u0628\u0639\u0629"}

@app.post("/marketing-recommend")
async def marketing_recommend(user_history: Dict):
    consultations = user_history.get("consultations", [])
    chronic_keywords = ["\u0633\u0643\u0631\u064a", "\u0636\u063a\u0637", "\u0642\u0644\u0628", "\u0631\u0626\u0629"]
    has_chronic = any(any(k in c.get("symptoms", "") for k in chronic_keywords) for c in consultations)

    if has_chronic and len(consultations) > 3:
        return {"recommendation": "family_plan", "message": "\u0628\u0645\u0627 \u0623\u0646\u0643 \u062a\u0633\u062a\u062e\u062f\u0645 \u0627\u0644\u0645\u0646\u0635\u0629 \u0628\u0643\u062b\u0631\u0629\u060c \u0646\u0648\u0635\u064a\u0643 \u0628\u0628\u0627\u0642\u0629 \u0639\u0627\u0626\u0644\u064a\u0629"}
    elif len(consultations) > 5:
        return {"recommendation": "premium_plan", "message": "\u0627\u0634\u062a\u0631\u0643 \u0641\u064a \u0627\u0644\u0628\u0627\u0642\u0629 \u0627\u0644\u0645\u0645\u062a\u0627\u0632\u0629 \u0644\u0627\u0633\u062a\u0634\u0627\u0631\u0627\u062a \u063a\u064a\u0631 \u0645\u062d\u062f\u0648\u062f\u0629"}
    return {"recommendation": "basic_plan", "message": "\u0627\u0633\u062a\u0645\u0631 \u0641\u064a \u0627\u0644\u0628\u0627\u0642\u0629 \u0627\u0644\u0627\u0633\u0627\u0633\u064a\u0629"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
