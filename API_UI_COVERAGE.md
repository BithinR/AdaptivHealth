# API ↔ UI Coverage Audit

> **Generated:** June 2025
> **Scope:** Backend API (FastAPI), Web Dashboard (React), Mobile Patient App (Flutter)

---

## A. Backend API Inventory

All paths are relative to the `/api/v1` prefix unless otherwise noted.

### A1. Authentication

| Method | Path | Auth | Role | Description |
|--------|------|:----:|------|-------------|
| POST | `/register` | — | — | Create new account |
| POST | `/login` | — | — | Obtain JWT token pair |
| POST | `/refresh` | — | — | Refresh access token |
| GET | `/me` | ✔ | Any | Return current user profile |
| POST | `/reset-password` | — | — | Request password-reset email |
| POST | `/reset-password/confirm` | — | — | Complete password reset |

### A2. User Management (`/users`)

| Method | Path | Auth | Role | Description |
|--------|------|:----:|------|-------------|
| GET | `/users/me` | ✔ | Any | Get own profile |
| PUT | `/users/me` | ✔ | Any | Update own profile |
| PUT | `/users/me/medical-history` | ✔ | Any | Update own medical history |
| GET | `/users/` | ✔ | Clinician+ | List all users |
| GET | `/users/{user_id}` | ✔ | Clinician+ | Get user by ID |
| PUT | `/users/{user_id}` | ✔ | Admin | Update any user |
| POST | `/users/` | ✔ | Admin | Create user (admin-provisioned) |
| DELETE | `/users/{user_id}` | ✔ | Admin | Delete user |
| GET | `/users/{user_id}/medical-history` | ✔ | Clinician+ | View patient medical history |

### A3. Vital Signs

| Method | Path | Auth | Role | Description |
|--------|------|:----:|------|-------------|
| POST | `/vitals` | ✔ | Any | Submit vital signs |
| POST | `/vitals/batch` | ✔ | Any | Submit batch vitals |
| GET | `/vitals/latest` | ✔ | Any | Get own latest vitals |
| GET | `/vitals/summary` | ✔ | Any | Get own vitals summary |
| GET | `/vitals/history` | ✔ | Any | Get own vitals history |
| GET | `/vitals/user/{user_id}/latest` | ✔ | Clinician+ | Get patient latest vitals |
| GET | `/vitals/user/{user_id}/summary` | ✔ | Clinician+ | Get patient vitals summary |
| GET | `/vitals/user/{user_id}/history` | ✔ | Clinician+ | Get patient vitals history |

### A4. Activities

| Method | Path | Auth | Role | Description |
|--------|------|:----:|------|-------------|
| POST | `/activities/start` | ✔ | Any | Start activity session |
| POST | `/activities/end/{session_id}` | ✔ | Any | End activity session |
| GET | `/activities` | ✔ | Any | List own activities |
| GET | `/activities/user/{user_id}` | ✔ | Clinician+ | List patient activities |
| GET | `/activities/{session_id}` | ✔ | Any | Get activity by ID |

### A5. Alerts

| Method | Path | Auth | Role | Description |
|--------|------|:----:|------|-------------|
| GET | `/alerts` | ✔ | Any | List own alerts |
| PATCH | `/alerts/{alert_id}/acknowledge` | ✔ | Any | Acknowledge alert |
| PATCH | `/alerts/{alert_id}/resolve` | ✔ | Any | Resolve alert |
| POST | `/alerts` | ✔ | Any | Create alert |
| GET | `/alerts/user/{user_id}` | ✔ | Clinician+ | List patient alerts |
| GET | `/alerts/stats` | ✔ | Clinician+ | Alert statistics |

### A6. AI Risk Prediction

