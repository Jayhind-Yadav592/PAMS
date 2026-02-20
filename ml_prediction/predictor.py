"""
ML Prediction Module
Predicts passport processing time for new applications
"""

import pickle
import os
from pathlib import Path
from datetime import datetime


def load_model():
    """Load trained ML model"""
    model_path = Path(__file__).parent / 'models' / 'passport_model.pkl'
    
    if not model_path.exists():
        print(f"⚠️  Model not found at: {model_path}")
        print("   Please run: python ml_prediction/train_model.py")
        return None
    
    try:
        with open(model_path, 'rb') as f:
            model_package = pickle.load(f)
        return model_package
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None


def predict_processing_time(application_type, city, state=None, workload=None):
    """
    Predict processing time for an application
    
    Args:
        application_type: 'new', 'renewal', or 'reissue'
        city: City name
        state: State name (optional)
        workload: Current pending applications count (optional)
    
    Returns:
        int: Predicted processing days
    """
    # Load model
    model_package = load_model()
    
    if model_package is None:
        # Fallback to rule-based prediction
        defaults = {'new': 30, 'renewal': 20, 'reissue': 25}
        return defaults.get(application_type, 30)
    
    # Extract components
    model = model_package['model']
    type_mapping = model_package['type_mapping']
    city_mapping = model_package['city_mapping']
    state_mapping = model_package.get('state_mapping', {})
    
    # Encode inputs
    type_encoded = type_mapping.get(application_type, 0)
    city_encoded = city_mapping.get(city, 0)
    state_encoded = state_mapping.get(state, 0) if state else 0
    month = datetime.now().month
    workload_val = workload if workload else 200
    
    # Prepare features
    features = [[type_encoded, city_encoded, state_encoded, month, workload_val]]
    
    # Predict
    predicted_days = model.predict(features)[0]
    
    # Round and ensure minimum
    predicted_days = max(int(predicted_days), 15)
    
    return predicted_days


def predict_for_application(application):
    """
    Predict processing time for Django Application model instance
    
    Args:
        application: Application model instance
    
    Returns:
        int: Predicted processing days
    """
    # Get current workload
    try:
        from applications.models import Application
        workload = Application.objects.filter(
            current_status__in=['submitted', 'document_verification', 'police_verification']
        ).count()
    except:
        workload = 200
    
    # Predict
    predicted_days = predict_processing_time(
        application_type=application.application_type,
        city=application.city,
        state=application.state,
        workload=workload
    )
    
    return predicted_days


if __name__ == '__main__':
    # Test predictions
    print("🧪 Testing ML Predictor...")
    print("=" * 50)
    
    test_cases = [
        {'type': 'new', 'city': 'Mumbai', 'state': 'Maharashtra', 'workload': 150},
        {'type': 'renewal', 'city': 'Delhi', 'state': 'Delhi', 'workload': 300},
        {'type': 'reissue', 'city': 'Bangalore', 'state': 'Karnataka', 'workload': 100},
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}:")
        print(f"   Type: {test['type']}")
        print(f"   City: {test['city']}")
        print(f"   Workload: {test['workload']}")
        
        days = predict_processing_time(
            test['type'],
            test['city'],
            test['state'],
            test['workload']
        )
        
        print(f"   ⏱️  Predicted: {days} days")
    
    print("\n" + "=" * 50)
    print("✅ Testing complete!")
