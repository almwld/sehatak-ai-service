from triage_model import TriageModel, ChatBot

def test_triage():
    model = TriageModel()
    r = model.predict("صداع شديد ودوخة", "head")
    assert r["specialization"] == "الطب العصبي"
    assert r["urgency"] in ["high", "medium", "low"]
    print("✅ Triage test passed")

def test_chatbot():
    bot = ChatBot()
    r = bot.respond("سلام عليكم")
    assert r["type"] == "greeting"
    print("✅ ChatBot test passed")

def test_unknown():
    bot = ChatBot()
    r = bot.respond("xyz123")
    assert r["create_ticket"] == True
    print("✅ Unknown test passed")

if __name__ == "__main__":
    test_triage()
    test_chatbot()
    test_unknown()
    print("\n🎉 All tests passed!")
