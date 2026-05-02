from triage_model import TriageModel, ChatBot, PredictionEngine
from neural_medical_model import MedicalNeuralNetwork, DeepHealthAnalyzer, SymptomEmbeddingModel

def test_neural_predict():
    nn = MedicalNeuralNetwork()
    r = nn.predict("صداع شديد مع دوخة وغثيان")
    assert len(r["all_predictions"]) == 3
    assert r["top_prediction"]["confidence"] > 0
    print("✅ Neural predict")

def test_deep_analysis():
    da = DeepHealthAnalyzer()
    r = da.comprehensive_analysis("صداع شديد وحمى وتعب", 45, "ذكر")
    assert "neural_network_diagnosis" in r
    assert "risk_assessment" in r
    print("✅ Deep analysis")

def test_symptom_embedding():
    se = SymptomEmbeddingModel()
    similar = se.find_similar("صداع")
    assert len(similar) > 0
    print("✅ Symptom embedding")

def test_deep_symptoms():
    nn = MedicalNeuralNetwork()
    r = nn.analyze_symptoms_deep("صداع ودوخة وغثيان")
    assert r["count"] >= 3
    print("✅ Deep symptoms")

def test_neural_multi_symptoms():
    nn = MedicalNeuralNetwork()
    r = nn.predict("ألم صدر وضيق تنفس وخفقان وتعرق")
    assert "صدر" in r["top_prediction"]["specialty"] or "قلب" in r["top_prediction"]["specialty"]
    print("✅ Multi-symptom neural")

if __name__ == "__main__":
    test_neural_predict()
    test_deep_analysis()
    test_symptom_embedding()
    test_deep_symptoms()
    test_neural_multi_symptoms()
    print("\n🎉 All neural tests passed!")
