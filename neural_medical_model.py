import numpy as np
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import pickle

class MedicalNeuralNetwork:
    """شبكة عصبية للتصنيف الطبي - 30 تخصص"""
    
    def __init__(self):
        # طبقات الشبكة
        self.input_size = 100  # ميزات الأعراض
        self.hidden1_size = 64
        self.hidden2_size = 32
        self.output_size = 30  # 30 تخصص طبي
        
        # أوزان الشبكة (محاكاة شبكة مدربة)
        np.random.seed(42)
        self.W1 = np.random.randn(self.input_size, self.hidden1_size) * 0.1
        self.b1 = np.zeros((1, self.hidden1_size))
        self.W2 = np.random.randn(self.hidden1_size, self.hidden2_size) * 0.1
        self.b2 = np.zeros((1, self.hidden2_size))
        self.W3 = np.random.randn(self.hidden2_size, self.output_size) * 0.1
        self.b3 = np.zeros((1, self.output_size))
        
        # أسماء التخصصات
        self.specialties = [
            "الطب العصبي", "الصدرية والقلب", "الجهاز الهضمي", "الجلدية",
            "العظام والمفاصل", "الصحة النفسية", "طب الأطفال", "طب العيون",
            "أنف وأذن وحنجرة", "طب الأسنان", "المسالك البولية", "الغدد الصماء",
            "الكبد", "الكلى", "الأورام", "أمراض الدم", "النساء والولادة",
            "الأمراض المعدية", "الحساسية والمناعة", "التغذية العلاجية",
            "طب النوم", "علاج الألم", "الطب العام", "الطب الرياضي",
            "الطب الطبيعي", "الطب المهني", "طب المسنين", "طب الطوارئ",
            "الطب الوقائي", "الطب النفسي العصبي"
        ]
        
        # ترميز الأعراض (bag-of-words طبي)
        self.symptom_vocab = self._build_symptom_vocabulary()
        
    def _build_symptom_vocabulary(self) -> Dict[str, int]:
        """بناء قاموس الأعراض الطبية"""
        symptoms_list = [
            "صداع", "دوار", "دوخة", "غثيان", "تقيؤ", "إسهال", "إمساك",
            "حمى", "حرارة", "سعال", "كحة", "بلغم", "ضيق تنفس", "نهجان",
            "ألم صدر", "خفقان", "ألم بطن", "حرقة", "انتفاخ", "غازات",
            "طفح", "حكة", "احمرار", "تورم", "بثور", "جفاف",
            "ألم مفاصل", "ألم ظهر", "ألم رقبة", "ألم ركبة", "تيبس",
            "قلق", "توتر", "اكتئاب", "حزن", "أرق", "خوف", "هلع",
            "تعب", "إرهاق", "ضعف", "فقدان وزن", "زيادة وزن",
            "عطش", "جوع", "تبول كثير", "تنميل", "وخز",
            "ألم أذن", "طنين", "ألم حلق", "صعوبة بلع", "بحة",
            "ألم أسنان", "نزيف لثة", "تسوس", "رائحة فم",
            "حرقان بول", "دم في بول", "تكرار تبول", "سلس",
            "طفح حفاض", "مغص رضيع", "تسنين", "بكاء مستمر",
            "زغللة", "غشاوة", "دموع", "حكة عين", "احمرار عين",
            "نزيف", "كدمات", "شحوب", "دوار عند الوقوف",
            "تعرق ليلي", "فقدان شهية", "ألم عضلات", "رجفة",
            "عدم توازن", "تشنج", "صرع", "إغماء", "غيبوبة",
            "اكتئاب", "وسواس", "هلوسة", "عدوانية", "انطواء"
        ]
        return {symptom: i for i, symptom in enumerate(symptoms_list)}
    
    def _symptoms_to_vector(self, symptoms_text: str) -> np.ndarray:
        """تحويل النص إلى متجه"""
        vector = np.zeros(self.input_size)
        text_lower = symptoms_text.lower()
        for symptom, idx in self.symptom_vocab.items():
            if symptom in text_lower:
                vector[idx] = 1.0
        return vector.reshape(1, -1)
    
    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """دالة التنشيط Sigmoid"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def _relu(self, x: np.ndarray) -> np.ndarray:
        """دالة التنشيط ReLU"""
        return np.maximum(0, x)
    
    def _softmax(self, x: np.ndarray) -> np.ndarray:
        """دالة Softmax للتصنيف"""
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def predict(self, symptoms: str) -> Dict:
        """توقع التخصص الطبي باستخدام الشبكة العصبية"""
        # Forward pass
        X = self._symptoms_to_vector(symptoms)
        
        # الطبقة الأولى
        Z1 = np.dot(X, self.W1) + self.b1
        A1 = self._relu(Z1)
        
        # الطبقة الثانية
        Z2 = np.dot(A1, self.W2) + self.b2
        A2 = self._relu(Z2)
        
        # طبقة الإخراج
        Z3 = np.dot(A2, self.W3) + self.b3
        A3 = self._softmax(Z3)
        
        # الحصول على أفضل 3 توقعات
        probabilities = A3[0]
        top3_idx = np.argsort(probabilities)[-3:][::-1]
        
        predictions = []
        for idx in top3_idx:
            predictions.append({
                "specialty": self.specialties[idx],
                "confidence": round(float(probabilities[idx]) * 100, 1),
                "probability": round(float(probabilities[idx]), 4)
            })
        
        return {
            "top_prediction": predictions[0],
            "all_predictions": predictions,
            "model_type": "Neural Network (3-layer)",
            "input_features_detected": int(np.sum(X)),
            "timestamp": datetime.now().isoformat()
        }
    
    def analyze_symptoms_deep(self, symptoms: str) -> Dict:
        """تحليل عميق للأعراض"""
        X = self._symptoms_to_vector(symptoms)
        detected = []
        for symptom, idx in self.symptom_vocab.items():
            if X[0][idx] > 0:
                detected.append(symptom)
        
        return {
            "detected_symptoms": detected,
            "count": len(detected),
            "severity_score": min(len(detected) / 10 * 100, 100)
        }


class TensorFlowMedicalModel:
    """نموذج TensorFlow للتصنيف الطبي"""
    
    def __init__(self):
        try:
            import tensorflow as tf
            self.tf = tf
            self.model = self._build_tf_model()
            self.is_tf_available = True
        except ImportError:
            self.is_tf_available = False
            self.model = None
    
    def _build_tf_model(self):
        """بناء نموذج TensorFlow"""
        import tensorflow as tf
        
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(100,), name='symptom_input'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation='relu', name='hidden1'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu', name='hidden2'),
            tf.keras.layers.Dense(30, activation='softmax', name='specialty_output')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def predict(self, symptoms_vector: np.ndarray) -> Dict:
        """توقع باستخدام TensorFlow"""
        if not self.is_tf_available:
            return {"error": "TensorFlow not available", "use_fallback": True}
        
        predictions = self.model.predict(symptoms_vector, verbose=0)
        top_idx = np.argmax(predictions[0])
        
        return {
            "predicted_class": int(top_idx),
            "confidence": float(predictions[0][top_idx]),
            "all_probabilities": predictions[0].tolist(),
            "model_type": "TensorFlow Keras"
        }


class SymptomEmbeddingModel:
    """نموذج تضمين الأعراض (Word2Vec طبي)"""
    
    def __init__(self):
        self.embedding_dim = 50
        self.symptom_embeddings = {}
        self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """تهيئة تضمينات الأعراض"""
        symptoms_groups = {
            "ألم": ["صداع", "ألم صدر", "ألم بطن", "ألم ظهر", "ألم مفاصل", "ألم أسنان"],
            "تنفسي": ["سعال", "كحة", "ضيق تنفس", "بلغم", "صفير"],
            "هضمي": ["غثيان", "تقيؤ", "إسهال", "إمساك", "حرقة", "انتفاخ"],
            "جلدي": ["طفح", "حكة", "احمرار", "تورم", "بثور"],
            "نفسي": ["قلق", "توتر", "اكتئاب", "أرق", "خوف"],
            "عام": ["حمى", "تعب", "ضعف", "دوار", "فقدان وزن"]
        }
        
        np.random.seed(42)
        for group, symptoms in symptoms_groups.items():
            # إنشاء تضمين مركزي للمجموعة
            center = np.random.randn(self.embedding_dim) * 0.1
            for symptom in symptoms:
                # إضافة تشويش بسيط للتمايز
                self.symptom_embeddings[symptom] = center + np.random.randn(self.embedding_dim) * 0.02
    
    def find_similar(self, symptom: str, top_k: int = 3) -> List[Dict]:
        """البحث عن أعراض مشابهة"""
        if symptom not in self.symptom_embeddings:
            return []
        
        target_embed = self.symptom_embeddings[symptom]
        similarities = []
        
        for name, embed in self.symptom_embeddings.items():
            if name != symptom:
                similarity = np.dot(target_embed, embed) / (np.linalg.norm(target_embed) * np.linalg.norm(embed))
                similarities.append({"symptom": name, "similarity": round(float(similarity), 3)})
        
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        return similarities[:top_k]


class DeepHealthAnalyzer:
    """محلل صحي عميق - يجمع كل النماذج"""
    
    def __init__(self):
        self.neural_net = MedicalNeuralNetwork()
        self.embedding_model = SymptomEmbeddingModel()
        self.tf_model = TensorFlowMedicalModel()
    
    def comprehensive_analysis(self, symptoms: str, patient_age: int = 35, patient_gender: str = "ذكر") -> Dict:
        """تحليل شامل باستخدام جميع النماذج"""
        
        # تحليل الشبكة العصبية
        nn_result = self.neural_net.predict(symptoms)
        
        # تحليل الأعراض العميق
        deep_analysis = self.neural_net.analyze_symptoms_deep(symptoms)
        
        # البحث عن أعراض مشابهة
        similar_symptoms = []
        if deep_analysis["detected_symptoms"]:
            first_symptom = deep_analysis["detected_symptoms"][0]
            similar_symptoms = self.embedding_model.find_similar(first_symptom)
        
        # محاولة TensorFlow
        try:
            X = self.neural_net._symptoms_to_vector(symptoms)
            tf_result = self.tf_model.predict(X)
        except:
            tf_result = {"error": "TF not available"}
        
        # حساب درجة الخطورة
        severity = deep_analysis["severity_score"]
        if patient_age > 60: severity += 15
        if patient_age < 5: severity += 10
        
        risk_level = "مرتفع" if severity > 70 else "متوسط" if severity > 40 else "منخفض"
        
        return {
            "neural_network_diagnosis": nn_result,
            "deep_symptom_analysis": deep_analysis,
            "similar_symptoms": similar_symptoms,
            "tensorflow_result": tf_result,
            "risk_assessment": {
                "severity_score": round(severity, 1),
                "risk_level": risk_level,
                "age_factor": patient_age,
                "gender": patient_gender
            },
            "recommendation": self._generate_recommendation(risk_level, nn_result),
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_recommendation(self, risk_level: str, nn_result: Dict) -> str:
        if risk_level == "مرتفع":
            return f"🚨 ننصح بمراجعة {nn_result['top_prediction']['specialty']} فوراً"
        elif risk_level == "متوسط":
            return f"📅 ننصح بحجز موعد مع {nn_result['top_prediction']['specialty']} خلال 48 ساعة"
        return "🏠 مراقبة منزلية. راجع الطبيب إذا استمرت الأعراض"
