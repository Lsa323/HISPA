from flask import Flask, render_template, request, jsonify
import joblib
import os
import numpy as np
from model_classes import SimpleReadmissionModel

app = Flask(__name__)

class ReadmissionPredictor:
    def __init__(self, model_path='readmission_model.pkl'):
        self.model_path = model_path
        self.model = None
        self.risk_labels = ['Faible', 'Moyen', 'Élevé']
        self.risk_colors = ['low-risk', 'medium-risk', 'high-risk']
        self.load_model()
    
    def load_model(self):
        """Load the trained model"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                print(f"✅ Model loaded successfully from {self.model_path}")
            else:
                print(f"❌ Model file not found: {self.model_path}")
                print("Please run 'python train_model.py' first to create the model.")
                self.model = None
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
    
    def predict_readmission(self, text):
        """Predict readmission risk using the trained model"""
        if not text or text.strip() == "":
            return {
                'risk_level': 1,
                'risk_label': 'Moyen',
                'probability': 0.5,
                'explanation': 'Aucun texte fourni pour l\'analyse',
                'confidence': 0.5,
                'model_used': 'default'
            }
        
        if self.model is None:
            # Fallback to keyword-based prediction if model not available
            return self._fallback_prediction(text)
        
        try:
            # Use the trained model for prediction
            prediction = self.model.predict([text])[0]
            probabilities = self.model.predict_proba([text])[0]
            
            risk_level = int(prediction)
            risk_label = self.risk_labels[risk_level]
            confidence = float(probabilities[risk_level])
            
            # Generate explanation based on probabilities
            prob_text = []
            for i, prob in enumerate(probabilities):
                if prob > 0.1:  # Only show probabilities > 10%
                    prob_text.append(f"{self.risk_labels[i]}: {prob:.1%}")
            
            explanation = f"Prédiction basée sur l'analyse ML. Probabilités: {', '.join(prob_text)}"
            
            return {
                'risk_level': risk_level,
                'risk_label': risk_label,
                'probability': confidence,
                'explanation': explanation,
                'confidence': confidence,
                'model_used': 'trained_ml',
                'probabilities': {
                    'low': float(probabilities[0]),
                    'medium': float(probabilities[1]),
                    'high': float(probabilities[2])
                }
            }
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            return self._fallback_prediction(text)
    
    def _fallback_prediction(self, text):
        """Fallback keyword-based prediction when model is not available"""
        complication_keywords = [
            "sepsis", "pneumonia", "respiratory distress", "tachycardia", "hypotension",
            "acidosis", "renal failure", "stroke", "deteriorated", "cardiac arrest",
            "bleeding", "wound infection", "nosocomial", "readmitted", "complicated", "died",
            "desaturation", "reintubation", "sirs", "intubated", "decompensated", "unstable",
            "fever", "infection", "critical", "emergency", "urgent", "complication"
        ]
        
        stability_keywords = [
            "stable", "recovered well", "no complications", "doing well", "uneventful",
            "hemodynamically stable", "clean wound", "mobilizing", "no signs of infection",
            "pain controlled", "tolerating diet", "improved", "vitals normal", "no issue",
            "healing", "good", "excellent", "normal", "satisfactory", "discharge home"
        ]
        
        def count_keywords(text, keywords):
            if not text or text.strip() == "":
                return 0
            text_lower = text.lower()
            return sum(1 for kw in keywords if kw.lower() in text_lower)
        
        comp_count = count_keywords(text, complication_keywords)
        stab_count = count_keywords(text, stability_keywords)
        total = comp_count + stab_count
        
        if total == 0:
            risk_level = 1
            risk_label = 'Moyen'
            probability = 0.5
            explanation = 'Analyse par mots-clés: Aucun indicateur spécifique détecté'
        else:
            comp_percentage = comp_count / total
            if comp_percentage <= 0.33:
                risk_level = 0
                risk_label = 'Faible'
                probability = comp_percentage
                explanation = f'Analyse par mots-clés: Plus d\'indicateurs de stabilité ({stab_count}) que de complications ({comp_count})'
            elif comp_percentage <= 0.66:
                risk_level = 1
                risk_label = 'Moyen'
                probability = comp_percentage
                explanation = f'Analyse par mots-clés: Indicateurs mixtes - {comp_count} complications, {stab_count} stabilité'
            else:
                risk_level = 2
                risk_label = 'Élevé'
                probability = comp_percentage
                explanation = f'Analyse par mots-clés: Plus d\'indicateurs de complications ({comp_count}) que de stabilité ({stab_count})'
        
        return {
            'risk_level': risk_level,
            'risk_label': risk_label,
            'probability': probability,
            'explanation': explanation,
            'confidence': probability,
            'model_used': 'fallback_keywords',
            'complication_count': comp_count,
            'stability_count': stab_count
        }

# Initialize the predictor
predictor = ReadmissionPredictor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        result = predictor.predict_readmission(text)
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/model-status')
def model_status():
    """Endpoint to check if the model is loaded"""
    return jsonify({
        'model_loaded': predictor.model is not None,
        'model_path': predictor.model_path,
        'model_exists': os.path.exists(predictor.model_path)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)