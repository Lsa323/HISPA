"""
Model classes for readmission prediction
This module contains the model classes that can be pickled and unpickled properly
"""

import re
import numpy as np

class SimpleReadmissionModel:
    """
    A simple statistical model for readmission prediction
    Based on weighted keyword analysis and statistical scoring
    """
    
    def __init__(self):
        self.complication_weights = {}
        self.stability_weights = {}
        self.word_scores = {}
        self.is_trained = False
        
        # Initialize with medical keywords and their weights
        self.complication_keywords = {
            "sepsis": 3.0, "pneumonia": 2.8, "respiratory distress": 3.2,
            "tachycardia": 2.1, "hypotension": 2.5, "acidosis": 2.7,
            "renal failure": 3.1, "stroke": 3.0, "deteriorated": 2.6,
            "cardiac arrest": 3.5, "bleeding": 2.4, "wound infection": 2.2,
            "nosocomial": 2.3, "readmitted": 2.9, "complicated": 2.0,
            "died": 3.8, "desaturation": 2.4, "reintubation": 3.0,
            "sirs": 2.6, "intubated": 2.7, "decompensated": 2.8,
            "unstable": 2.3, "fever": 1.8, "infection": 2.1,
            "critical": 2.9, "emergency": 2.4, "urgent": 2.1,
            "complication": 2.2
        }
        
        self.stability_keywords = {
            "stable": -2.5, "recovered well": -2.8, "no complications": -3.0,
            "doing well": -2.3, "uneventful": -2.6, "hemodynamically stable": -2.9,
            "clean wound": -2.1, "mobilizing": -1.9, "no signs of infection": -2.7,
            "pain controlled": -1.8, "tolerating diet": -1.6, "improved": -2.0,
            "vitals normal": -2.4, "no issue": -2.2, "healing": -2.0,
            "good": -1.7, "excellent": -2.5, "normal": -1.8,
            "satisfactory": -2.1, "discharge home": -2.3
        }
        
        # Combine all keywords with their weights
        self.word_scores = {**self.complication_keywords, **self.stability_keywords}
        self.is_trained = True
    
    def _extract_features(self, text):
        """Extract numerical features from text"""
        if not text:
            return np.array([0.0, 0.0, 0.0, 0.0])
        
        text_lower = str(text).lower()
        
        # Calculate weighted scores
        complication_score = 0.0
        stability_score = 0.0
        word_count = len(text_lower.split())
        
        for word, weight in self.word_scores.items():
            count = len(re.findall(r'\b' + re.escape(word.lower()) + r'\b', text_lower))
            if weight > 0:  # Complication keyword
                complication_score += count * weight
            else:  # Stability keyword (negative weight)
                stability_score += count * abs(weight)
        
        # Calculate additional features
        sentence_count = len(re.split(r'[.!?]+', text_lower))
        avg_word_length = np.mean([len(word) for word in text_lower.split()]) if word_count > 0 else 0
        
        return np.array([complication_score, stability_score, word_count, avg_word_length])
    
    def predict(self, texts):
        """Predict readmission risk for a list of texts"""
        if isinstance(texts, str):
            texts = [texts]
        
        predictions = []
        for text in texts:
            features = self._extract_features(text)
            complication_score, stability_score, word_count, avg_word_length = features
            
            # Calculate risk score
            if complication_score == 0 and stability_score == 0:
                risk_score = 0.5  # neutral/medium risk
            else:
                total_score = complication_score + stability_score
                risk_score = complication_score / total_score if total_score > 0 else 0.5
            
            # Convert to risk level (0=low, 1=medium, 2=high)
            if risk_score <= 0.33:
                risk_level = 0
            elif risk_score <= 0.66:
                risk_level = 1
            else:
                risk_level = 2
            
            predictions.append(risk_level)
        
        return np.array(predictions)
    
    def predict_proba(self, texts):
        """Predict probabilities for each risk class"""
        if isinstance(texts, str):
            texts = [texts]
        
        probabilities = []
        for text in texts:
            features = self._extract_features(text)
            complication_score, stability_score, word_count, avg_word_length = features
            
            # Calculate normalized risk score
            if complication_score == 0 and stability_score == 0:
                risk_score = 0.5
            else:
                total_score = complication_score + stability_score
                risk_score = complication_score / total_score if total_score > 0 else 0.5
            
            # Convert to probabilities using softmax-like function
            # Adjust scores to create probability distribution
            if risk_score <= 0.33:
                # Low risk scenario
                prob_low = 0.7 + (0.33 - risk_score) * 0.8
                prob_medium = 0.25
                prob_high = 0.05
            elif risk_score <= 0.66:
                # Medium risk scenario
                prob_low = 0.3 - (risk_score - 0.33) * 0.6
                prob_medium = 0.5 + (risk_score - 0.33) * 0.3
                prob_high = 0.2 + (risk_score - 0.33) * 0.3
            else:
                # High risk scenario
                prob_low = 0.05
                prob_medium = 0.25 - (risk_score - 0.66) * 0.4
                prob_high = 0.7 + (risk_score - 0.66) * 0.25
            
            # Normalize probabilities
            total_prob = prob_low + prob_medium + prob_high
            prob_low /= total_prob
            prob_medium /= total_prob
            prob_high /= total_prob
            
            probabilities.append([prob_low, prob_medium, prob_high])
        
        return np.array(probabilities)
    
    def fit(self, X, y):
        """Dummy fit method for compatibility"""
        # This model doesn't actually train, but we keep the interface
        self.is_trained = True
        return self