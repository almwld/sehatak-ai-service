from triage_model import TriageModel, ChatBot, PredictionEngine

def test_triage_head():
    model = TriageModel()
    r = model.predict("صداع شديد ودوخة", "head")
    assert r["specialization"] == "الطب العصبي"
    assert r["urgency"] == "high"
    print("✅ Triage head test passed")

def test_triage_chest():
    model = TriageModel()
    r = model.predict("ألم في الصدر وضيق تنفس")
    assert r["specialization"] == "الصدرية والقلب"
    print("✅ Triage chest test passed")

def test_triage_unknown():
    model = TriageModel()
    r = model.predict("أعراض غريبة")
    assert r["specialization"] == "الطب العام"
    print("✅ Triage unknown test passed")

def test_seasonal():
    model = TriageModel()
    r = model.predict("كحة وحرارة")
    assert len(r["seasonal_risks"]) > 0
    print("✅ Seasonal risks test passed")

def test_chatbot_greeting():
    bot = ChatBot()
    r = bot.respond("سلام")
    assert r["type"] == "greeting"
    print("✅ ChatBot greeting test passed")

def test_chatbot_emergency():
    bot = ChatBot()
    r = bot.respond("عندي حالة طوارئ")
    assert r["type"] == "urgent"
    print("✅ ChatBot emergency test passed")

def test_chatbot_subscription():
    bot = ChatBot()
    r = bot.respond("كم سعر الباقة")
    assert r["type"] == "info"
    print("✅ ChatBot subscription test passed")

def test_chatbot_unknown():
    bot = ChatBot()
    r = bot.respond("xyz something unknown 123")
    assert r["create_ticket"] == True
    print("✅ ChatBot escalation test passed")

def test_emotion():
    bot = ChatBot()
    r = bot.respond("أنا حزين ومكتئب")
    assert r["type"] == "emotional"
    print("✅ Emotion detection test passed")

def test_prediction_engine():
    engine = PredictionEngine()
    r = engine.assess_risk({"age": 55, "smoking": True, "bmi": 32, "family_history": True})
    assert r["overall_risk"] == "مرتفع"
    assert len(r["risks"]) >= 3
    print("✅ Risk assessment test passed")

def test_symptom_checker():
    model = TriageModel()
    conditions = model.get_possible_conditions("صداع شديد", "head")
    assert len(conditions) >= 2
    assert "treatment" in conditions[0]
    print("✅ Symptom checker test passed")

if __name__ == "__main__":
    test_triage_head()
    test_triage_chest()
    test_triage_unknown()
    test_seasonal()
    test_chatbot_greeting()
    test_chatbot_emergency()
    test_chatbot_subscription()
    test_chatbot_unknown()
    test_emotion()
    test_prediction_engine()
    test_symptom_checker()
    print("\n🎉✅ All 11 tests passed successfully!")
