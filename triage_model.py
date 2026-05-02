import re
import json
from typing import Optional, Dict, List
from datetime import datetime, timedelta

class TriageModel:
    def __init__(self):
        # قاعدة معرفية موسعة بـ 50+ حالة
        self.specialization_map = {
            "head": ["صداع", "دوار", "صداع ميغراين", "ارهاق", "دوخة", "رأس", "نصفي", "headache", "migraine", "dizziness", "vertigo"],
            "chest": ["صدر", "قلب", "ضيق النفس", "سعال", "كحة", "بلغم", "نهجان", "chest pain", "heart", "breathing", "cough", "wheezing"],
            "stomach": ["بطن", "معدة", "إسهال", "تقيء", "غثيان", "امساك", "غازات", "حرقة", "stomach", "abdomen", "nausea", "vomiting", "diarrhea", "constipation", "bloating"],
            "skin": ["طفح جلدي", "حكة", "برص", "حرق", "احمرار", "بثور", "تورم", "rash", "skin", "itching", "acne", "eczema", "redness", "swelling"],
            "bones": ["عظام", "مفاصل", "ظهر", "مفصل", "رقبة", "ركبة", "كسر", "تورم مفصل", "bones", "joints", "knee", "back pain", "fracture", "arthritis"],
            "mental": ["قلق", "اكتئاب", "ارهاق", "ارق", "خوف", "هلع", "حزن", "توتر", "انتحار", "anxiety", "depression", "stress", "insomnia", "panic", "sadness", "suicidal"],
            "children": ["طفل", "رضيع", "حمى", "تسنين", "مغص", "baby", "child", "fever", "infant", "newborn", "teething", "colic"],
            "eyes": ["عين", "رؤية", "نظر", "غشاوة", "احمرار عين", "دموع", "eye", "vision", "blurry", "red eye", "tearing"],
            "ent": ["أذن", "أنف", "حلق", "زكام", "رشح", "عطس", "تهاب حلق", "ear", "nose", "throat", "cold", "sneeze", "sore throat", "tonsils"],
            "dental": ["أسنان", "ضرس", "لثة", "فم", "تسوس", "dental", "tooth", "gum", "mouth", "cavity"],
            "urinary": ["بول", "حرقان", "تبول", "مثانة", "دم في بول", "urine", "urinary", "bladder", "burning", "blood in urine"],
            "diabetes": ["سكر", "عطش", "جوع", "تبول كثير", "تنميل", "diabetes", "sugar", "thirst", "hunger", "numbness"],
            "general": ["حرارة", "تعب", "إرهاق", "ضعف", "فقدان وزن", "fever", "fatigue", "tired", "body ache", "weakness", "weight loss"]
        }

        self.specialization_names = {
            "head": "الطب العصبي",
            "chest": "الصدرية والقلب",
            "stomach": "الجهاز الهضمي",
            "skin": "الجلدية",
            "bones": "العظام والمفاصل",
            "mental": "الصحة النفسية",
            "children": "طب الأطفال",
            "eyes": "طب العيون",
            "ent": "أنف وأذن وحنجرة",
            "dental": "طب الأسنان",
            "urinary": "المسالك البولية",
            "diabetes": "الغدد الصماء والسكري",
            "general": "الطب العام"
        }

        self.urgency_keywords = {
            "high": ["شديد", "قوي", "حادث", "لا استطيع", "لا اقدر", "موت", "اختناق", "نزيف", "غيبوبة", "emergency", "severe", "critical", "cant breathe", "unconscious", "bleeding heavily", "dying"],
            "medium": ["متوسط", "مستمر", "متكرر", "منتظم", "moderate", "persistent", "worsening", "constant", "frequent"],
            "low": ["خفيف", "بسيط", "عارض", "mild", "slight", "minor", "occasional", "temporary"]
        }

        # قاعدة معرفية للظروف الموسمية
        self.seasonal_conditions = {
            1: ["انفلونزا", "زكام", "التهاب رئوي", "flu", "cold", "pneumonia"],
            2: ["انفلونزا", "حساسية الربيع", "flu", "spring allergy"],
            3: ["حساسية الربيع", "ربو موسمي", "spring allergy", "seasonal asthma"],
            4: ["حساسية الربيع", "spring allergy"],
            5: ["ضربة شمس", "جفاف", "heat stroke", "dehydration"],
            6: ["ضربة شمس", "جفاف", "تسمم غذائي", "heat stroke", "dehydration", "food poisoning"],
            7: ["ضربة شمس", "جفاف", "تسمم غذائي", "heat stroke", "dehydration", "food poisoning"],
            8: ["ضربة شمس", "جفاف", "heat stroke", "dehydration"],
            9: ["حساسية الخريف", "fall allergy"],
            10: ["انفلونزا", "زكام", "flu", "cold"],
            11: ["انفلونزا", "زكام", "flu", "cold"],
            12: ["انفلونزا", "زكام", "flu", "cold"]
        }

    def predict(self, symptoms: str, body_part: Optional[str] = None) -> Dict:
        symptoms_lower = symptoms.lower()
        best_specialization = "general"
        max_score = 0

        if body_part and body_part in self.specialization_map:
            best_specialization = self.specialization_names.get(body_part, "الطب العام")
        else:
            for part, keywords in self.specialization_map.items():
                score = sum(1 for kw in keywords if kw in symptoms_lower)
                if score > max_score:
                    max_score = score
                    best_specialization = self.specialization_names.get(part, "الطب العام")

        urgency = "low"
        for u_level, keywords in self.urgency_keywords.items():
            if any(kw in symptoms_lower for kw in keywords):
                urgency = u_level
                break

        # توصية ذكية حسب الطوارئ
        if urgency == "high":
            action = "🚨 استشارة فورية أو زيارة مستشفى - لا تنتظر!"
            timeframe = "الآن - فوري"
        elif urgency == "medium":
            action = "📅 استشارة طبية في أقرب وقت (خلال 24-48 ساعة)"
            timeframe = "خلال 24 ساعة"
        else:
            action = "🏠 مراقبة منزلية واستشارة إذا استمرت الأعراض أكثر من 3 أيام"
            timeframe = "خلال 3-5 أيام"

        # فحص موسمي
        current_month = datetime.now().month
        seasonal_risks = self.seasonal_conditions.get(current_month, [])

        # ثقة محسنة
        confidence = 0.7 + (0.15 if body_part else 0) + (0.1 if max_score > 0 else 0) + (0.05 if urgency != "low" else 0)
        confidence = min(confidence, 0.95)

        return {
            "specialization": best_specialization,
            "urgency": urgency,
            "recommended_action": action,
            "timeframe": timeframe,
            "confidence": round(confidence, 2),
            "seasonal_risks": seasonal_risks,
            "body_part_matched": body_part is not None,
            "timestamp": datetime.now().isoformat()
        }

    def get_possible_conditions(self, symptoms: str, body_part: Optional[str] = None) -> List[Dict]:
        result = self.predict(symptoms, body_part)
        conditions_map = {
            "الطب العصبي": [
                {"name": "صداع توتري", "probability": "مرتفع", "treatment": "راحة، مسكنات، تجنب الإجهاد"},
                {"name": "شقيقة (صداع نصفي)", "probability": "متوسط", "treatment": "غرفة مظلمة، مسكنات خاصة، تجنب المحفزات"},
                {"name": "دوخة مرتبطة بالجيوب الأنفية", "probability": "منخفض", "treatment": "مضادات احتقان، بخاخ أنف"}
            ],
            "الصدرية والقلب": [
                {"name": "التهاب شعب هوائية حاد", "probability": "متوسط", "treatment": "مضادات حيوية، موسعات شعب"},
                {"name": "ذبحة صدرية", "probability": "منخفض", "treatment": "🚨 راجع الطوارئ فوراً"},
                {"name": "ارتجاع مريئي", "probability": "متوسط", "treatment": "مضادات حموضة، تجنب الأكل قبل النوم"}
            ],
            "الجهاز الهضمي": [
                {"name": "التهاب معدي", "probability": "مرتفع", "treatment": "سوائل، راحة، أكل خفيف"},
                {"name": "قولون عصبي", "probability": "متوسط", "treatment": "تجنب المهيجات، ألياف، بروبيوتك"},
                {"name": "تسمم غذائي", "probability": "منخفض", "treatment": "🚨 سوائل فموية، راجع طبيب إذا استمر"}
            ],
            "الجلدية": [
                {"name": "إكزيما", "probability": "متوسط", "treatment": "مرطبات، كورتيزون موضعي"},
                {"name": "حساسية جلدية", "probability": "مرتفع", "treatment": "مضاد هستامين، تجنب المسبب"},
                {"name": "صدفية", "probability": "منخفض", "treatment": "علاجات موضعية، راجع مختص"}
            ],
            "العظام والمفاصل": [
                {"name": "شد عضلي", "probability": "مرتفع", "treatment": "راحة، كمادات، مسكن"},
                {"name": "التهاب مفاصل", "probability": "متوسط", "treatment": "مسكنات، علاج طبيعي"},
                {"name": "انزلاق غضروفي", "probability": "منخفض", "treatment": "راحة تامة، راجع مختص عظام"}
            ],
            "الصحة النفسية": [
                {"name": "قلق عام", "probability": "مرتفع", "treatment": "تمارين تنفس، تأمل، استشارة نفسية"},
                {"name": "اكتئاب", "probability": "متوسط", "treatment": "استشارة نفسية، علاج سلوكي"},
                {"name": "نوبة هلع", "probability": "منخفض", "treatment": "🚨 تمارين تنفس عميق، تواصل مع مختص"}
            ],
            "طب الأطفال": [
                {"name": "التهاب حلق فيروسي", "probability": "مرتفع", "treatment": "سوائل دافئة، راحة، باراسيتامول"},
                {"name": "مغص رضيع", "probability": "متوسط", "treatment": "تدليك بطن، تجشئة، دفء"},
                {"name": "تسنين", "probability": "مرتفع", "treatment": "عضاضة باردة، جل مسكن"}
            ],
            "الطب العام": [
                {"name": "نزلة بردية", "probability": "مرتفع", "treatment": "راحة، سوائل، فيتامين C"},
                {"name": "إرهاق عام", "probability": "متوسط", "treatment": "نوم كاف، تغذية متوازنة"},
                {"name": "فقر دم", "probability": "منخفض", "treatment": "فحص دم، مكملات حديد"}
            ]
        }
        return conditions_map.get(result["specialization"], [{"name": "يجب استشارة طبية", "probability": "غير معروف", "treatment": "راجع طبيب للتشخيص"}])


