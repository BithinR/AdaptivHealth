# Adaptiv Health App - UI/UX Design Specification
## Professional, Compact, Medical-Grade Aesthetic

---

## 1. Design System Foundation

### Color Palette

#### Primary Colors
```
- Primary Blue: #0066FF (Actions, CTA buttons)
- Success Green: #00C853 (Safe zone, completed actions)
- Warning Yellow: #FFB300 (Caution, moderate alerts)
- Alert Red: #FF3B30 (Critical, dangerous levels)
- Neutral Gray: #F5F5F5 (Backgrounds)
```

#### Health Status Colors (Heart Rate Zones)
```
- Resting (50-70 BPM): #4CAF50 (Green - Safe)
- Light Activity (70-100 BPM): #8BC34A (Light Green - Safe)
- Moderate Zone (100-140 BPM): #FFC107 (Yellow - Caution)
- Hard Zone (140-170 BPM): #FF9800 (Orange - Intensive)
- Maximum (170+ BPM): #F44336 (Red - Dangerous)
```

#### Risk Level Indicators
```
- Low Risk: #4CAF50 (Green)
- Moderate Risk: #FFC107 (Yellow)
- High Risk: #FF9800 (Orange)
- Critical Risk: #F44336 (Red)
```

### Typography

#### Font Family
```
- Primary: Inter (Google Fonts) - Modern, clean, medical-grade
- Monospace: JetBrains Mono - For numeric values (HR, SpO2, BP)
```

#### Font Weights & Sizes
```
Headings:
- H1 (Screen Titles): 28px, Weight 600, Color: #212121
- H2 (Section Headers): 20px, Weight 600, Color: #424242
- H3 (Card Titles): 16px, Weight 600, Color: #212121

Body:
- Body Large: 16px, Weight 400, Color: #424242
- Body Small: 14px, Weight 400, Color: #666666
- Caption: 12px, Weight 400, Color: #999999

Numeric Values:
- Value Display: 32px, Weight 700, Monospace, Color: Risk-based
- Subtext (units): 12px, Weight 400, Color: #666666
```

### Spacing System

```
xs: 4px
sm: 8px
md: 12px
lg: 16px
xl: 24px
xxl: 32px

Standard padding: 16px (lg)
Card margins: 12px (md)
Screen padding: 16px (lg)
```

### Border Radius

```
- Cards: 12px
- Buttons: 8px
- Badge/Pills: 20px (full round for small elements)
- Input fields: 8px
```

### Shadows (Elevated Cards)

```
Subtle: elevation 2
  Box shadow: 0px 2px 4px rgba(0,0,0,0.08)

Standard: elevation 4
  Box shadow: 0px 4px 8px rgba(0,0,0,0.12)

Prominent: elevation 8
  Box shadow: 0px 8px 16px rgba(0,0,0,0.16)
```

---

## 2. Component Library

### VitalCard (Compact Vital Display)

**Usage:** Home screen, top vital signs grid
**Size:** ~80x100px each

```
┌─────────────────┐
│  ♥ HR           │  ← Icon + Label (12px)
│                 │
│  105 BPM        │  ← Value (28px bold) + Unit (10px)
│  ─────          │  ← Mini trend line (last 10 readings)
│ ▁▂▃▄▃▂▁▄       │     Color-coded by zone
└─────────────────┘
```