| Method | Path | Auth | Role | Description |
|--------|------|:----:|------|-------------|
| GET | `/predict/status` | — | — | ML model health check |
| POST | `/predict/risk` | ✔ | Any | Run risk prediction |
| GET | `/predict/user/{user_id}/risk` | ✔ | Clinician+ | Get patient risk prediction |
| GET | `/predict/my-risk` | ✔ | Any | Get own risk prediction |
| POST | `/risk-assessments/compute` | ✔ | Any | Compute own risk assessment |
| POST | `/patients/{user_id}/risk-assessments/compute` | ✔ | Clinician+ | Compute patient risk assessment |
| GET | `/risk-assessments/latest` | ✔ | Any | Get own latest risk assessment |
| GET | `/patients/{user_id}/risk-assessments/latest` | ✔ | Clinician+ | Get patient risk assessment |
| GET | `/recommendations/latest` | ✔ | Any | Get own latest recommendations |
| GET | `/patients/{user_id}/recommendations/latest` | ✔ | Clinician+ | Get patient recommendations |

### A7. Advanced ML

| Method | Path | Auth | Role | Description |
|--------|------|:----:|------|-------------|
| GET | `/anomaly-detection` | ✔ | Any | Detect anomalies in vitals |
| GET | `/trend-forecast` | ✔ | Any | Forecast vitals trends |
| GET | `/baseline-optimization` | ✔ | Any | Get optimized baseline |
| POST | `/baseline-optimization/apply` | ✔ | Any | Apply baseline |
| GET | `/recommendation-ranking` | ✔ | Any | Rank recommendations |
| POST | `/recommendation-ranking/outcome` | ✔ | Any | Report recommendation outcome |
| POST | `/alerts/natural-language` | ✔ | Any | Generate NL alert |
| GET | `/risk-summary/natural-language` | ✔ | Any | NL risk summary |
| GET | `/model/retraining-status` | ✔ | Clinician+ | Model retraining status |
| GET | `/model/retraining-readiness` | ✔ | Clinician+ | Model retraining readiness |
| POST | `/predict/explain` | ✔ | Any | Explainability for prediction |

**Total endpoints: 55**

---

## B. Frontend Usage Matrix

✅ = called from at least one page &nbsp; ⬜ = wrapper exists but unused &nbsp; — = no wrapper

| Backend Endpoint | Mobile App | Web Dashboard |
|------------------|:----------:|:-------------:|
| **Authentication** | | |
| POST `/register` | ✅ register_screen | ✅ RegisterPage |
| POST `/login` | ✅ login_screen | ✅ LoginPage |
| POST `/refresh` | — | — |
| GET `/me` | ✅ home_screen, profile_screen | ✅ LoginPage, DashboardPage |
| POST `/reset-password` | — | — |
| POST `/reset-password/confirm` | — | — |
| **User Management** | | |
| GET `/users/me` | ✅ (via getCurrentUser) | ✅ (via getCurrentUser) |
| PUT `/users/me` | ✅ profile_screen | ⬜ wrapper only |
| PUT `/users/me/medical-history` | — | — |
| GET `/users/` | — | ✅ DashboardPage, PatientsPage |
| GET `/users/{user_id}` | — | ✅ PatientDetailPage |
| PUT `/users/{user_id}` | — | — |
| POST `/users/` | — | — |
| DELETE `/users/{user_id}` | — | — |
| GET `/users/{user_id}/medical-history` | — | — |
| **Vital Signs** | | |
| POST `/vitals` | ⬜ wrapper only | ⬜ wrapper only |
| POST `/vitals/batch` | — | — |
| GET `/vitals/latest` | ✅ home_screen | ⬜ wrapper only |
| GET `/vitals/summary` | — | ✅ DashboardPage |
| GET `/vitals/history` | ⬜ wrapper only | ⬜ wrapper only |
| GET `/vitals/user/{id}/latest` | — | ✅ PatientDetailPage |
| GET `/vitals/user/{id}/summary` | — | ⬜ wrapper only |
| GET `/vitals/user/{id}/history` | — | ✅ PatientDetailPage |
| **Activities** | | |
| POST `/activities/start` | ✅ workout_screen | ⬜ wrapper only |
| POST `/activities/end/{id}` | ✅ workout_screen | ⬜ wrapper only |
| GET `/activities` | ✅ history_screen | ⬜ wrapper only |
| GET `/activities/user/{user_id}` | — | ✅ PatientDetailPage |
| GET `/activities/{session_id}` | ⬜ wrapper only | ⬜ wrapper only |
| **Alerts** | | |
| GET `/alerts` | — | ✅ DashboardPage |
| PATCH `/alerts/{id}/acknowledge` | — | ⬜ wrapper only |
| PATCH `/alerts/{id}/resolve` | — | ⬜ wrapper only |
| POST `/alerts` | — | — |
| GET `/alerts/user/{user_id}` | — | ✅ PatientDetailPage |
| GET `/alerts/stats` | — | ✅ DashboardPage |
| **Risk / Predictions** | | |
| GET `/predict/status` | — | — |
| POST `/predict/risk` | ✅ home_screen | ⬜ wrapper only |
| GET `/predict/user/{id}/risk` | — | — |
| GET `/predict/my-risk` | — | — |
| POST `/risk-assessments/compute` | — | ⬜ wrapper only |
| POST `/patients/{id}/risk-assessments/compute` | — | ⬜ wrapper only |
| GET `/risk-assessments/latest` | — | ⬜ wrapper only |
| GET `/patients/{id}/risk-assessments/latest` | — | ✅ PatientDetailPage |
| GET `/recommendations/latest` | ⬜ wrapper only | ⬜ wrapper only |
| GET `/patients/{id}/recommendations/latest` | — | ✅ PatientDetailPage |
| **Advanced ML** | | |
| GET `/anomaly-detection` | — | — |
| GET `/trend-forecast` | — | — |
| GET `/baseline-optimization` | — | — |
| POST `/baseline-optimization/apply` | — | — |
| GET `/recommendation-ranking` | — | — |
| POST `/recommendation-ranking/outcome` | — | — |
| POST `/alerts/natural-language` | — | — |
| GET `/risk-summary/natural-language` | — | — |
| GET `/model/retraining-status` | — | — |
| GET `/model/retraining-readiness` | — | — |
| POST `/predict/explain` | — | — |