class ChatBot:
    def __init__(self):
        self.context = {}  # ذاكرة المحادثة
        self.responses = {
            # ========== ترحيب ==========
            r"\b(سلام|هلا|مرحب|اهلا|hi|hello|hey|good morning|good evening)\b": {
                "response": "وعليكم السلام ورحمة الله وبركاته! 🌸\n\nأنا مساعدك الصحي الذكي. يمكنني:\n• تحليل أعراضك 🩺\n• اقتراح تخصص طبي 👨‍⚕️\n• الإجابة عن أسئلتك الصحية 💬\n• مساعدتك في استخدام التطبيق 📱\n\nكيف يمكنني خدمتك؟",
                "type": "greeting"
            },

            # ========== تغيير كلمة المرور ==========
            r"\b(كيف|طريقة|ابي|اريد|ابغى).*(تغيير|تعديل|update|change).*(مرور|باسورد|password)\b": {
                "response": "🔐 لتغيير كلمة المرور:\n1. اذهب للملف الشخصي 👤\n2. الأمان 🔒\n3. تغيير كلمة المرور\n\nأدخل كلمة المرور الحالية ثم الجديدة.\n\nنصيحة: استخدم كلمة مرور قوية (8 أحرف + رقم + رمز)",
                "type": "help"
            },

            # ========== وصفة طبية ==========
            r"\b(وصفة|وصفتي|prescription).*(لم|ما|لا|not).*(تصل|تظهر|arrive)\b": {
                "response": "📋 الوصفات تظهر في:\n• قسم الاستشارات السابقة\n• الملف الصحي > الوصفات\n\nإذا وصفت لك اليوم، قد تستغرق 15-30 دقيقة للظهور.\n\nهل ما زالت المشكلة؟ سأقوم بتنبيه فريق الدعم.",
                "type": "support",
                "create_ticket": True
            },

            # ========== إلغاء استشارة ==========
            r"\b(إلغا|cancel).*(استشار|موعد|consultation|appointment)\b": {
                "response": "❌ لإلغاء الاستشارة:\n1. اذهب للمواعيد 📅\n2. اختر الموعد المطلوب\n3. اضغط إلغاء\n\n⚠️ يمكن الإلغاء قبل ساعتين فقط من الموعد.\nبعدها: تواصل مع الطبيب مباشرة.",
                "type": "help"
            },

            # ========== باقات ==========
            r"\b(باقة|اشتراك|plan|subscription|سعر|تكلف|price|cost)\b": {
                "response": "💎 باقاتنا:\n\n🆓 الأساسية - مجانية\n  • 2 استشارة/شهر\n  • خصم 5% صيدلية\n\n⭐ الذهبية - 99 ر.س/شهر\n  • استشارات غير محدودة\n  • خصم 20%\n\n👑 البلاتينية - 249 ر.س\n  • فيديو + خصم 30%\n\n👨‍👩‍👧‍👦 العائلية - 399 ر.س\n  • 5 أفراد + طبيب أسرة\n\nأي باقة تناسبك؟",
                "type": "info"
            },

            # ========== حجز موعد ==========
            r"\b(احجز|book|حجز|موعد|appointment).*(طبيب|doctor|دكتور)\b": {
                "response": "📅 لحجز موعد:\n1. اذهب لقسم الأطباء 👨‍⚕️\n2. اختر التخصص والطبيب\n3. اختر التاريخ والوقت\n4. نوع الموعد (حضوري/فيديو)\n\n💡 يمكنك تصفية الأطباء حسب التقييم والسعر.",
                "type": "help"
            },

            # ========== طوارئ ==========
            r"\b(طوارئ|emergency|urgent|طارئ|حادث|نزيف|اختناق)\b": {
                "response": "🚨 في حالة الطوارئ:\n• اتصل فوراً: 1122 📞\n• اذهب لأقرب مستشفى 🏥\n\nلا تنتظر! الطوارئ الطبية تحتاج استجابة فورية.",
                "type": "urgent"
            },

            # ========== دواء ==========
            r"\b(دوا|علاج|medicine|medication|drug|pharmacy|صيدل)\b": {
                "response": "💊 للأدوية:\n• تصفح الصيدلية في التطبيق 🛒\n• ابحث عن الدواء بالاسم\n• أضف للسلة واطلب\n\n⚠️ لا تأخذ أي دواء بدون استشارة طبية!\n📋 راجع قاموس الأدوية للمعلومات.",
                "type": "info"
            },

            # ========== نتائج تحاليل ==========
            r"\b(نتيجة|نتائج|تحليل|lab|test result|فحص)\b": {
                "response": "🔬 نتائج التحاليل:\n• التقارير الطبية في الملف الصحي 📄\n• تستغرق 2-48 ساعة حسب نوع التحليل\n• سيصلك إشعار عند الجاهزية 🔔\n\nهل لديك رقم تحليل محدد؟",
                "type": "info"
            },

            # ========== شكر ==========
            r"\b(شكر|thanks|thank|مشكو|بارك الله|جزاك)\b": {
                "response": "العفو! 🌸\n\nسعيد بمساعدتك. أي شيء آخر تحتاجه؟",
                "type": "greeting"
            },

            # ========== وداع ==========
            r"\b(وداع|باي|bye|مع السلام|سلامه)\b": {
                "response": "في أمان الله! 👋\n\nدمت بصحة وعافية 🤍\n\nتذكر: أنا هنا دائماً لمساعدتك.",
                "type": "greeting"
            },

            # ========== أعراض عامة - تحويل للفرز ==========
            r"\b(عندي|اعاني|احس|اشعر|الم|وجع|تعبان|مرض|مریض|symptom|pain|hurt|sick)\b": {
                "response": "🩺 دعني أحلل أعراضك...\n\nالرجاء وصف:\n• الأعراض بالتفصيل\n• منذ متى بدأت؟\n• شدتها (خفيف/متوسط/شديد)\n• أي جزء من الجسم؟\n\nسأقوم بفرز حالتك وتوجيهك للتخصص المناسب.",
                "type": "triage",
                "create_ticket": False
            }
        }

        # ردود عاطفية
        self.emotional_responses = {
            "sad": "أتفهم شعورك 🤍. الصحة النفسية مهمة مثل الجسدية. هل تريد التحدث مع مختص؟",
            "angry": "أعتذر عن أي إزعاج 😔. دعني أساعدك في حل المشكلة. هل يمكنك شرح ما حدث؟",
            "worried": "القلق طبيعي، لكن دعنا نتصرف بهدوء 🧘. ما هي الأعراض بالتحديد؟",
            "happy": "جميل أن أسمع ذلك! 😊 كيف يمكنني مساعدتك اليوم؟"
        }

    def analyze_emotion(self, message: str) -> Optional[str]:
        sad_words = ["حزين", "مكتئب", "مقهور", "ضايق", "sad", "depressed", "down"]
        angry_words = ["غاضب", "معصب", "مستفز", "غبي", "سيء", "angry", "stupid", "bad"]
        worried_words = ["قلق", "خايف", "متوتر", "worried", "scared", "anxious"]
        happy_words = ["سعيد", "مبسوط", "فرحان", "happy", "glad", "great"]

        msg_lower = message.lower()
        if any(w in msg_lower for w in sad_words): return "sad"
        if any(w in msg_lower for w in angry_words): return "angry"
        if any(w in msg_lower for w in worried_words): return "worried"
        if any(w in msg_lower for w in happy_words): return "happy"
        return None

    def respond(self, message: str, user_context: Optional[Dict] = None) -> Dict:
        if user_context:
            self.context = user_context

        # تحليل المشاعر أولاً
        emotion = self.analyze_emotion(message)
        if emotion:
            return {
                "response": self.emotional_responses[emotion],
                "type": "emotional",
                "create_ticket": False
            }

        # البحث في القاعدة المعرفية
        for pattern, response_data in self.responses.items():
            if re.search(pattern, message, re.IGNORECASE):
                result = response_data.copy()
                result["timestamp"] = datetime.now().isoformat()
                return result

        # رد افتراضي مع تحويل ذكي
        return {
            "response": "شكراً لتواصلك! 🙏\n\nلم أتمكن من فهم سؤالك بشكل كامل، لكن لا تقلق:\n\n• سأقوم بتحويل سؤالك لفريق الدعم البشري 🧑‍💻\n• سيرد عليك أحد المختصين خلال 2-4 ساعات\n• يمكنك أيضاً الاتصال بنا: +967 777 123 456 📞\n\nهل تريد مساعدة في شيء آخر؟",
            "type": "escalate",
            "create_ticket": True,
            "ticket_priority": "normal",
            "timestamp": datetime.now().isoformat()
        }


