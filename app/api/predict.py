"""
Risk prediction routes.

These endpoints use the AI model to estimate heart risk.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import logging
import time

from app.database import get_db
from app.models.user import User
from app.models.activity import ActivitySession
from app.models.risk_assessment import RiskAssessment
from app.services.ml_prediction import get_ml_service, MLPredictionService
from app.api.auth import get_current_user, get_current_doctor_user

# Logger
logger = logging.getLogger(__name__)

# Router
router = APIRouter()


# =============================================================================
# Request/Response Schemas
# =============================================================================

class RiskPredictionRequest(BaseModel):
    """Input data for risk prediction."""
    age: int = Field(..., ge=18, le=100, description="Patient age")
    baseline_hr: int = Field(..., ge=40, le=100, description="Resting heart rate")
    max_safe_hr: int = Field(..., ge=100, le=220, description="Maximum safe heart rate")
    avg_heart_rate: int = Field(..., ge=40, le=220, description="Average HR during session")
    peak_heart_rate: int = Field(..., ge=40, le=250, description="Peak HR during session")
    min_heart_rate: int = Field(..., ge=30, le=200, description="Minimum HR during session")
    avg_spo2: int = Field(..., ge=70, le=100, description="Average SpO2 during session")
    duration_minutes: int = Field(..., ge=1, le=300, description="Session duration in minutes")
    recovery_time_minutes: int = Field(..., ge=1, le=60, description="Recovery time in minutes")
    activity_type: str = Field(default="walking", description="Activity type")


class RiskPredictionResponse(BaseModel):
    """Response from risk prediction."""
    risk_score: float = Field(..., description="Risk score 0.0 to 1.0")
    risk_level: str = Field(..., description="low, moderate, or high")
    high_risk: bool = Field(..., description="True if high risk")
    confidence: float = Field(..., description="Model confidence")
    recommendation: str = Field(..., description="Safety recommendation")
    inference_time_ms: float = Field(..., description="Prediction time in ms")
    model_info: Dict[str, Any] = Field(..., description="Model details")
    features_used: Optional[Dict[str, float]] = Field(None, description="Engineered features")


# =============================================================================
# Endpoints
# =============================================================================

@router.get("/predict/status")
async def check_model_status():
    """Check if the ML model is loaded and ready."""
    try:
        service = get_ml_service()
        return {
            "status": "ready" if service.is_loaded else "not_loaded",
            "model_loaded": service.is_loaded,
            "features_count": len(service.feature_columns) if service.feature_columns else 0
        }
    except Exception as e:
        return {
            "status": "error",
            "model_loaded": False,
            "error": str(e)
        }


@router.post("/predict/risk", response_model=RiskPredictionResponse)
async def predict_risk(
    request: RiskPredictionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Predict cardiovascular risk for a workout session.
    
    It takes the user’s readings and returns a risk score and a short tip.
    The mobile app uses this to warn users during exercise.
    """
    # Load ML service
    service = get_ml_service()
    if not service.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML model not loaded. Check server logs."
        )

    # Run prediction with timing
    start_time = time.time()

    try:
        # Call MLPredictionService to:
        # 1. Engineer features from raw vitals
        # 2. Run model inference
        # 3. Map probability to risk level
        # 4. Generate text recommendation
        result = service.predict_risk(
            age=request.age,
            baseline_hr=request.baseline_hr,
            max_safe_hr=request.max_safe_hr,
            avg_heart_rate=request.avg_heart_rate,
            peak_heart_rate=request.peak_heart_rate,
            min_heart_rate=request.min_heart_rate,
            avg_spo2=request.avg_spo2,
            duration_minutes=request.duration_minutes,
            recovery_time_minutes=request.recovery_time_minutes,
            activity_type=request.activity_type
        )
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

    # Calculate inference time
    # WHY track inference time:
    # - Monitor if model slows down (memory pressure, I/O bottleneck)
    # - Alert if prediction takes >1s (indicates server issue)
    # - Mobile app uses this to show \"computing...\" vs instant response
    inference_ms = (time.time() - start_time) * 1000

    logger.info(
        f"Risk prediction for user {current_user.user_id}: "
        f"score={result['risk_score']}, level={result['risk_level']}, "
        f"time={inference_ms:.1f}ms"
    )

    return RiskPredictionResponse(
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        high_risk=result["high_risk"],
        confidence=result["confidence"],
        recommendation=result["recommendation"],
        inference_time_ms=round(inference_ms, 2),
        model_info=result["model_info"],
        features_used=result["features_used"]
    )