**Coverage summary:**

| | Endpoints Used | Wrapper Only | No Wrapper |
|---|:-:|:-:|:-:|
| Mobile App | 9 | 4 | 42 |
| Web Dashboard | 15 | 14 | 26 |

---

## C. Client API Wrapper Methods

### C1. Web Dashboard (`api.ts`)

| Wrapper Method | Backend Endpoint | Called From Page? |
|----------------|------------------|:-:|
| `login()` | POST `/login` | ✅ LoginPage |
| `register()` | POST `/register` | ✅ RegisterPage |
| `getCurrentUser()` | GET `/users/me` | ✅ LoginPage, DashboardPage |
| `updateCurrentUserProfile()` | PUT `/users/me` | ❌ |
| `getAllUsers()` | GET `/users/` | ✅ DashboardPage, PatientsPage |
| `getUserById()` | GET `/users/{id}` | ✅ PatientDetailPage |
| `getLatestVitalSigns()` | GET `/vitals/latest` | ❌ |
| `getLatestVitalSignsForUser()` | GET `/vitals/user/{id}/latest` | ✅ PatientDetailPage |
| `getVitalSignsHistory()` | GET `/vitals/history` | ❌ |
| `getVitalSignsHistoryForUser()` | GET `/vitals/user/{id}/history` | ✅ PatientDetailPage |
| `getVitalSignsSummary()` | GET `/vitals/summary` | ✅ DashboardPage |
| `getVitalSignsSummaryForUser()` | GET `/vitals/user/{id}/summary` | ❌ |
| `submitVitalSigns()` | POST `/vitals` | ❌ |
| `getLatestRiskAssessment()` | GET `/risk-assessments/latest` | ❌ |
| `getLatestRiskAssessmentForUser()` | GET `/patients/{id}/risk-assessments/latest` | ✅ PatientDetailPage |
| `computeRiskAssessment()` | POST `/risk-assessments/compute` | ❌ |
| `computeRiskAssessmentForUser()` | POST `/patients/{id}/risk-assessments/compute` | ❌ |
| `predictRisk()` | POST `/predict/risk` | ❌ |
| `getLatestRecommendation()` | GET `/recommendations/latest` | ❌ |
| `getLatestRecommendationForUser()` | GET `/patients/{id}/recommendations/latest` | ✅ PatientDetailPage |
| `getRecommendations()` | GET `/recommendations` | ❌ |
| `getRecommendationById()` | GET `/recommendations/{id}` | ❌ |
| `updateRecommendation()` | PATCH `/recommendations/{id}` | ❌ |
| `getAlerts()` | GET `/alerts` | ✅ DashboardPage |
| `getAlertsForUser()` | GET `/alerts/user/{id}` | ✅ PatientDetailPage |
| `getAlertStats()` | GET `/alerts/stats` | ✅ DashboardPage |
| `acknowledgeAlert()` | PATCH `/alerts/{id}/acknowledge` | ❌ |
| `resolveAlert()` | PATCH `/alerts/{id}/resolve` | ❌ |
| `getActivities()` | GET `/activities` | ❌ |
| `getActivitiesForUser()` | GET `/activities/user/{id}` | ✅ PatientDetailPage |
| `getActivityById()` | GET `/activities/{id}` | ❌ |
| `startActivity()` | POST `/activities/start` | ❌ |
| `endActivity()` | POST `/activities/end/{id}` | ❌ |
| `updateActivity()` | PATCH `/activities/{id}` | ❌ |
| `getHealth()` | GET `/health` | ❌ |
| `getDatabaseHealth()` | GET `/health/db` | ❌ |