class PredictionEngine:
    """محرك تنبؤات طبية متقدم"""
    
    def __init__(self):
        self.risk_factors = {
            "smoking": ["رئة", "قلب", "lung", "heart"],
            "obesity": ["سكري", "ضغط", "مفاصل", "diabetes", "pressure", "joints"],
            "family_history": ["وراثي", "genetic"],
            "age_above_50": ["قلب", "ضغط", "عظام", "heart", "pressure", "bones"]
        }
    
    def assess_risk(self, patient_data: Dict) -> Dict:
        risks = []
        score = 0
        
        if patient_data.get("smoking"):
            risks.append({"risk": "أمراض الرئة والقلب", "level": "مرتفع"})
            score += 3
        
        if patient_data.get("bmi", 0) > 30:
            risks.append({"risk": "السكري وضغط الدم", "level": "مرتفع"})
            score += 3
        
        if patient_data.get("age", 0) > 50:
            risks.append({"risk": "أمراض مزمنة", "level": "متوسط"})
            score += 2
        
        if patient_data.get("family_history"):
            risks.append({"risk": "أمراض وراثية", "level": "يحتاج فحص"})
            score += 2
        
        overall = "مرتفع" if score >= 6 else "متوسط" if score >= 3 else "منخفض"
        
        return {
            "risks": risks,
            "overall_risk": overall,
            "score": score,
            "recommendation": "فحص دوري سنوي" if score >= 3 else "فحص كل سنتين"
        }
