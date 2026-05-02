import sys
from triage_model import TriageModel, ChatBot, PredictionEngine
from neural_medical_model import MedicalNeuralNetwork, DeepHealthAnalyzer, SymptomEmbeddingModel

def test_neural_predict():
    nn = MedicalNeuralNetwork()
    r = nn.predict("صداع شديد مع دوخة وغثيان")
    assert len(r["all_predictions"]) == 3
    print("✅ Neural predict passed")

def test_deep_analysis():
    da = DeepHealthAnalyzer()
    r = da.comprehensive_analysis("صداع شديد وحمى وتعب", 45, "ذكر")
    assert "neural_network_diagnosis" in r
    print("✅ Deep analysis passed")

def test_symptom_embedding():
    se = SymptomEmbeddingModel()
    similar = se.find_similar("صداع")
    assert len(similar) > 0
    print("✅ Symptom embedding passed")

def test_deep_symptoms():
    nn = MedicalNeuralNetwork()
    r = nn.analyze_symptoms_deep("صداع ودوخة وغثيان")
    assert r["count"] >= 3
    print("✅ Deep symptoms passed")

def test_triage():
    r = TriageModel().predict("صداع شديد", "head")
    assert r["specialization"] == "الطب العصبي"
    print("✅ Triage passed")

def test_chatbot():
    r = ChatBot().respond("سلام")
    assert r["type"] == "greeting"
    print("✅ ChatBot passed")

def test_drug_info():
    info = TriageModel().get_drug_info("باراسيتامول")
    assert info and "مسكن" in info["category"]
    print("✅ Drug info passed")

def test_prediction_engine():
    r = PredictionEngine().assess_risk({"age": 55, "smoking": True, "bmi": 32, "family_history": True})
    assert r["overall_risk"] == "مرتفع"
    print("✅ Risk assessment passed")

if __name__ == "__main__":
    tests = [test_neural_predict, test_deep_analysis, test_symptom_embedding, 
             test_deep_symptoms, test_triage, test_chatbot, test_drug_info, test_prediction_engine]
    passed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"❌ {t.__name__} failed: {e}")
    print(f"\n🎉 {passed}/{len(tests)} tests passed!")