**Used: 15 / 36** — 21 wrappers are defined but never called from any page.

### C2. Mobile App (`api_client.dart`)

| Wrapper Method | Backend Endpoint | Called From Screen? |
|----------------|------------------|:-:|
| `login()` | POST `/login` | ✅ login_screen |
| `register()` | POST `/register` | ✅ register_screen |
| `logout()` | — (local token clear) | ❌ |
| `getCurrentUser()` | GET `/users/me` | ✅ profile_screen, home_screen |
| `updateProfile()` | PUT `/users/me` | ✅ profile_screen |
| `getLatestVitals()` | GET `/vitals/latest` | ✅ home_screen |
| `getVitalHistory()` | GET `/vitals/history` | ❌ |
| `submitVitalSigns()` | POST `/vitals` | ❌ |
| `predictRisk()` | POST `/predict/risk` | ✅ home_screen |
| `startSession()` | POST `/activities/start` | ✅ workout_screen |
| `endSession()` | POST `/activities/end/{id}` | ✅ workout_screen |
| `getActivities()` | GET `/activities` | ✅ history_screen |
| `getActivityById()` | GET `/activities/{id}` | ❌ |
| `getRecommendation()` | GET `/recommendations/latest` | ❌ |

**Used: 9 / 14** — 5 wrappers are defined but never called from any screen.

---

## D. Gaps & Decisions

### D1. Missing UI for Existing Backend Features

| # | Gap | Impact | Priority |
|---|-----|--------|----------|
| 1 | **No password-reset UI.** Backend exposes `POST /reset-password` and `POST /reset-password/confirm`, but neither client has a "Forgot Password" flow. | Users cannot self-service password resets. | High |
| 2 | **No admin user-creation page.** `POST /users/` (admin-only) exists but the web dashboard has no Admin → Create User screen. | Admins must use raw API or scripts to onboard patients. | High |
| 3 | **No UI for alert acknowledge/resolve.** Dashboard lists alerts but has no buttons wired to `PATCH /alerts/{id}/acknowledge` or `/resolve`. | Clinicians cannot manage alert lifecycle from the UI. | Medium |
| 4 | **No medical-history UI.** `PUT /users/me/medical-history` and `GET /users/{id}/medical-history` have no frontend consumer. | Medical history intake requires manual API calls. | Medium |
| 5 | **Advanced ML endpoints have zero frontend consumers.** All 11 endpoints (anomaly detection, trend forecast, NL alerts, explainability, etc.) are backend-only. | Planned Phase C / Phase D features with no UI yet. | Low (future) |

### D2. Auth & Security Gaps

