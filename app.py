from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

class ReadmissionPredictor:
    def __init__(self):
        self.complication_keywords = [
            "sepsis", "pneumonia", "respiratory distress", "tachycardia", "hypotension",
            "acidosis", "renal failure", "stroke", "deteriorated", "cardiac arrest",
            "bleeding", "wound infection", "nosocomial", "readmitted", "complicated", "died",
            "desaturation", "reintubation", "sirs", "intubated", "decompensated", "unstable",
            "fever", "infection", "critical", "emergency", "urgent", "complication"
        ]
        
        self.stability_keywords = [
            "stable", "recovered well", "no complications", "doing well", "uneventful",
            "hemodynamically stable", "clean wound", "mobilizing", "no signs of infection",
            "pain controlled", "tolerating diet", "improved", "vitals normal", "no issue",
            "healing", "good", "excellent", "normal", "satisfactory", "discharge home"
        ]
    
    def count_keywords(self, text, keywords):
        """Count occurrences of keywords in text"""
        if not text or text.strip() == "":
            return 0
        text_lower = text.lower()
        return sum(1 for kw in keywords if kw.lower() in text_lower)
    
    def predict_readmission(self, text):
        """Predict readmission risk based on text analysis"""
        if not text or text.strip() == "":
            return {
                'risk_level': 1,
                'risk_label': 'Moyen',
                'probability': 0.5,
                'explanation': 'Aucun texte fourni pour l\'analyse'
            }
        
        comp_count = self.count_keywords(text, self.complication_keywords)
        stab_count = self.count_keywords(text, self.stability_keywords)
        total = comp_count + stab_count
        
        if total == 0:
            risk_level = 1  # Medium risk by default
            risk_label = 'Moyen'
            probability = 0.5
            explanation = 'Aucun indicateur spécifique détecté'
        else:
            comp_percentage = comp_count / total
            if comp_percentage <= 0.33:
                risk_level = 0  # Low risk
                risk_label = 'Faible'
                probability = comp_percentage
                explanation = f'Plus d\'indicateurs de stabilité ({stab_count}) que de complications ({comp_count})'
            elif comp_percentage <= 0.66:
                risk_level = 1  # Medium risk
                risk_label = 'Moyen'
                probability = comp_percentage
                explanation = f'Indicateurs mixtes: {comp_count} complications, {stab_count} stabilité'
            else:
                risk_level = 2  # High risk
                risk_label = 'Élevé'
                probability = comp_percentage
                explanation = f'Plus d\'indicateurs de complications ({comp_count}) que de stabilité ({stab_count})'
        
        return {
            'risk_level': risk_level,
            'risk_label': risk_label,
            'probability': probability,
            'explanation': explanation,
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)