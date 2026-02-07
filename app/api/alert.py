"""
Alert API endpoints.

Manages health alerts and warnings for cardiac patients.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from typing import Optional
from datetime import datetime, timedelta, timezone
import logging

from app.database import get_db
from app.models.user import User
from app.models.alert import Alert
from app.schemas.alert import (
    AlertCreate,
    AlertUpdate,
    AlertResponse,
    AlertListResponse
)
from app.api.auth import get_current_user, get_current_doctor_user

logger = logging.getLogger(__name__)
router = APIRouter()


# =============================================================================
# Alert Deduplication Helper
# =============================================================================

def check_duplicate_alert(
    db: Session,
    user_id: int,
    alert_type: str,
    window_minutes: int = 5
) -> bool:
    """
    Check if a similar alert was created recently (within window_minutes).
    
    Prevents alert spam from triggering multiple notifications for the same issue.
    
    Args:
        db: Database session
        user_id: User ID
        alert_type: Type of alert to check
        window_minutes: Time window in minutes (default 5)
        
    Returns:
        True if duplicate exists, False otherwise
    """
    since = datetime.now(timezone.utc) - timedelta(minutes=window_minutes)
    
    existing = db.query(Alert).filter(
        and_(
            Alert.user_id == user_id,
            Alert.alert_type == alert_type,
            Alert.created_at >= since
        )
    ).first()
    
    return existing is not None


# =============================================================================
# Patient Endpoints
# =============================================================================

@router.get("/alerts", response_model=AlertListResponse)
async def get_my_alerts(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    acknowledged: Optional[bool] = Query(None),
    severity: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's alerts.
    
    Returns paginated list of alerts with optional filtering.
    """
    query = db.query(Alert).filter(Alert.user_id == current_user.user_id)
    
    # Apply filters
    if acknowledged is not None:
        query = query.filter(Alert.acknowledged == acknowledged)
    
    if severity:
        query = query.filter(Alert.severity == severity)
    
    # Count total for pagination
    total = query.count()
    
    # Get paginated results
    alerts = query.order_by(desc(Alert.created_at))\
                  .offset((page - 1) * per_page)\
                  .limit(per_page)\
                  .all()
    
    return AlertListResponse(
        alerts=[AlertResponse.model_validate(alert) for alert in alerts],
        total=total,
        page=page,
        per_page=per_page
    )


@router.patch("/alerts/{alert_id}/acknowledge", response_model=AlertResponse)
async def acknowledge_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Acknowledge an alert.
    
    Marks the alert as read/acknowledged by the user.
    """
    alert = db.query(Alert).filter(
        Alert.alert_id == alert_id,
        Alert.user_id == current_user.user_id
    ).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    alert.acknowledged = True
    alert.updated_at = datetime.now(timezone.utc)  # type: ignore
    
    db.commit()
    db.refresh(alert)
    
    logger.info(f"Alert {alert_id} acknowledged by user {current_user.user_id}")
    
    return alert


@router.patch("/alerts/{alert_id}/resolve", response_model=AlertResponse)
async def resolve_alert(
    alert_id: int,
    update_data: AlertUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Resolve an alert with optional notes.
    
    Marks alert as resolved and records resolution details.
    """
    alert = db.query(Alert).filter(
        Alert.alert_id == alert_id,
        Alert.user_id == current_user.user_id
    ).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    # Update fields
    if update_data.acknowledged is not None:
        alert.acknowledged = update_data.acknowledged
    
    if update_data.resolved_at:
        alert.resolved_at = update_data.resolved_at
    else:
        alert.resolved_at = datetime.now(timezone.utc)
    
    if update_data.resolved_by:
        alert.resolved_by = str(update_data.resolved_by)  # type: ignore
    else:
        alert.resolved_by = str(current_user.user_id)  # type: ignore
    
    if update_data.resolution_notes:
        alert.resolution_notes = update_data.resolution_notes
    
    alert.updated_at = datetime.now(timezone.utc)  # type: ignore
    
    db.commit()
    db.refresh(alert)
    
    logger.info(f"Alert {alert_id} resolved by user {current_user.user_id}")
    
    return alert


@router.post("/alerts", response_model=AlertResponse)
async def create_alert(
    alert_data: AlertCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new alert.
    
    Includes deduplication to prevent alert spam.
    """
    # Check for duplicate within 5-minute window
    if check_duplicate_alert(db, alert_data.user_id, alert_data.alert_type):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Similar alert already exists within the last 5 minutes"
        )
    
    alert = Alert(
        user_id=alert_data.user_id,
        alert_type=alert_data.alert_type,
        severity=alert_data.severity,
        message=alert_data.message,
        title=alert_data.title,
        action_required=alert_data.action_required,
        trigger_value=alert_data.trigger_value,
        threshold_value=alert_data.threshold_value
    )
    
    db.add(alert)
    db.commit()
    db.refresh(alert)
    
    logger.info(f"Alert created: {alert.alert_id} for user {alert_data.user_id}")
    
    return alert


# =============================================================================
# Clinician Endpoints
# =============================================================================

@router.get("/alerts/user/{user_id}", response_model=AlertListResponse)
async def get_user_alerts(
    user_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    acknowledged: Optional[bool] = Query(None),
    severity: Optional[str] = Query(None),
    current_user: User = Depends(get_current_doctor_user),
    db: Session = Depends(get_db)
):
    """
    Get alerts for a specific user.
    
    Clinician/Admin access only.
    """
    query = db.query(Alert).filter(Alert.user_id == user_id)
    
    # Apply filters
    if acknowledged is not None:
        query = query.filter(Alert.acknowledged == acknowledged)
    
    if severity:
        query = query.filter(Alert.severity == severity)
    
    # Count total for pagination
    total = query.count()
    
    # Get paginated results
    alerts = query.order_by(desc(Alert.created_at))\
                  .offset((page - 1) * per_page)\
                  .limit(per_page)\
                  .all()
    
    return AlertListResponse(
        alerts=[AlertResponse.model_validate(alert) for alert in alerts],
        total=total,
        page=page,
        per_page=per_page
    )


@router.get("/alerts/stats")
async def get_alert_statistics(
    days: int = Query(7, ge=1, le=90),
    current_user: User = Depends(get_current_doctor_user),
    db: Session = Depends(get_db)
):
    """
    Get alert statistics across all users.
    
    Admin/Clinician access only. Used for dashboard metrics.
    """
    since = datetime.now(timezone.utc) - timedelta(days=days)
    
    # Count alerts by severity
    from sqlalchemy import func
    severity_counts = db.query(
        Alert.severity,
        func.count(Alert.alert_id).label('count')
    ).filter(
        Alert.created_at >= since
    ).group_by(Alert.severity).all()
    
    # Count unacknowledged alerts
    unacknowledged = db.query(func.count(Alert.alert_id)).filter(
        and_(
            Alert.created_at >= since,
            Alert.acknowledged == False
        )
    ).scalar()
    
    return {
        "period_days": days,
        "severity_breakdown": {
            severity: count for severity, count in severity_counts
        },
        "unacknowledged_count": unacknowledged,
        "generated_at": datetime.now(timezone.utc).isoformat()
    }
