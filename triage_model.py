import re
from typing import Optional, Dict, List

class TriageModel:
    def __init__(self):
        self.specialization_map = {
            "head": ["\u0635\u062f\u0627\u0639", "\u062f\u0648\u0627\u0631", "\u0635\u062f\u0627\u0639 \u0645\u064a\u063a\u0631\u0627\u064a\u0646", "\u0627\u0631\u0647\u0627\u0642", "\u062f\u0648\u062e\u0629", "\u0631\u0623\u0633", "headache", "migraine", "dizziness"],
            "chest": ["\u0635\u062f\u0631", "\u0642\u0644\u0628", "\u0636\u064a\u0642 \u0627\u0644\u0646\u0641\u0633", "\u0633\u0639\u0627\u0644", "chest pain", "heart", "breathing", "cough"],
            "stomach": ["\u0628\u0637\u0646", "\u0645\u0639\u062f\u0629", "\u0625\u0633\u0647\u0627\u0644", "\u062a\u0642\u064a\u0621", "stomach", "abdomen", "nausea", "vomiting", "diarrhea"],
            "skin": ["\u0637\u0641\u062d \u062c\u0644\u062f\u064a", "\u062d\u0643\u0629", "\u0628\u0631\u0635", "\u062d\u0631\u0642", "rash", "skin", "itching", "acne", "eczema"],
            "bones": ["\u0639\u0638\u0627\u0645", "\u0645\u0641\u0627\u0635\u0644", "\u0638\u0647\u0631", "\u0645\u0641\u0635\u0644", "\u0631\u0642\u0628\u0629", "bones", "joints", "knee", "back pain", "fracture"],
            "mental": ["\u0642\u0644\u0642", "\u0627\u0643\u062a\u0626\u0627\u0628", "\u0627\u0631\u0647\u0627\u0642", "\u0627\u0643\u062a\u0626\u0627\u0628", "anxiety", "depression", "stress", "insomnia", "panic"],
            "children": ["\u0637\u0641\u0644", "\u0631\u0636\u064a\u0639", "\u062d\u0645\u0649", "baby", "child", "fever", "infant", "newborn"],
            "general": ["\u062d\u0631\u0627\u0631\u0629", "\u062a\u0639\u0628", "\u0625\u0631\u0647\u0627\u0642", "fever", "fatigue", "tired", "body ache"]
        }

        self.specialization_names = {
            "head": "\u0627\u0644\u0637\u0628 \u0627\u0644\u0639\u0635\u0628\u064a",
            "chest": "\u0627\u0644\u0635\u062f\u0631\u064a\u0629 \u0648\u0627\u0644\u0623\u0648\u0639\u064a\u0629",
            "stomach": "\u0627\u0644\u062c\u0647\u0627\u0632 \u0627\u0644\u0647\u0636\u0645\u064a",
            "skin": "\u0627\u0644\u062c\u0644\u062f\u064a\u0629",
            "bones": "\u0627\u0644\u0639\u0638\u0627\u0645 \u0648\u0627\u0644\u0645\u0641\u0627\u0635\u0644",
            "mental": "\u0627\u0644\u0635\u062d\u0629 \u0627\u0644\u0646\u0641\u0633\u064a\u0629",
            "children": "\u0637\u0628 \u0627\u0644\u0623\u0637\u0641\u0627\u0644",
            "general": "\u0627\u0644\u0637\u0628 \u0627\u0644\u0639\u0627\u0645"
        }

        self.urgency_keywords = {
            "high": ["\u0634\u062f\u064a\u062f", "\u0642\u0648\u064a", "\u062d\u0627\u062f\u062b", "emergency", "severe", "critical", "cant breathe", "unconscious", "bleeding heavily"],
            "medium": ["\u0645\u062a\u0648\u0633\u0637", "moderate", "persistent", "worsening", "constant"],
            "low": ["\u062e\u0641\u064a\u0641", "mild", "slight", "minor", " occasional"]
        }

    def predict(self, symptoms: str, body_part: Optional[str] = None) -> Dict:
        symptoms_lower = symptoms.lower()
        best_specialization = "general"
        max_score = 0

        if body_part and body_part in self.specialization_map:
            best_specialization = self.specialization_names.get(body_part, "\u0627\u0644\u0637\u0628 \u0627\u0644\u0639\u0627\u0645")
        else:
            for part, keywords in self.specialization_map.items():
                score = sum(1 for kw in keywords if kw in symptoms_lower)
                if score > max_score:
                    max_score = score
                    best_specialization = self.specialization_names.get(part, "\u0627\u0644\u0637\u0628 \u0627\u0644\u0639\u0627\u0645")

        urgency = "low"
        for u_level, keywords in self.urgency_keywords.items():
            if any(kw in symptoms_lower for kw in keywords):
                urgency = u_level
                break

        if urgency == "high":
            action = "\u0627\u0633\u062a\u0634\u0627\u0631\u0629 \u0641\u0648\u0631\u064a\u0629 \u0623\u0648 \u0632\u064a\u0627\u0631\u0629 \u0645\u0633\u062a\u0634\u0641\u0649"
        elif urgency == "medium":
            action = "\u0627\u0633\u062a\u0634\u0627\u0631\u0629 \u0637\u0628\u064a\u0629 \u0641\u064a \u0623\u0642\u0631\u0628 \u0648\u0642\u062a"
        else:
            action = "\u0645\u0631\u0627\u0642\u0628\u0629 \u0645\u0646\u0632\u0644\u064a\u0629 \u0648\u0627\u0633\u062a\u0634\u0627\u0631\u0629 \u0625\u0630\u0627 \u0627\u0633\u062a\u0645\u0631\u062a \u0627\u0644\u0623\u0639\u0631\u0627\u0636"

        return {
            "specialization": best_specialization,
            "urgency": urgency,
            "recommended_action": action,
            "confidence": 0.7 + (0.1 if body_part else 0) + (0.1 if max_score > 0 else 0)
        }

    def get_possible_conditions(self, symptoms: str, body_part: Optional[str] = None) -> List[Dict]:
        result = self.predict(symptoms, body_part)
        conditions_map = {
            "\u0627\u0644\u0637\u0628 \u0627\u0644\u0639\u0635\u0628\u064a": [
                {"name": "\u0635\u062f\u0627\u0639 \u062a\u0648\u062a\u0631\u064a", "probability": "\u0645\u062a\u0648\u0633\u0637"},
                {"name": "\u062f\u0648\u0627\u0631 \u0645\u0631\u062a\u0628\u0637\u0629 \u0628\u0627\u0644\u062c\u064a\u0648\u0628", "probability": "\u0645\u0646\u062e\u0641\u0636"}
            ],
            "\u0627\u0644\u0635\u062f\u0631\u064a\u0629 \u0648\u0627\u0644\u0623\u0648\u0639\u064a\u0629": [
                {"name": "\u0628\u0631\u0648\u0646\u0643\u0648\u0646 \u062d\u0627\u062f", "probability": "\u0645\u062a\u0648\u0633\u0637"},
                {"name": "\u0627\u0644\u062a\u0647\u0627\u0628 \u062d\u0644\u0642", "probability": "\u0645\u062a\u0648\u0633\u0637"}
            ],
            "\u0627\u0644\u062c\u0647\u0627\u0632 \u0627\u0644\u0647\u0636\u0645\u064a": [
                {"name": "\u062a\u0647\u0627\u0628 \u0645\u0639\u062f\u064a", "probability": "\u0645\u062a\u0648\u0633\u0637"},
                {"name": "\u0642\u0648\u0644\u0648\u0646 \u0639\u0635\u0628\u064a", "probability": "\u0645\u0646\u062e\u0641\u0636"}
            ],
            "\u0627\u0644\u0637\u0628 \u0627\u0644\u0639\u0627\u0645": [
                {"name": "\u0646\u0632\u0644\u0629 \u0628\u0631\u062f\u064a\u0629", "probability": "\u0645\u062a\u0648\u0633\u0637"},
                {"name": "\u0625\u0631\u0647\u0627\u0642 \u0639\u0627\u0645", "probability": "\u0645\u0646\u062e\u0641\u0636"}
            ]
        }
        return conditions_map.get(result["specialization"], [{"name": "\u064a\u062c\u0628 \u0627\u0633\u062a\u0634\u0627\u0631\u0629 \u0637\u0628\u064a\u0629", "probability": "\u063a\u064a\u0631 \u0645\u0639\u0631\u0641"}])


