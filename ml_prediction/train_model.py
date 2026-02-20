#!/usr/bin/env python3
"""
Machine Learning Model Training Script
Trains a Random Forest model for passport processing time prediction
"""

import os
import sys
import numpy as np
import pandas as pd
import pickle
from pathlib import Path

# Check if sklearn is available
try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
except ImportError:
    print("❌ scikit-learn not installed!")
    print("Run: pip install scikit-learn pandas numpy")
    sys.exit(1)


def generate_training_data(n_samples=1000):
    """Generate synthetic training data"""
    print(f"📊 Generating {n_samples} training samples...")
    
    np.random.seed(42)
    
    app_types = ['new', 'renewal', 'reissue']
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']
    states = ['Maharashtra', 'Delhi', 'Karnataka', 'Telangana', 'Tamil Nadu', 'West Bengal', 'Maharashtra', 'Gujarat']
    
    data = {
        'application_type': np.random.choice(app_types, n_samples),
        'city': np.random.choice(cities, n_samples),
        'state': np.random.choice(states, n_samples),
        'month': np.random.randint(1, 13, n_samples),
        'workload': np.random.randint(50, 500, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Calculate processing days based on logic
    base_days = {'new': 30, 'renewal': 20, 'reissue': 25}
    df['processing_days'] = df['application_type'].map(base_days)
    df['processing_days'] += (df['workload'] / 50).astype(int)
    df['processing_days'] += np.random.randint(-5, 10, n_samples)
    df['processing_days'] = df['processing_days'].clip(lower=15)  # Minimum 15 days
    
    print(f"✅ Generated {len(df)} samples")
    return df


def prepare_features(df):
    """Encode categorical variables"""
    print("🔧 Preparing features...")
    
    # Create mappings
    type_map = {t: i for i, t in enumerate(df['application_type'].unique())}
    city_map = {c: i for i, c in enumerate(df['city'].unique())}
    state_map = {s: i for i, s in enumerate(df['state'].unique())}
    
    # Encode
    df['type_encoded'] = df['application_type'].map(type_map)
    df['city_encoded'] = df['city'].map(city_map)
    df['state_encoded'] = df['state'].map(state_map)
    
    # Features and target
    X = df[['type_encoded', 'city_encoded', 'state_encoded', 'month', 'workload']]
    y = df['processing_days']
    
    print("✅ Features prepared")
    return X, y, type_map, city_map, state_map


def train_model(X, y):
    """Train Random Forest model"""
    print("🤖 Training Random Forest model...")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"📈 Training R² Score: {train_score:.4f}")
    print(f"📈 Testing R² Score: {test_score:.4f}")
    
    # Sample predictions
    sample_pred = model.predict(X_test[:5])
    sample_actual = y_test.iloc[:5].values
    
    print("\n🔍 Sample Predictions:")
    for i, (pred, actual) in enumerate(zip(sample_pred, sample_actual), 1):
        print(f"   Sample {i}: Predicted={pred:.0f} days, Actual={actual} days")
    
    return model


def save_model(model, type_map, city_map, state_map):
    """Save trained model and mappings"""
    print("\n💾 Saving model...")
    
    # Create models directory
    models_dir = Path('ml_prediction/models')
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # Package everything
    model_package = {
        'model': model,
        'type_mapping': type_map,
        'city_mapping': city_map,
        'state_mapping': state_map,
        'version': '1.0',
    }
    
    # Save
    model_path = models_dir / 'passport_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model_package, f)
    
    print(f"✅ Model saved to: {model_path}")
    print(f"   File size: {model_path.stat().st_size / 1024:.2f} KB")


def main():
    """Main training pipeline"""
    print("=" * 60)
    print("🚀 PASSPORT PROCESSING TIME PREDICTION - MODEL TRAINING")
    print("=" * 60)
    print()
    
    try:
        # Generate data
        df = generate_training_data(n_samples=1000)
        
        # Prepare features
        X, y, type_map, city_map, state_map = prepare_features(df)
        
        # Train model
        model = train_model(X, y)
        
        # Save model
        save_model(model, type_map, city_map, state_map)
        
        print("\n" + "=" * 60)
        print("✅ MODEL TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\n📌 Next Steps:")
        print("   1. Model is ready to use")
        print("   2. Run migrations: python manage.py migrate")
        print("   3. Start server: python manage.py runserver")
        
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
