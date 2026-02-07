# Flutter AI Integration Guide

## Overview
This guide shows how to integrate the new AI risk assessment and recommendation features into your Flutter app.

## Files Created

### Core
- `lib/core/token_storage.dart` - Secure token storage
- `lib/core/api_client.dart` - Dio HTTP client with auto Bearer token

### AI Features
- `lib/features/ai/ai_api.dart` - AI endpoint calls
- `lib/features/ai/ai_store.dart` - State management for AI data

### Screens
- `lib/screens/ai_home_screen.dart` - Home screen with risk display
- `lib/screens/ai_plan_screen.dart` - Exercise recommendation screen

### Main
- `lib/main_with_ai.dart` - Example main.dart with AI integration

## Setup Steps

### 1. Install Dependencies

The following packages have been added to `pubspec.yaml`:
```yaml
dependencies:
  dio: ^5.4.0                       # Already added
  flutter_secure_storage: ^9.0.0   # NEW - Secure token storage
  provider: ^6.1.0                  # Already added
```

Run:
```bash
cd mobile-app
flutter pub get
```

### 2. Configure Backend URL

Edit `lib/main_with_ai.dart` and update this line:
```dart
baseUrl: 'http://YOUR_IP:8000/api/v1', // <-- UPDATE THIS
```

Replace `YOUR_IP` with:
- Your computer's local IP (e.g., `192.168.1.100`)
- Or `localhost` if testing on emulator
- Or your production domain

### 3. Update Login Screen

Make sure your login screen saves the token after successful login:

```dart
// After successful login
final tokenStorage = TokenStorage();
await tokenStorage.saveToken(response['access_token']);
```

### 4. Switch to AI Main

Option A: Replace your current main.dart with the AI version:
```bash
# Backup current main
cp lib/main.dart lib/main_old.dart

# Use new AI version
cp lib/main_with_ai.dart lib/main.dart
```

Option B: Gradually integrate by copying the provider setup from `main_with_ai.dart` into your existing `main.dart`.

## Using the AI Features

### Home Screen Flow

1. **User opens app** → `AiHomeScreen` loads
2. **initState()** → Calls `loadHome()` to fetch:
   - Latest vitals
   - Latest risk assessment
   - Latest recommendation
3. **Display cards** → Shows vitals and risk with drivers
4. **Compute button** → User taps "Compute AI Now"
5. **Backend processes** → Analyzes last 30 min of vitals
6. **Results update** → Risk and recommendation refresh

### Key Methods

From `AiStore`:
- `loadHome()` - Load all data on screen open
- `computeAiAndRefresh()` - Trigger new risk assessment

### Error Handling

The app handles these errors gracefully:
- **404** - No data yet (prompts to submit vitals)
- **401** - Session expired (prompts to login)
- **Network errors** - Shows retry button

## API Endpoints Used

### GET /vitals/latest
Returns user's most recent vital signs reading.

**Response:**
```json
{
  "heart_rate": 75,
  "spo2": 98,
  "systolic_bp": 120,
  "diastolic_bp": 80,
  "timestamp": "2026-02-08T10:30:00Z"
}
```

### POST /risk-assessments/compute
Computes risk assessment from last 30 minutes of vitals.

**Response:**
```json
{
  "assessment_id": 123,
  "user_id": 1,
  "risk_score": 0.25,
  "risk_level": "low",
  "confidence": 0.92,
  "inference_time_ms": 45.2,
  "drivers": [
    "Vitals are within expected safe limits."
  ],
  "based_on": {
    "window_minutes": 30,
    "points": 12,
    "activity_type": "walking"
  }
}
```

### GET /risk-assessments/latest
Returns user's most recent risk assessment.

**Response:**
```json
{
  "assessment_id": 123,
  "user_id": 1,
  "risk_score": 0.25,
  "risk_level": "low",
  "confidence": 0.92,
  "assessment_date": "2026-02-08T10:35:00Z",
  "drivers": [
    "Vitals are within expected safe limits."
  ]
}
```

### GET /recommendations/latest
Returns user's most recent exercise recommendation.

**Response:**
```json
{
  "recommendation_id": 456,
  "user_id": 1,
  "title": "Continue Safe Training",
  "suggested_activity": "Walking / Light cardio",
  "intensity_level": "moderate",
  "duration_minutes": 20,
  "target_heart_rate_min": 87,
  "target_heart_rate_max": 117,
  "description": "You are in a safe zone. Keep steady effort and stay hydrated.",
  "warnings": "Monitor for symptoms. Avoid sudden spikes in intensity.",
  "created_at": "2026-02-08T10:35:00Z"
}
```

## Customization

### Change Risk Card Colors

Edit `ai_home_screen.dart`:
```dart
// Add color based on risk level
Color _getRiskColor(String level) {
  switch (level.toLowerCase()) {
    case 'critical':
    case 'high':
      return Colors.red;
    case 'moderate':
      return Colors.orange;
    default:
      return Colors.green;
  }
}
```

### Add Animations

Add `animated_text_kit` package and animate risk score changes.

### Persist Data Locally

Use `shared_preferences` to cache the latest data when offline.

## Troubleshooting

### "No data yet" Error
**Cause:** No vitals have been submitted.
**Fix:** Submit at least one vital sign reading via POST /vitals.

### "Session expired" Error
**Cause:** Token is invalid or expired.
**Fix:** User needs to login again.

### API Not Responding
**Cause:** Backend server not running or wrong URL.
**Fix:** 
1. Check backend is running: `uvicorn app.main:app --reload`
2. Verify base URL in main.dart
3. Check firewall settings

### Field Name Mismatches
**Cause:** Backend returns different field names than expected.
**Fix:** Update parsing in `_VitalsCard` and `_RiskCard` to match your actual API response.

## Next Steps

1. **Test the flow:**
   - Login
   - Submit some vitals
   - Tap "Compute AI Now"
   - View risk drivers
   - Check recommendation

2. **Enhance UI:**
   - Add charts for risk history
   - Color-code risk levels
   - Add success animations

3. **Add features:**
   - Push notifications for high risk
   - Share recommendations with clinician
   - Track compliance with plan

## Support

If you encounter issues:
1. Check backend logs for API errors
2. Use Flutter DevTools to inspect network calls
3. Verify token is being sent in Authorization header
4. Test endpoints in Swagger UI first