@router.get("/predict/user/{user_id}/risk")
async def predict_user_risk_from_latest_session(
    user_id: int,
    current_user: User = Depends(get_current_doctor_user),
    db: Session = Depends(get_db)
):
    """
    Clinicians can check a patient's latest session risk here.
    Only clinicians and admins can use it.

    ENDPOINT PURPOSE:
    - Allows healthcare providers to review patient's risk from latest session
    - Similar to predict_risk, but uses data from database instead of request body
    - Used in clinician dashboard to understand patient's recent activity risk
    
    DATA SOURCES:
    - Patient profile: age, baseline_hr, max_safe_hr (pulled from User model)
    - Latest session: avg_heart_rate, peak_heart_rate, duration, etc. (from ActivitySession table)
    - Database query: Gets most recent session for the patient from AWS RDS
    
    ACCESS CONTROL:
    - Requires get_current_doctor_user dependency (checks role = \"doctor\" or \"admin\")
    - Prevents patients from requesting predictions for other patients
    - Prevents unauthorized access to patient activity data
    
    RATIONALE FOR SEPARATE ENDPOINT:
    - Real-time predictions use /predict/risk (mobile app, inline)
    - Clinician tools use this endpoint (dashboard, patient review)
    - Decouples patient-facing real-time API from clinician tools
    
    FALLBACK STRATEGY:
    - Uses 'or' defaults for missing user fields (age || 55)
    - Prevents 500 error if patient never filled profile
    - Allows prediction even with incomplete patient data
    - Could be improved: Show warning if using defaults
    """
    # Get user
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get the most recent session for this user.
    session = db.query(ActivitySession)\
        .filter(ActivitySession.user_id == user_id)\
        .order_by(desc(ActivitySession.start_time))\
        .first()

    if not session:
        raise HTTPException(status_code=404, detail="No activity sessions found for user")

    # Load ML service
    service = get_ml_service()
    if not service.is_loaded:
        raise HTTPException(status_code=503, detail="ML model not loaded")

    # Run prediction using user profile + session data
    start_time = time.time()
    result = service.predict_risk(
        age=user.age or 55,
        baseline_hr=user.baseline_hr or 72,
        max_safe_hr=user.max_safe_hr or (220 - (user.age or 55)),
        avg_heart_rate=session.avg_heart_rate or 90,
        peak_heart_rate=session.peak_heart_rate or 120,
        min_heart_rate=session.min_heart_rate or 65,
        avg_spo2=session.avg_spo2 or 96,
        duration_minutes=session.duration_minutes or 30,
        recovery_time_minutes=session.recovery_time_minutes or 8,
        activity_type=session.activity_type or "walking"
    )
    inference_ms = (time.time() - start_time) * 1000

    return {
        "user_id": user_id,
        "user_name": user.full_name,
        "session_id": session.session_id,
        "session_date": session.start_time.isoformat() if session.start_time else None,
        "prediction": {
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "high_risk": result["high_risk"],
            "confidence": result["confidence"],
            "recommendation": result["recommendation"]
        },
        "inference_time_ms": round(inference_ms, 2)
    }

@router.get("/predict/my-risk")
async def get_my_risk_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """
    Get current patient's own risk assessment history.
    Available to all authenticated users (patients, doctors, admins).

    ENDPOINT PURPOSE:
    - Shows patient their historical risk assessments
    - Useful for tracking trends (improving or declining?)
    - Mobile app displays this in \"History\" or \"Trends\" view
    
    ACCESS CONTROL:
    - Requires authentication (get_current_user)
    - Patient only sees their own history
    - Doctors can access their patient's history via different endpoint
    - No role restriction (both patient and clinician can view their own)
    
    DATA SOURCE:
    - RiskAssessment table (database records of all risk evaluations)
    - Ordered by most recent first (assessment_date DESC)
    - Limited to last N records (default 10, configurable)
    
    RESPONSE STRUCTURE:
    - user_id: Who the assessments belong to
    - risk_assessments: Array with risk_score, risk_level, assessment_date, etc.
    - Custom recommendation: Generated from risk_level (not stored in DB)
    
    WHY GENERATE RECOMMENDATIONS HERE:
    - Recommendations may change based on updated guidelines
    - Avoids storing redundant data (can be computed from risk_level)
    - Allows updating recommendation logic without database migration
    - Each historical record shows what recommendation would be TODAY
    
    FUTURE ENHANCEMENT:
    - Could filter by date range (\"Show last month\", \"Show last 3 months\")
    - Could compute trend (Is risk improving or worsening?)
    - Could correlate with activity (Which activities cause higher risk?)
    """
    # Get user's risk assessments
    assessments = db.query(RiskAssessment)\
        .filter(RiskAssessment.user_id == current_user.user_id)\
        .order_by(desc(RiskAssessment.assessment_date))\
        .limit(limit)\
        .all()

    if not assessments:
        return {
            "user_id": current_user.user_id,
            "user_name": current_user.full_name,
            "risk_assessments": [],
            "message": "No risk assessments found yet"
        }

    def get_recommendation(risk_level: str, risk_score: float) -> str:
        """
        Generate user-facing recommendation based on risk level.
        
        DESIGN PHILOSOPHY:
        - Recommendations are ACTION-ORIENTED (what should user do?)
        - Escalate with risk level: Normal → Monitor → Concern → Emergency
        - Consistent across all APIs (same recommendation logic everywhere)
        
        WHY NOT STORE IN DATABASE:
        - Recommendations may change as medical guidelines evolve
        - Computing from risk_level is reliable (inverse operation)
        - Avoids storing redundant string data (risk_level → recommendation)
        
        RISK LEVEL THRESHOLDS:
        - \"critical\": Immediate danger, seek emergency care
        - \"high\": Concerning, contact healthcare provider
        - \"moderate\": Caution, monitor condition
        - \"low\": Normal, safe to continue
        
        These thresholds match /vitals/submit alert checking logic.
        """
        if risk_level == "critical":
            return "Seek immediate medical attention"
        elif risk_level == "high":
            return "Contact your healthcare provider today"
        elif risk_level == "moderate":
            return "Monitor your vitals closely and take it easy"
        else:
            return "Continue normal activities with regular monitoring"
    
    return {
        "user_id": current_user.user_id,
        "user_name": current_user.full_name,
        "assessment_count": len(assessments),
        "risk_assessments": [
            {
                "assessment_id": a.assessment_id,
                "risk_score": a.risk_score,
                "risk_level": a.risk_level,
                "assessment_type": a.assessment_type,
                "assessment_date": a.assessment_date.isoformat() if a.assessment_date else None,
                "confidence": a.confidence,
                "primary_concern": a.primary_concern,
                "recommendation": get_recommendation(a.risk_level, a.risk_score),
                "generated_by": a.generated_by
            }
            for a in assessments
        ]
    }