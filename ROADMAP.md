# Adaptiv Health - Development Roadmap

This document consolidates all TODO items and planned features not yet implemented.

## Outstanding Development Items

### 🚨 Alert & Notification System
**Status**: Not implemented  
**Priority**: High  
**Files affected**:
- `app/api/vital_signs.py` (lines 56, 64, 68, 120)

**Tasks**:
- [ ] Implement alert checking logic in `check_vitals_for_alerts()` function
- [ ] Create alert records in database when thresholds are exceeded
- [ ] Send push notifications to users and caregivers
- [ ] Send notifications to clinicians for high-risk patients
- [ ] Implement alert counting in vitals summary

**Acceptance Criteria**:
- Alerts trigger when HR > 180 BPM
- Alerts trigger when SpO2 < 90%
- Notifications sent within 30 seconds
- Alerts queryable via API

---

### 🔐 Email & Password Reset
**Status**: Partially implemented (API endpoints exist, but email sending disabled)  
**Priority**: High  
**Files affected**:
- `app/api/auth.py` (lines 371, 391)

**Tasks**:
- [ ] Implement email sending (currently TODO comment)
- [ ] Configure email provider (SendGrid, AWS SES, or similar)
- [ ] Validate password reset tokens
- [ ] Send password reset links to user emails
- [ ] Implement token expiration (suggest 1 hour)

**Acceptance Criteria**:
- Users receive reset email within 1 minute
- Reset link expires after 1 hour
- New password successfully updates auth_credentials

---

### 👥 Caregiver Access Control
**Status**: Role defined, but access permissions not implemented  
**Priority**: Medium  
**Files affected**:
- `app/api/user.py` (line 68)
- `app/models/user.py` (UserRole.CAREGIVER defined)

**Tasks**:
- [ ] Define caregiver-to-patient relationship table
- [ ] Implement permission checking for caregiver views
- [ ] Allow caregivers to view assigned patient data
- [ ] Restrict caregivers from viewing other patients
- [ ] Add caregiver notification preferences

**Acceptance Criteria**:
- Caregivers can see assigned patients' vitals
- Caregivers cannot see other patients
- Audit trail logs caregiver data access

---

### 📊 UI Placeholders
**Status**: Placeholder components in place, need real implementations  
**Priority**: Low-Medium  
**Files affected**:
- `mobile-app/lib/screens/home_screen.dart` (lines 273, 452)

**Tasks**:
- [ ] Replace heart rate ring with actual rendering (currently uses custom painter)
- [ ] Implement sparkline charts for vitals trends
- [ ] Add animations for real-time data updates
- [ ] Implement notification bell functionality

---

## Completed Items ✅

- [x] Critical logic error fixes (lockout time, user ID references)
- [x] API endpoint consistency (vitals submission URL)
- [x] Data validation (SpO2 range checking)
- [x] Recommendation generation logic
- [x] Security middleware configuration

---

## Notes

- Email implementation should use environment-based configuration
- Alert thresholds should be user-customizable in future
- Caregiver model requires database migration
- UI placeholders are intentional for MVP and can be upgraded incrementally
