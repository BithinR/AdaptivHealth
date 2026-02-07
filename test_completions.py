"""
Test script to verify the completed implementations.
"""
import os
import sys
import base64
from datetime import datetime, timezone

# Set up environment
os.environ['SECRET_KEY'] = 'test_secret_key_for_development'
os.environ['PHI_ENCRYPTION_KEY'] = base64.urlsafe_b64encode(b'0' * 32).decode()
os.environ['DATABASE_URL'] = 'sqlite:///./test_completions.db'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user import User, UserRole
from app.models.auth_credential import AuthCredential
from app.models.vital_signs import VitalSignRecord
from app.models.alert import Alert, AlertType, SeverityLevel
from app.services.auth_service import AuthService
from app.schemas.vital_signs import VitalSignCreate
from app.api.vital_signs import check_vitals_for_alerts
from app.api.user import can_access_user

# Create test database
engine = create_engine('sqlite:///./test_completions.db', echo=False)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

auth_service = AuthService()

def test_alert_creation():
    """Test that alerts are created when vitals exceed thresholds."""
    print("\n=== Testing Alert Creation ===")
    
    db = SessionLocal()
    try:
        # Create test user
        user = User(
            email="test_patient@example.com",
            full_name="Test Patient",
            role=UserRole.PATIENT,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✓ Created test user: {user.user_id}")
        
        # Test high heart rate alert
        vital_data = VitalSignCreate(
            heart_rate=190,  # Above 180 threshold
            spo2=95.0,
            timestamp=datetime.now(timezone.utc)
        )
        check_vitals_for_alerts(user.user_id, vital_data)
        
        alerts = db.query(Alert).filter(
            Alert.user_id == user.user_id,
            Alert.alert_type == AlertType.HIGH_HEART_RATE.value
        ).all()
        
        assert len(alerts) > 0, "High heart rate alert not created"
        alert = alerts[0]
        assert alert.severity == SeverityLevel.CRITICAL.value
        assert "190" in alert.trigger_value
        print(f"✓ High heart rate alert created: {alert.title}")
        
        # Test low SpO2 alert
        vital_data2 = VitalSignCreate(
            heart_rate=80,
            spo2=85.0,  # Below 90% threshold
            timestamp=datetime.now(timezone.utc)
        )
        check_vitals_for_alerts(user.user_id, vital_data2)
        
        alerts2 = db.query(Alert).filter(
            Alert.user_id == user.user_id,
            Alert.alert_type == AlertType.LOW_SPO2.value
        ).all()
        
        assert len(alerts2) > 0, "Low SpO2 alert not created"
        alert2 = alerts2[0]
        assert alert2.severity == SeverityLevel.CRITICAL.value
        assert "85" in alert2.trigger_value
        print(f"✓ Low SpO2 alert created: {alert2.title}")
        
        # Test high blood pressure alert
        vital_data3 = VitalSignCreate(
            heart_rate=80,
            spo2=95.0,
            blood_pressure_systolic=170,  # Above 160 threshold
            blood_pressure_diastolic=95,
            timestamp=datetime.now(timezone.utc)
        )
        check_vitals_for_alerts(user.user_id, vital_data3)
        
        alerts3 = db.query(Alert).filter(
            Alert.user_id == user.user_id,
            Alert.alert_type == AlertType.HIGH_BLOOD_PRESSURE.value
        ).all()
        
        assert len(alerts3) > 0, "High blood pressure alert not created"
        alert3 = alerts3[0]
        assert alert3.severity == SeverityLevel.WARNING.value
        print(f"✓ High blood pressure alert created: {alert3.title}")
        
        print(f"✓ Total alerts created: {db.query(Alert).count()}")
        
    finally:
        db.close()


def test_password_reset():
    """Test password reset token generation and confirmation."""
    print("\n=== Testing Password Reset ===")
    
    db = SessionLocal()
    try:
        # Create test user with auth credentials
        user = User(
            email="reset_test@example.com",
            full_name="Reset Test User",
            role=UserRole.PATIENT,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create auth credential
        hashed_password = auth_service.hash_password("old_password123")
        auth_cred = AuthCredential(
            user_id=user.user_id,
            hashed_password=hashed_password
        )
        db.add(auth_cred)
        db.commit()
        print(f"✓ Created test user with auth credentials")
        
        # Generate reset token
        from datetime import timedelta
        reset_token = auth_service.create_access_token(
            data={"user_id": user.user_id, "type": "password_reset"},
            expires_delta=timedelta(hours=1)
        )
        print(f"✓ Generated reset token")
        
        # Decode and validate token
        payload = auth_service.decode_token(reset_token)
        assert payload is not None, "Token decode failed"
        assert payload.get("type") == "password_reset"
        assert payload.get("user_id") == user.user_id
        print(f"✓ Token validated successfully")
        
        # Update password
        new_password = "new_password456"
        new_hashed = auth_service.hash_password(new_password)
        auth_cred.hashed_password = new_hashed
        db.commit()
        print(f"✓ Password updated successfully")
        
        # Verify new password works
        assert auth_service.verify_password(new_password, auth_cred.hashed_password)
        assert not auth_service.verify_password("old_password123", auth_cred.hashed_password)
        print(f"✓ New password verified, old password rejected")
        
    finally:
        db.close()


def test_caregiver_access():
    """Test caregiver access control."""
    print("\n=== Testing Caregiver Access Control ===")
    
    db = SessionLocal()
    try:
        # Create test users
        patient = User(
            email="patient@example.com",
            full_name="Test Patient",
            role=UserRole.PATIENT,
            is_active=True
        )
        caregiver = User(
            email="caregiver@example.com",
            full_name="Test Caregiver",
            role=UserRole.CAREGIVER,
            is_active=True
        )
        clinician = User(
            email="clinician@example.com",
            full_name="Test Clinician",
            role=UserRole.CLINICIAN,
            is_active=True
        )
        admin = User(
            email="admin@example.com",
            full_name="Test Admin",
            role=UserRole.ADMIN,
            is_active=True
        )
        
        db.add_all([patient, caregiver, clinician, admin])
        db.commit()
        db.refresh(patient)
        db.refresh(caregiver)
        db.refresh(clinician)
        db.refresh(admin)
        print(f"✓ Created test users")
        
        # Test self-access
        assert can_access_user(patient, patient), "Patient should access own data"
        print(f"✓ Self-access works")
        
        # Test admin access
        assert can_access_user(admin, patient), "Admin should access patient data"
        print(f"✓ Admin access works")
        
        # Test clinician access
        assert can_access_user(clinician, patient), "Clinician should access patient data"
        print(f"✓ Clinician access works")
        
        # Test caregiver access (NEW IMPLEMENTATION)
        assert can_access_user(caregiver, patient), "Caregiver should access patient data"
        print(f"✓ Caregiver access works")
        
        # Test denied access
        another_patient = User(
            email="patient2@example.com",
            full_name="Another Patient",
            role=UserRole.PATIENT,
            is_active=True
        )
        db.add(another_patient)
        db.commit()
        db.refresh(another_patient)
        
        assert not can_access_user(patient, another_patient), "Patient should not access other patient data"
        print(f"✓ Access denial works")
        
    finally:
        db.close()


if __name__ == "__main__":
    try:
        test_alert_creation()
        test_password_reset()
        test_caregiver_access()
        
        print("\n" + "=" * 50)
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Clean up test database
        if os.path.exists('./test_completions.db'):
            os.remove('./test_completions.db')
            print("\n✓ Cleaned up test database")
