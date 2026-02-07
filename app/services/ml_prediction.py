"""
Machine learning helper.

This loads the trained model and returns a risk score.
"""

import pickle
import json
import logging
import os
from typing import Optional, Dict, Any

# Logger setup
logger = logging.getLogger(__name__)

# ---- Path to Massoud's trained model files ----
# These files are from the Adaptiv/Adaptiv folder
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ml_models")
MODEL_PATH = os.path.join(MODEL_DIR, "risk_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
FEATURES_PATH = os.path.join(MODEL_DIR, "feature_columns.json")


class MLPredictionService:
    """
    Uses the trained model to estimate heart risk.
    It turns raw readings into a risk score and a simple recommendation.
    """

    def __init__(self):
        """Initialize the service and load model files."""
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self._loaded = False

    def load_model(self) -> bool:
        """
        Load the model files from disk.

        Returns:
            True if successful, False on any file/parsing error
        """
        try:
            # Load pre-trained Random Forest model
            # WHY pickle: Model was trained in Python, pickle preserves all state
            with open(MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)
            logger.info(f"Loaded model from {MODEL_PATH}")

            # Load feature scaler (StandardScaler or similar)
            # WHY: Tree models don't need scaling, but other models might
            # Loaded for future compatibility if model architecture changes
            with open(SCALER_PATH, 'rb') as f:
                self.scaler = pickle.load(f)
            logger.info(f"Loaded scaler from {SCALER_PATH}")

            # Load feature column names
            # WHY: Model expects 17 features in specific order
            # Loading from JSON makes it easy to change without code edits
            with open(FEATURES_PATH, 'r') as f:
                self.feature_columns = json.load(f)
            logger.info(f"Loaded {len(self.feature_columns)} feature columns")

            self._loaded = True
            return True

        except FileNotFoundError as e:
            # Model files not found - likely first deployment
            # User should copy ml_models/ folder from training repo
            logger.error(f"Model file not found: {e}")
            logger.error(f"Expected files in: {MODEL_DIR}")
            logger.error("Copy risk_model.pkl, scaler.pkl, feature_columns.json to ml_models/")
            return False
        except Exception as e:
            # Unexpected error (corrupted file, wrong format, etc.)
            logger.error(f"Failed to load ML model: {e}")
            return False

    @property
    def is_loaded(self) -> bool:
        """Check if the model is loaded and ready."""
        return self._loaded

    def engineer_features(
        self,
        age: int,
        baseline_hr: int,
        max_safe_hr: int,
        avg_heart_rate: int,
        peak_heart_rate: int,
        min_heart_rate: int,
        avg_spo2: int,
        duration_minutes: int,
        recovery_time_minutes: int,
        activity_type: str = "walking"
    ) -> Dict[str, float]:
        """
        Turn raw readings into the features the model expects.
        This gives the model enough context to judge risk.

        Returns dict of feature_name -> value.
        """
        # Build the feature values the model expects.
        hr_pct_of_max = peak_heart_rate / max_safe_hr if max_safe_hr > 0 else 0
        hr_elevation = avg_heart_rate - baseline_hr
        hr_range = peak_heart_rate - min_heart_rate
        duration_intensity = duration_minutes * hr_pct_of_max
        recovery_efficiency = recovery_time_minutes / duration_minutes if duration_minutes > 0 else 0
        spo2_deviation = 98 - avg_spo2
        age_risk_factor = age / 70

        # Activity type encoding (same mapping as train_model.py)
        activity_mapping = {
            'walking': 1, 'yoga': 1,
            'jogging': 2, 'cycling': 2,
            'swimming': 3
        }
        activity_intensity = activity_mapping.get(activity_type, 2)

        return {
            'age': age,
            'baseline_hr': baseline_hr,
            'max_safe_hr': max_safe_hr,
            'avg_heart_rate': avg_heart_rate,
            'peak_heart_rate': peak_heart_rate,
            'min_heart_rate': min_heart_rate,
            'avg_spo2': avg_spo2,
            'duration_minutes': duration_minutes,
            'recovery_time_minutes': recovery_time_minutes,
            'hr_pct_of_max': hr_pct_of_max,
            'hr_elevation': hr_elevation,
            'hr_range': hr_range,
            'duration_intensity': duration_intensity,
            'recovery_efficiency': recovery_efficiency,
            'spo2_deviation': spo2_deviation,
            'age_risk_factor': age_risk_factor,
            'activity_intensity': activity_intensity
        }

    def predict_risk(
        self,
        age: int,
        baseline_hr: int,
        max_safe_hr: int,
        avg_heart_rate: int,
        peak_heart_rate: int,
        min_heart_rate: int,
        avg_spo2: int,
        duration_minutes: int,
        recovery_time_minutes: int,
        activity_type: str = "walking"
    ) -> Dict[str, Any]:
        """
        Predict heart risk for a workout session.
        Returns a score, a label, and a simple recommendation.
        """
        if not self._loaded:
            raise RuntimeError("ML model not loaded. Call load_model() first.")

        # Step 1: build the features from the raw readings.
        features = self.engineer_features(
            age, baseline_hr, max_safe_hr,
            avg_heart_rate, peak_heart_rate, min_heart_rate,
            avg_spo2, duration_minutes, recovery_time_minutes,
            activity_type
        )

        # Step 2: put features in the exact order the model expects.
        import numpy as np
        feature_array = np.array([[features[col] for col in self.feature_columns]])

        # Step 3: scale values if needed.
        feature_scaled = self.scaler.transform(feature_array)

        # Step 4: ask the model for a prediction.
        prediction = self.model.predict(feature_scaled)[0]  # 0 or 1
        probabilities = self.model.predict_proba(feature_scaled)[0]  # [prob_low, prob_high]

        # Step 5: turn the score into a simple risk label.
        risk_score = float(probabilities[1])  # probability of high risk class

        if risk_score >= 0.80:
            # High risk.
            risk_level = "high"
            recommendation = "STOP activity immediately. Rest and monitor symptoms."
        elif risk_score >= 0.50:
            # Medium risk.
            risk_level = "moderate"
            recommendation = "Reduce intensity. Consider taking a break."
        else:
            # Low risk.
            risk_level = "low"
            recommendation = "Safe to continue at current intensity."

        return {
            "risk_score": round(risk_score, 4),
            "risk_level": risk_level,
            "high_risk": bool(prediction == 1),
            "confidence": round(float(max(probabilities)), 4),
            "features_used": features,
            "recommendation": recommendation,
            "model_info": {
                "name": "RandomForest",
                "version": "1.0",
                "accuracy": "96.9%"
            }
        }



# ---- Singleton instance ----
ml_service = MLPredictionService()


def get_ml_service() -> MLPredictionService:
    """Get the ML prediction service, loading model if needed."""
    if not ml_service.is_loaded:
        ml_service.load_model()
    return ml_service