| # | Gap | Impact | Priority |
|---|-----|--------|----------|
| 6 | **No logout endpoint on backend.** Both clients clear the local token but do not invalidate it server-side. Token remains valid until expiry. | Stolen tokens cannot be revoked. | Medium |
| 7 | **No refresh-token retry logic.** Neither client intercepts 401 responses to transparently refresh the access token. Users are logged out on token expiry. | Poor UX — sessions expire silently. | Medium |
| 8 | **RBAC not fully enforced.** Backend role decorators (`get_current_doctor_user`, `get_current_admin_user`) exist but there is no middleware preventing a patient from accessing PHI endpoints beyond the decorator check. Dashboard has no role-based routing — all roles see the same navigation. | A patient logging into the dashboard sees the clinician view. | High |

### D3. Client Design Issues

| # | Gap | Impact | Priority |
|---|-----|--------|----------|
| 9 | **Mobile app exposes a registration screen.** Per requirements, patient accounts should be provisioned by an admin — the self-registration screen should be removed or gated behind an admin flow. | Patients could create unmanaged accounts. | Medium |
| 10 | **Dashboard has no role-based routing.** A patient and a clinician both land on the same dashboard. There is no conditional navigation based on user role. | Patients see admin/clinician-level data and navigation. | High |
| 11 | **21 unused wrappers in `api.ts`.** Methods like `submitVitalSigns`, `startActivity`, `endActivity`, `computeRiskAssessment`, `acknowledgeAlert`, `resolveAlert`, and others are defined but never invoked. | Dead code increases maintenance burden. These should be wired to UI or pruned. | Low |
| 12 | **5 unused wrappers in `api_client.dart`.** `getVitalHistory`, `submitVitalSigns`, `getActivityById`, `getRecommendation`, and `logout` are defined but not called. | Same as above. | Low |

### D4. Missing Backend Endpoints

| # | Gap | Details |
|---|-----|---------|
| 13 | **No `POST /logout` or token-blacklist endpoint.** | Needed for secure session termination. |
| 14 | **No consent/data-sharing workflow.** | No endpoints for patients to grant/revoke data-sharing permissions to clinicians. Required for HIPAA / privacy compliance. |
| 15 | **`updateActivity` wrapper calls `PATCH /activities/{id}` but no such endpoint exists on the backend.** | The `api.ts` wrapper targets a route the server does not serve — will always 404/405. |
| 16 | **`getRecommendations` and `getRecommendationById` wrappers call `GET /recommendations` and `GET /recommendations/{id}` — no matching backend routes.** | Same as above — dead wrappers pointing at non-existent endpoints. |

### D5. Summary Heatmap

```
                         Mobile App    Web Dashboard
Authentication              ██████        ██████
User Management              ███           █████
Vital Signs                  ███           █████
Activities                   ████          ██
Alerts                                     ████
Risk / Predictions           ██            ███
Advanced ML
Medical History
Password Reset
Admin User Mgmt
Consent / Sharing
```

_Filled blocks (█) indicate relative coverage depth. Empty rows = no frontend coverage._

---

## Appendix: Page → API Call Map

### Web Dashboard

| Page | API Calls |
|------|-----------|
| **LoginPage** | `login()`, `getCurrentUser()` |
| **RegisterPage** | `register()` |
| **DashboardPage** | `getCurrentUser()`, `getAllUsers()`, `getAlertStats()`, `getAlerts()`, `getVitalSignsSummary()` |
| **PatientsPage** | `getAllUsers()` |
| **PatientDetailPage** | `getUserById()`, `getLatestVitalSignsForUser()`, `getVitalSignsHistoryForUser()`, `getActivitiesForUser()`, `getAlertsForUser()`, `getLatestRiskAssessmentForUser()`, `getLatestRecommendationForUser()` |

### Mobile App

| Screen | API Calls |
|--------|-----------|
| **login_screen** | `login()` |
| **register_screen** | `register()` |
| **home_screen** | `getLatestVitals()`, `getCurrentUser()`, `predictRisk()` |
| **workout_screen** | `startSession()`, `endSession()` |
| **profile_screen** | `getCurrentUser()`, `updateProfile()` |
| **history_screen** | `getActivities()` |
| **recovery_screen** | _(no API calls — static UI)_ |
