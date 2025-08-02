#!/usr/bin/env python3
"""
Create and save the readmission prediction model
"""

import joblib
from model_classes import SimpleReadmissionModel

def create_and_save_model():
    """Create and save the simple model"""
    print("Creating simple readmission prediction model...")
    
    # Create model
    model = SimpleReadmissionModel()
    
    # Test the model
    test_texts = [
        "Patient stable, no complications, vitals normal, doing well",
        "Some complications noted, patient under observation, stable overall", 
        "Sepsis developed, respiratory distress, critical condition, intensive care needed"
    ]
    
    predictions = model.predict(test_texts)
    probabilities = model.predict_proba(test_texts)
    
    risk_labels = ['Low Risk', 'Medium Risk', 'High Risk']
    
    print("\nModel Testing:")
    for i, text in enumerate(test_texts):
        pred_label = risk_labels[predictions[i]]
        max_prob = max(probabilities[i])
        print(f"\nText: {text[:50]}...")
        print(f"Prediction: {pred_label} (confidence: {max_prob:.2f})")
        print(f"Probabilities: Low={probabilities[i][0]:.2f}, Medium={probabilities[i][1]:.2f}, High={probabilities[i][2]:.2f}")
    
    # Save model
    model_filename = 'readmission_model.pkl'
    joblib.dump(model, model_filename)
    print(f"\n✅ Model saved as: {model_filename}")
    
    return model

if __name__ == "__main__":
    print("Creating Readmission Prediction Model")
    print("=" * 50)
    
    try:
        model = create_and_save_model()
        print("\n" + "=" * 50)
        print("✅ Model creation completed successfully!")
        print("You can now use the Flask app with the trained model.")
        
    except Exception as e:
        print(f"❌ Error during model creation: {e}")
        raise