class ChatBot:
    def __init__(self):
        self.responses = {
            r"\b(\\u0643\u064a\u0641|how).*(\\u063a\u064a\u0631|change).*(\\u0645\u0631\u0648\u0631|password)\b": {
                "response": "\\u0644\u062a\u063a\u064a\u064a\u0631 \u0643\u0644\u0645\u0629 \u0627\u0644\u0645\u0631\u0648\u0631: \\u0627\u0630\u0647\u0628 \u0644\\u0644\u0645\u0644\u0641 \\u0627\u0644\u0634\u062e\u0635\u064a > \\u0627\u0644\u0623\u0645\u0627\u0646 > \\u062a\u063a\u064a\u064a\u0631 \\u0643\u0644\u0645\u0629 \\u0627\u0644\u0645\u0631\u0648\u0631",
                "type": "help",
                "create_ticket": False
            },
            r"\b(\\u0648\u0635\u0641\u0629|prescription).*(\\u0644\u0645|not|didn't).*(\\u062a\u0635\u0644|arrive|come)\b": {
                "response": "\\u064a\u0645\u0643\u0646\u0643 \\u0645\u0631\u0627\u062c\u0639\u0629 \\u0627\u0644\u0648\u0635\u0641\u0627\u062a \\u0641\u064a \\u0642\u0633\u0645 \\u0627\u0644\u0627\u0633\u062a\u0634\u0627\u0631\u0627\u062a \\u0627\u0644\u0633\u0627\u0628\u0642\u0629. \\u0625\u0630\u0627 \\u0645\u0633\u062a\u0645\u0631 \u0627\u0644\u0645\u0634\u0643\u0644\u0629\u060c \\u0633\u0623\u0642\u0648\u0645 \\u0628\u0625\u0646\u0634\u0627\u0621 \\u062a\u0630\u0643\u0631\u0629 \\u062f\u0639\u0645.",
                "type": "support",
                "create_ticket": False
            },
            r"\b(\\u0625\u0644\u063a\u0627\u0621|cancel).*(\\u0627\u0633\u062a\u0634\u0627\u0631\u0629|consultation)\b": {
                "response": "\\u0644\u0625\u0644\u063a\u0627\u0621 \\u0627\u0644\u0627\u0633\u062a\u0634\u0627\u0631\u0629: \\u0627\u0630\u0647\u0628 \\u0644\\u0642\u0633\u0645 \\u0627\u0644\u0627\u0633\u062a\u0634\u0627\u0631\u0627\u062a \\u0627\u0644\u062d\u062f\u064a\u062b\u0629 \\u0648\u0627\u0636\u063a\u0637 \\u0639\u0644\u0649 \\u0625\u0644\u063a\u0627\u0621. \\u064a\u0645\u0643\u0646 \\u0625\u0644\u063a\u0627\u0621 \\u0627\u0644\u0627\u0633\u062a\u0634\u0627\u0631\u0627\u062a \\u0627\u0644\u0646\u0634\u0637\u0629 \u0641\u0642\u0637.",
                "type": "help",
                "create_ticket": False
            },
            r"\\u0633\u0644\u0627\u0645|\\u0623\u0647\u0644\u0627\\u064b|\\u0645\u0631\u062d\u0628\\u0627": {
                "response": "\\u0648\\u0639\\u0644\\u064a\\u0643\\u0645 \\u0627\\u0644\\u0633\\u0644\\u0627\\u0645 \\u0648\\u0631\\u062d\\u0645\\u0629 \\u0627\\u0644\\u0644\\u0647 \\u0648\\u0628\\u0631\\u0643\\u0627\\u062a\\u0647! \\u0643\\u064a\\u0641 \\u064a\\u0645\\u0643\\u0646\\u0646\\u064a \\u0645\\u0633\\u0627\\u0639\\u062f\\u062a\\u0643\\u061f",
                "type": "greeting",
                "create_ticket": False
            },
            r"\\u0628\u0627\u0642\u0629|\\u0627\u0634\u062a\u0631\u0627\u0643|subscription|plan": {
                "response": "\\u0646\\u0648\\u0641\\u0631 \\u062b\\u0644\\u0627\\u062b \\u0628\\u0627\\u0642\\u0627\\u062a: \\u0627\\u0644\\u0623\\u0633\\u0627\\u0633\\u064a\\u0629 (49 \\u0631\\u064a\\u0627\\u0644)\\u060c \\u0627\\u0644\\u0645\\u0645\\u062a\\u0627\\u0632\\u0629 (99 \\u0631\\u064a\\u0627\\u0644)\\u060c \\u0627\\u0644\\u0639\\u0627\\u0626\\u0644\\u064a\\u0629 (189 \\u0631\\u064a\\u0627\\u0644). \\u0647\\u0644 \\u062a\\u0631\\u064a\\u062f \\u0627\\u0644\\u062a\\u0641\\u0627\\u0635\\u064a\\u0644\\u061f",
                "type": "info",
                "create_ticket": False
            }
        }

    def respond(self, message: str) -> Dict:
        for pattern, response in self.responses.items():
            if re.search(pattern, message, re.IGNORECASE):
                return response

        return {
            "response": "\\u0639\\u0630\\u0631\\u0627\\u064b\\u060c \\u0644\\u0645 \\u0623\\u0641\\u0647\\u0645 \\u0633\\u0624\\u0627\\u0644\\u0643. \\u0633\\u0623\\u0642\\u0648\\u0645 \\u0628\\u0646\\u0642\\u0644 \\u0633\\u0624\\u0627\\u0644\\u0643 \\u0644\\u0640 \\u0641\\u0631\\u064a\\u0642 \\u0627\\u0644\\u062f\\u0639\\u0645.",
            "type": "escalate",
            "create_ticket": True
        }