**Properties:**
- Icon: Heart, Droplet (SpO2), Pressure (BP), etc.
- Value: Large monospace number
- Trend: Micro line chart (green=stable, yellow=trending up)
- Background: White with 1px border (#E0E0E0)
- Tap behavior: Navigate to detailed view

**Code Structure:**
```dart
VitalCard(
  icon: Icons.favorite,
  label: "Heart Rate",
  value: 105,
  unit: "BPM",
  status: VitalStatus.safe, // Controls color
  trend: [95, 98, 102, 105, 103, 106], // Last 6 readings
  onTap: () => navigateToVitalsDetail(),
)
```

### RiskBadge (Status Indicator)

**Usage:** Home screen, activity cards
**Size:** Compact indicator

```
┌─────────────────────┐
│ 🟢 Low Risk | 0.23  │  ← Icon + Level + Score (0-1)
└─────────────────────┘
```

**Properties:**
- Size options: small (24px), medium (32px), large (40px)
- Animated pulse on critical alerts
- Tooltip on hover: "Based on recent heart rate, recovery, and activity"

**Code Structure:**
```dart
RiskBadge(
  riskLevel: "moderate",
  riskScore: 0.67,
  confidence: 0.92,
  showConfidence: true,
  size: RiskBadgeSize.medium,
)
```

### RecommendationCard (Fitness Plan)

**Usage:** Fitness Plans screen, Today's Workout section
**Size:** Full width, ~120px height

```
┌─────────────────────────────────────────────────┐
│ 🚶 Light Walking  |  30 min  |  92-120 BPM      │
├─────────────────────────────────────────────────┤
│ Gentle pace to improve cardiovascular base...   │
│                                                 │
│ [Target Zone] ────────────── [Safety Notes]    │
│                              └─ Take rest breaks│
│                                                 │
│         [Start Session] [View Details]          │
└─────────────────────────────────────────────────┘
```

**Properties:**
- Activity icon (walking, running, yoga, etc.)
- Duration in minutes
- Target HR zone visual
- Brief description
- Confidence score badge (small, top-right)
- Call-to-action buttons

**Code Structure:**
```dart
RecommendationCard(
  title: "Light Walking",
  activity: ActivityType.walking,
  duration: 30,
  targetHRMin: 92,
  targetHRMax: 120,
  description: "Gentle pace to improve cardiovascular base...",
  confidence: 0.95,
  warnings: ["Take rest breaks", "Reduce if chest discomfort"],
  onStart: () => startWorkout(),
  onDetails: () => showDetails(),
)
```

### TargetZoneIndicator (Heart Rate Zone Visual)

**Usage:** Workout screens, recommendation cards, recovery analysis
**Size:** Flexible width, 60px height

```
Current: 105 BPM
┌────────────────────────────────────────┐
│ Resting  Light   Moderate  Hard  Max   │
│   0─70   70─100  100─140   140─170 170+│
│ ──────────────●─────────────────────── │
│              ↑                          │
│          Current HR                    │
│ Status: Safe Zone (Target: 92-120)     │
└────────────────────────────────────────┘
```

**Properties:**
- Color-coded zones
- Current HR position indicator
- Target zone highlighted
- Dynamic update during workouts
- Touch-enabled tooltips

**Code Structure:**
```dart
TargetZoneIndicator(
  currentHR: 105,
  targetMin: 92,
  targetMax: 120,
  zones: [
    ZoneRange(label: "Resting", min: 0, max: 70, color: Colors.green),
    ZoneRange(label: "Light", min: 70, max: 100, color: Colors.lightGreen),
    // ... more zones
  ],
  showAnimation: true,
)
```

### SessionSummaryCard (Activity Result)

**Usage:** Recovery screen, Activity history
**Size:** Full width, ~180px height

```
┌──────────────────────────────────────────────┐
│ 🚶 Walking Session  | 28 min ago             │
├──────────────────────────────────────────────┤
│ Duration: 28 min  |  Calories: 156 kcal      │
│ Avg HR: 105 BPM   |  Peak HR: 128 BPM        │
│ Recovery Score: 78/100 (Excellent)           │
│                                              │
│ Time in target zone: 82% (24 min)            │
│ Recovery time to baseline: 4 min             │
│                                              │
│ Feeling: Good → Refreshed ✓                 │
└──────────────────────────────────────────────┘
```

**Properties:**
- Activity type + duration since
- Key metrics in grid (2x2)
- Recovery score with color
- User feeling progression
- Tap to expand for full details
- Share/Export options

### AlertBanner (Notification Display)

**Usage:** Top of screen during workouts or when alerts occur
**Size:** 56px height (collapsed), full screen (expanded)

```
Collapsed:
┌────────────────────────────────────────┐
│ ⚠️ Heart Rate High | 145 BPM | Dismiss │
└────────────────────────────────────────┘

Expanded:
┌────────────────────────────────────────┐
│ ⚠️ Heart Rate High                     │
│                                        │
│ Your heart rate reached 145 BPM,       │
│ above your target zone (92-120 BPM).   │
│                                        │
│ → Slow down your pace for 2 minutes    │
│ → Take 5 deep breaths                  │
│ → Contact doctor if persistent         │
│                                        │
│ [Dismiss] [Details] [Contact Doctor]   │
└────────────────────────────────────────┘
```

**Properties:**
- Color-coded by severity (info=blue, warning=yellow, critical=red)
- Icon + message
- Auto-dismiss timing (info: 5s, warning: 15s, critical: persistent)
- Expandable for full explanation
- Action buttons

**Code Structure:**
```dart
AlertBanner(
  severity: AlertSeverity.warning,
  title: "Heart Rate High",
  message: "145 BPM - above target zone",
  expandedContent: "Detailed explanation and actions",
  actions: [
    AlertAction(label: "Dismiss", onTap: dismiss),
    AlertAction(label: "Details", onTap: showDetails),
  ],
  autoDismissAfterSeconds: 15,
)
```

### ChartCard (Trend Visualization)

**Usage:** Recovery screen, Analytics sections
**Size:** Full width, variable height based on chart

```
┌────────────────────────────────────────┐
│ Heart Rate - Last 7 Days               │
├────────────────────────────────────────┤
│                                        │
│ 150│                                   │
│    │        ╱╲       ╱╲                │
│ 100│      ╱    ╲   ╱    ╲            │
│    │    ╱        ╲╱                    │
│  50│                                   │
│    │─────────────────────────────────  │
│    │ M  T  W  T  F  S  S              │
│                                        │
│ Trend: ↑ Increasing (2% per day)      │
│ Baseline: 72 BPM  |  Avg: 98 BPM      │
└────────────────────────────────────────┘
```

**Properties:**
- Time period selector (24h, 7d, 30d, custom)
- Interactive points (tap for exact values)
- Trend indicator (up/down/stable)
- Min/max/avg annotations
- Baseline comparison line

---

## 3. Screen Layouts

### Home Screen (Redesigned)

```
┌────────────────────────────────────────┐
│ Adaptiv Health        🔔  ⚙️           │  ← Header w/ notifications
├────────────────────────────────────────┤
│ Good morning, Sarah                    │  ← Personal greeting
│ Your heart is looking good today       │
├────────────────────────────────────────┤
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐      │
│ │ ♥   │ │ O₂  │ │ BP  │ │ HRV │      │  ← Vital Signs Grid (4 cards)
│ │105  │ │100% │ │120/ │ │42   │      │
│ │BPM  │ │     │ │ 80  │ │ ms  │      │
│ │ ▂▃▄ │ │ ▄▅▆ │ │ ▃▄▅ │ │ ▅▆▇ │      │
│ └─────┘ └─────┘ └─────┘ └─────┘      │
│ Status: 🟢 Low Risk (0.23)            │  ← Risk Badge
├────────────────────────────────────────┤
│ Today's Recommendation                 │  ← Today's Workout Section
│ ┌──────────────────────────────────┐  │
│ │ 🚶 Light Walking                 │  │
│ │ 30 min | 92-120 BPM              │  │
│ │ Gentle pace for recovery...      │  │
│ │ [Start Session]                  │  │
│ └──────────────────────────────────┘  │
├────────────────────────────────────────┤
│ Quick Actions                          │  ← Action Buttons
│ ┌──────┐ ┌──────┐ ┌──────┐            │
│ │ 💬   │ │ 📞   │ │ 🎧   │            │
│ │Chat  │ │Message│ │Sounds│            │
│ └──────┘ └──────┘ └──────┘            │
├────────────────────────────────────────┤
│ Recent Activity                        │  ← Last Session Summary
│ ✓ Walking (yesterday): 28 min, 82% TZ │
│ ✓ Yoga (2 days ago): 15 min           │
├────────────────────────────────────────┤
│ 🏠 Home | 💪 Fitness | 🛡️ Recovery    │  ← Bottom Navigation
│ 💬 Health | 👤 Profile                 │
└────────────────────────────────────────┘

DESIGN PRINCIPLES:
- Compact, no wasted space
- Medical data clearly organized
- Status immediately visible
- Quick action to primary feature (workout)
- Recent activity for context
```

### Fitness Plans Screen

```
┌────────────────────────────────────────┐
│ Fitness Plans              [Filter ▼]  │
├────────────────────────────────────────┤
│ This Week's Summary                    │  ← Weekly Overview
│ ✓ 3/7 workouts completed               │
│ 📈 Consistency: Good                    │
├────────────────────────────────────────┤
│                                        │
│ TODAY                                  │  ← Today Section
│ ┌──────────────────────────────────┐  │
│ │ 🚶 Light Walking                 │  │
│ │ 30 min | 92-120 BPM              │  │
│ │ Based on your recovery status    │  │
│ │ Confidence: 95%                  │  │
│ │              [Start] [Details]   │  │
│ └──────────────────────────────────┘  │
│                                        │
│ COMING UP (Next 3 Days)                │  ← Upcoming Section
│ ┌──────────────────────────────────┐  │
│ │ Tue: 🏃 Moderate Run (30 min)    │  │
│ │      Target: 120-140 BPM         │  │
│ └──────────────────────────────────┘  │
│ ┌──────────────────────────────────┐  │
│ │ Wed: 🧘 Yoga & Breathing (20m)   │  │
│ │      Relaxation & recovery        │  │
│ └──────────────────────────────────┘  │
│ ┌──────────────────────────────────┐  │
│ │ Thu: 🚴 Cycling (40 min)         │  │
│ │      Target: 110-135 BPM         │  │
│ └──────────────────────────────────┘  │
│                                        │
│ [Customize Plan] [View Alternatives]   │  ← Bottom CTA
├────────────────────────────────────────┤
│ 🏠 Home | 💪 Fitness | 🛡️ Recovery    │
└────────────────────────────────────────┘

DESIGN PRINCIPLES:
- Clear day-by-day structure
- Action-focused design
- Start button prominent
- Alternative options visible
- Customization always available
```

### Recovery Screen (Enhanced)

```
┌────────────────────────────────────────┐
│ Recovery              Last 28 min ago  │
├────────────────────────────────────────┤
│                                        │
│ Recovery Score: 78/100 ✨              │  ← Main Metric
│ ████████░░ (Excellent)                │
│                                        │
│ Session Metrics                        │  ← Session Stats
│ ┌─────────────┬─────────────────────┐  │
│ │ Duration    │ 28 min              │  │
│ │ Avg HR      │ 105 BPM             │  │
│ │ Peak HR     │ 128 BPM             │  │
│ │ Calories    │ 156 kcal            │  │
│ │ Recovery    │ 4 min               │  │
│ │ In Zone     │ 82% (24 min)        │  │
│ └─────────────┴─────────────────────┘  │
│                                        │
│ Recovery HR Trend                      │  ← Recovery Graph
│ ┌────────────────────────────────────┐ │
│ │ 140│       Peak                    │ │
│ │    │      ╱╲                       │ │
│ │ 100│    ╱    ╲╲                    │ │
│ │    │  ╱        ╲╲                  │ │
│ │  60│────────────╲────────────────  │ │
│ │    │ 0  1  2  3  4  5  6 min      │ │
│ │    │ Recovery complete: 4 min      │ │
│ └────────────────────────────────────┘ │
│                                        │
│ Breathing Exercise                     │  ← Recovery Activities
│ ┌──────────────────────────────────┐  │
│ │ 🫁 Post-Workout Breathing       │  │
│ │ 5 min guided session             │  │
│ │ Helps stabilize heart rate       │  │
│ │              [Start Exercise]    │  │
│ └──────────────────────────────────┘  │
│                                        │
│ Daily Tips                             │  ← Health Tips
│ 💡 Stay hydrated - Drink 500ml water  │
│ 💡 Light stretching improves recovery │
│                                        │
│ How did you feel?                      │  ← Mood Check-in
│ [😊 Good] [😐 Okay] [😴 Tired]        │
├────────────────────────────────────────┤
│ 🏠 Home | 💪 Fitness | 🛡️ Recovery    │
└────────────────────────────────────────┘

DESIGN PRINCIPLES:
- Recovery score immediately visible
- Detailed metrics for understanding
- Visual trend of HR recovery
- Actionable next steps (breathing exercise)
- Mood tracking for daily insights
```

### Health Coach (Chatbot) Screen

```
┌────────────────────────────────────────┐
│ Health Coach              [i] About     │
├────────────────────────────────────────┤
│                                        │
│ Daily Briefing (Today)                 │  ← AI Summary
│ ┌──────────────────────────────────┐  │
│ │ 🟢 Your heart looks great today! │  │
│ │                                  │  │
│ │ Risk Level: Low (0.28)           │  │
│ │ Trend: Improving (↓ 12% this wk) │  │
│ │ Energy: Perfect for exercise!    │  │
│ │                                  │  │
│ │ Recommendation: Moderate workout │  │
│ │ (see Fitness Plans for details)  │  │
│ └──────────────────────────────────┘  │
│                                        │
│ Quick Questions                        │  ← Quick Actions
│ ┌──────────────────────────────────┐  │
│ │ ❓ Should I exercise today?      │  │
│ └──────────────────────────────────┘  │
│ ┌──────────────────────────────────┐  │
│ │ ❓ Why was I fatigued yesterday?  │  │
│ └──────────────────────────────────┘  │
│ ┌──────────────────────────────────┐  │
│ │ ❓ How's my recovery progressing? │  │
│ └──────────────────────────────────┘  │
│                                        │
│ Chat History                           │  ← Conversation
│ ┌──────────────────────────────────┐  │
│ │ You: What's my risk score today? │  │
│ │ Coach: Your risk level is LOW... │  │
│ │        [View Full Analysis]      │  │
│ │                                  │  │
│ │ You: Should I do cardio today?   │  │
│ │ Coach: Yes! Your recovery...     │  │
│ │        [See Recommendation]      │  │
│ └──────────────────────────────────┘  │
│                                        │
│ [Send Message] 🔤              💬     │  ← Input
├────────────────────────────────────────┤
│ 🏠 Home | 💪 Fitness | 🛡️ Recovery    │
└────────────────────────────────────────┘

DESIGN PRINCIPLES:
- AI insights at top (what you need to know)
- Quick common questions
- Conversation history visible
- Links to relevant features (Fitness Plans)
- Easy message input at bottom
```

### Messages Screen

```
┌────────────────────────────────────────┐
│ Care Team Messages          [+ New]    │
├────────────────────────────────────────┤
│                                        │
│ Active Conversations                   │  ← Care Team List
│ ┌──────────────────────────────────┐  │
│ │ 🔴 Dr. Emily Rodriguez (Cardio)  │  │
│ │ Available Now                    │  │
│ │ Last: "Continue with light..."   │  │
│ │ 2 hours ago                      │  │
│ │              [Message] [Call]    │  │
│ └──────────────────────────────────┘  │
│                                        │
│ ┌──────────────────────────────────┐  │
│ │ 🟡 Lisa Chang (Cardiac Nurse)    │  │
│ │ Busy (≈30 min response)          │  │
│ │ Last: "How are you feeling?"     │  │
│ │ Yesterday                        │  │
│ │              [Message] [Call]    │  │
│ └──────────────────────────────────┘  │
│                                        │
│ ┌──────────────────────────────────┐  │
│ │ ⚫ Dr. Amanda White (Nutritionist)│  │
│ │ Offline                          │  │
│ │ Last: "Avoid high sodium..."     │  │
│ │ 3 days ago                       │  │
│ │              [Message] [Call]    │  │
│ └──────────────────────────────────┘  │
│                                        │
├────────────────────────────────────────┤
│ 🏠 Home | 💪 Fitness | 🛡️ Recovery    │
└────────────────────────────────────────┘

CONVERSATION VIEW (Tap any clinician):

┌────────────────────────────────────────┐
│ Dr. Emily Rodriguez          [⋮]       │
│ Cardiologist | Available                │
├────────────────────────────────────────┤
│                                        │
│ 📅 Yesterday, 2:45 PM                 │  ← Timestamp
│ ┌──────────────────────────────────┐  │
│ │ Dr: Continue with light cardio   │  │
│ │     2-3x per week. Monitor HR.   │  │
│ └──────────────────────────────────┘  │
│                                        │
│ 📅 You, Today 10:15 AM                 │
│ ┌──────────────────────────────────┐  │
│ │ I did the walking session you    │  │
│ │ recommended. Heart rate stayed   │  │
│ │ in target zone! [Attach Report]  │  │
│ └──────────────────────────────────┘  │
│                                        │
│ 📅 Today, 10:32 AM                     │
│ ┌──────────────────────────────────┐  │
│ │ Excellent! Keep it up. How's     │  │
│ │ your energy level?               │  │
│ └──────────────────────────────────┘  │
│                                        │
│ ┌────────────────────────────────────┐ │
│ │ Type your message...         📎 📤 │ │  ← Input
│ └────────────────────────────────────┘ │
├────────────────────────────────────────┤
│ 🏠 Home | 💪 Fitness | 🛡️ Recovery    │
└────────────────────────────────────────┘

DESIGN PRINCIPLES:
- Care team availability visible
- Message previews show context
- Status indicators (online/busy/offline)
- Professional tone in interface
- Easy file attachment for vital reports
```

### Activity History Screen

```
┌────────────────────────────────────────┐
│ Activity History          [Filter▼][📊] │
├────────────────────────────────────────┤
│ This Month: 12 sessions | 8h 45min     │  ← Stats Summary
│ Average HR: 108 BPM | Streak: 5 days  │
├────────────────────────────────────────┤
│                                        │
│ FEBRUARY                               │  ← Month Section
│ ┌──────────────────────────────────┐  │
│ │ 15 (Today) 🚶 Walking            │  │
│ │ 28 min | ♥ 105 avg | ⭐ 78 score │  │
│ │ [Details] [Share]                │  │
│ └──────────────────────────────────┘  │
│ ┌──────────────────────────────────┐  │
│ │ 14       🚴 Cycling              │  │
│ │ 40 min | ♥ 115 avg | ⭐ 82 score │  │
│ │ [Details] [Share]                │  │
│ └──────────────────────────────────┘  │
│ ┌──────────────────────────────────┐  │
│ │ 13       🧘 Yoga                 │  │
│ │ 20 min | ♥ 85 avg  | ⭐ 88 score │  │
│ │ [Details] [Share]                │  │
│ └──────────────────────────────────┘  │
│ ┌──────────────────────────────────┐  │
│ │ 12       🏃 Running              │  │
│ │ 25 min | ♥ 128 avg | ⭐ 75 score │  │
│ │ [Details] [Share]                │  │
│ └──────────────────────────────────┘  │
│                                        │
│ JANUARY                                │  ← Previous Month
│ ┌──────────────────────────────────┐  │
│ │ 30       🚶 Walking              │  │
│ │ 28 min | ♥ 102 avg | ⭐ 81 score │  │
│ │ [Details] [Share]                │  │
│ └──────────────────────────────────┘  │
│ ... (more sessions)                    │
│                                        │
├────────────────────────────────────────┤
│ 🏠 Home | 💪 Fitness | 🛡️ Recovery    │
└────────────────────────────────────────┘

DETAIL VIEW (Tap a session):

┌────────────────────────────────────────┐
│ Walking Session          Feb 15, 2:30pm│
│ Completed ✓          [Share] [Delete]  │
├────────────────────────────────────────┤
│                                        │
│ Session Duration                       │  ← Key Stats
│ 28 minutes                             │
│                                        │
│ Heart Rate Performance                 │
│ ┌──────────────────────────────────┐  │
│ │ Current: 105 BPM                 │  │
│ │ Avg: 105 BPM | Peak: 128 BPM     │  │
│ │ Min: 92 BPM                      │  │
│ │                                  │  │
│ │ [HR Graph: Line chart showing]   │  │
│ │ [activity duration]              │  │
│ └──────────────────────────────────┘  │
│                                        │
│ Oxygen & Recovery                      │  ← Additional Metrics
│ ┌──────────────────────────────────┐  │
│ │ Avg SpO2: 98% | Min: 96%         │  │
│ │ Recovery Score: 78/100 (Excellent)   │
│ │ Time to Baseline: 4 minutes       │  │
│ └──────────────────────────────────┘  │
│                                        │
│ Performance Insights                   │  ← Analysis
│ ✓ Time in Target Zone: 82% (24 min)   │
│ ✓ Recovery Quality: Excellent          │
│ 💡 Consistent pace throughout session  │
│                                        │
│ User Feedback                          │  ← Subjective Data
│ Before: Good (😊)                      │
│ After: Refreshed (😄)                  │
│                                        │
│ Risk Assessment                        │  ← Safety
│ Session Risk: Low (0.18)               │
│ No alerts triggered ✓                  │
│                                        │
│ [Send to Doctor] [Export PDF]          │  ← Actions
├────────────────────────────────────────┤
│ 🏠 Home | 💪 Fitness | 🛡️ Recovery    │
└────────────────────────────────────────┘

DESIGN PRINCIPLES:
- Chronological organization
- Quick session previews
- Deep detail view available
- Share functionality for doctor coordination
- Performance insights highlighted
```

---

## 4. Interaction Patterns

### Loading States
```
- Pulse animation on vital cards while fetching
- Skeleton loaders for recommendation cards
- "Updating..." text in headers during sync
- Never show blank states (use placeholders)
```

### Empty States
```
For Activity History (first time):
┌────────────────────────────────────────┐
│ Start Your First Workout                │
│                                        │
│ 🏃 No activities yet                  │
│                                        │
│ Begin your fitness journey today!      │
│ Choose a recommended workout →          │
│                                        │
│ [View Fitness Plans] [Chat with Coach] │
└────────────────────────────────────────┘
```

### Error States
```
┌────────────────────────────────────────┐
│ ⚠️ Could Not Load Recommendations      │
│                                        │
│ Check your internet connection and     │
│ try again.                             │
│                                        │
│ [Retry] [Use Offline Cache]            │
│ [Contact Support]                      │
└────────────────────────────────────────┘
```

### Animations
- **Card Appearance:** Fade-in + slight scale (100ms)
- **Heart Rate Update:** Color pulse when changing zones (200ms)
- **Alert Banner:** Slide in from top (150ms)
- **Button Press:** Micro-scale (80ms)
- **Screen Transitions:** Slide from bottom (300ms)

---

## 5. Responsive Design

### Breakpoints
```
Mobile (default): 360px - 430px
Tablet: 600px+
```

### Adaptations
```
Mobile:
- Full width cards with padding
- Single column layout
- Bottom sheet for details

Tablet:
- Two-column grid for vital cards
- Side-by-side comparison charts
- Expanded navigation rail
```

---

## 6. Accessibility

### Typography Contrast
- All text: WCAG AA minimum (4.5:1 ratio)
- Critical alerts: WCAG AAA (7:1 ratio)

### Touch Targets
- Minimum 48px x 48px for all interactive elements
- Larger buttons for elderly users (option in settings)

### Color Independence
- Never rely only on color to indicate status
- Always include icons/text labels
- Example: "🟢 Low Risk" not just green

### Labels & Descriptions
- All vital cards have descriptive labels
- Buttons have descriptive text (not just icons)
- Charts have alt text descriptions
- Important numbers announced to screen readers

---

## 7. Dark Mode Support

```
Dark Mode Colors:
- Background: #121212
- Card Background: #1E1E1E
- Text Primary: #FFFFFF
- Text Secondary: #B3B3B3
- Risk Zones: Use same colors but with opacity adjustments
```

---

## 8. Implementation Notes

### Flutter Packages
```dart
- flutter_svg: For medical icons
- charts_flutter: For HR trend graphs
- intl: For date/time formatting
- provider: For state management
- dio: For API calls with retry logic
- uuid: For local data sync
```

### Custom Widgets to Build
1. `VitalCard` - Compact vital display
2. `RiskBadge` - Status indicator
3. `RecommendationCard` - Fitness plan card
4. `TargetZoneIndicator` - HR zone visualization
5. `AlertBanner` - Alert notification
6. `SessionSummaryCard` - Activity result
7. `ChartCard` - Time series visualization

### State Management Pattern
```
Provider pattern:
- VitalSignsProvider: Real-time vital data
- RecommendationProvider: Fitness suggestions
- ActivityProvider: Session history
- AlertProvider: Alert management
- MessagingProvider: Chat history
```

---

## Success Criteria

✓ All screens load in < 1.5 seconds
✓ Vital signs update every 10 seconds (when active)
✓ No card or component exceeds 120px height unless expanded
✓ WCAG 2.1 AA accessibility compliance
✓ Zepp-comparable aesthetics and compact design
✓ All backend data types properly displayed
✓ Smooth animations (60 FPS)
✓ Offline functionality for cached data

---

**Design Document Version:** 1.0
**Created:** February 15, 2026
**Designed for:** Adaptiv Health Patient App (Flutter)
**Target Devices:** iOS 14+, Android 10+
