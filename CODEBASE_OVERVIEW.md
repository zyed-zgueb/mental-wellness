# Serene - Mental Wellness AI Companion: Comprehensive Architecture Overview

## Executive Summary

**Serene** is a mental wellness application designed to help users prevent burnout and maintain mental balance through regular check-ins, empathetic AI conversations, and personalized insights. Built with Streamlit and Python, it features a **minimalist gallery-inspired design** (Bauhaus + Scandinavian aesthetics) and stores all data locally using SQLite for privacy.

**Status**: Active development (MVP phase) - Story 1.1 complete, Stories 1.2-1.4 in progress/completed
**Language**: French UI with English comments
**Privacy**: All data stored locally - no cloud uploads

---

## 1. Current Application Structure

### 1.1 Tech Stack

**Frontend & Framework:**
- **Streamlit** (1.40.0+) - Web framework for rapid UI development
- **Plotly** (5.18.0+) - Interactive data visualizations
- **Pandas** (2.1.0+) - Data manipulation for charts/analytics
- **streamlit-shadcn-ui** (0.1.19) - Component library (optional)

**Backend & AI:**
- **Python** (3.11+) - Core runtime
- **Anthropic Claude API** (0.40.0+) - AI conversations & insights generation
- **SQLite3** (built-in) - Local database

**Development & Configuration:**
- **pytest** (8.0.0) - Unit testing
- **pytest-mock** (3.14.0) - Mock objects for testing
- **python-dotenv** (1.0.0) - Environment variable management

### 1.2 Project Directory Structure

```
mental-wellness/
├── app.py                           # Main Streamlit entry point
├── requirements.txt                 # Python dependencies
├── pytest.ini                       # Pytest configuration
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── README.md                        # Project documentation
├── MIGRATION.md                     # Database migration notes
├── migrate_mood_score_range.py     # Database migration script
│
├── src/
│   ├── __init__.py
│   ├── database/                    # Database layer
│   │   ├── db_manager.py           # SQLite database manager (CRUD operations)
│   │   └── schema.sql              # Database schema definition
│   │
│   ├── llm/                         # AI/LLM integration
│   │   ├── conversation_manager.py  # Claude API conversation handling
│   │   └── insights_generator.py    # AI insights generation with caching
│   │
│   ├── ui/                          # UI/Presentation layer
│   │   ├── app.py                   # Main app logic (legacy name)
│   │   ├── checkin.py              # Quick check-in page
│   │   ├── conversation.py          # AI conversation page
│   │   ├── dashboard.py             # Analytics dashboard & insights
│   │   ├── disclaimer.py            # Disclaimer/consent screen
│   │   ├── styles/
│   │   │   ├── serene_styles.py    # CSS & color palette (Gallery Minimalist)
│   │   │   └── __init__.py
│   │   └── ui_components/
│   │       ├── mood_components.py   # Reusable mood display components
│   │       └── __init__.py
│   │
│   └── utils/
│       ├── prompts.py              # LLM system prompts & crisis keywords
│       └── __init__.py
│
├── tests/                           # Test suite
│   ├── test_database.py            # Database manager tests (comprehensive)
│   ├── test_llm.py                 # LLM tests
│   ├── test_insights.py            # Insights generator tests
│   ├── conftest.py                 # Pytest fixtures
│   └── __init__.py
│
└── .streamlit/                      # Streamlit configuration
    └── config.toml
```

---

## 2. User Sessions & Authentication

### 2.1 Current Authentication Model

**NO TRADITIONAL AUTHENTICATION** - Simplified approach for MVP:

- **Session State Management**: Uses Streamlit's built-in `st.session_state` for tracking user interactions within a session
- **Disclaimer Gate**: Users must accept disclaimer before accessing features
  - Stored in: `st.session_state.disclaimer_acknowledged` (boolean)
  - Persists only during current session (not across browser tabs/sessions)
  
- **Local-Only Access**: No user accounts or login system
  - All data tied to local SQLite database on device
  - Each instance of the app has its own isolated data
  - Multiple users sharing a device would share the same database

### 2.2 Session State Structure

```python
st.session_state = {
    'disclaimer_acknowledged': bool,      # Gate to main app
    'current_page': str,                  # Active nav page (Home, Check-in, Conversation, Dashboard)
    'conversation_history': list,         # Last 5 conversations cached in memory
}
```

### 2.3 Multi-User Limitation

**Current Design Limitation:**
- No user isolation - all check-ins, conversations, and insights go into single shared SQLite DB
- Suitable for single-user app or family shared device
- **Future Enhancement**: Add user profiles with separate check-in histories

---

## 3. Mood Tracking & Insights Storage/Display

### 3.1 Mood Tracking System

**Check-in Data Model** (`check_ins` table):
```python
{
    id: int,                    # Primary key
    timestamp: datetime,        # When recorded (default: NOW)
    mood_score: int,           # 0-10 scale (validated)
    notes: str,                # Optional user text (max 500 chars in UI)
    created_at: datetime       # Record creation time
}
```

**Mood Score Interpretation**:
- 0-2: "Très difficile" (Very difficult) → Dark gray
- 3-4: "Difficile" (Difficult) → Medium gray
- 5-6: "Neutre" (Neutral) → Light gray
- 7-8: "Bien" (Good) → Medium gray
- 9-10: "Excellent" → Dark gray

**Design Note**: Color palette is **intentionally desaturated** (all grays/blacks) to avoid emotional triggers and maintain minimalist aesthetic

### 3.2 Data Storage

**Location**: SQLite database (`serene.db`) - local file only
**Indexes**: `idx_check_ins_timestamp` for fast date-range queries
**Validation**: CHECK constraint ensures mood_score BETWEEN 0 AND 10

### 3.3 Insights Storage

**Insights Data Model** (`insights_log` table):
```python
{
    id: int,
    created_at: datetime,
    insight_type: str,              # "weekly", "monthly", etc.
    content: str,                   # AI-generated insight text
    based_on_data: str,            # JSON metadata about data used
    tokens_used: int               # API usage tracking
}
```

**Metadata Example** (`based_on_data`):
```json
{
    "days_count": 30,
    "maturity_level": "mature",     # early/developing/mature
    "conv_count": 15,
    "avg_mood": 7.2
}
```

### 3.4 Mood Display on Dashboard

**Chart Implementation** (Plotly scatter plot):
- **Chart Type**: Scatter plot with date/time on X-axis, mood score (0-10) on Y-axis
- **Styling**: Monochrome (grayscale) with geometric square markers
- **Interactivity**: Hover shows exact date/time and score
- **Period Selection**: Radio buttons for 1 day, 7 days, 30 days, 90 days
- **Metrics Display**:
  - Large center metric: Current latest score
  - Three stat cards: Average, Minimum, Maximum scores for selected period
  - Delta calculation: Latest vs. period average

**Example Metrics Card**:
```
┌─────────────────────────┐
│   Score Actuel          │
│      7.5                │
│      sur 10             │
│───────────────────────  │
│  +0.3 vs moyenne        │
└─────────────────────────┘
```

### 3.5 Check-in History Display

**Location**: Check-in page below form
**Format**: Card-based history (up to 30 days)
**Card Components**:
- Date/time label (formatted: DD/MM/YYYY · HH:MM)
- Large mood score typography
- Mood label text
- Optional user notes (italicized)
- Small black geometric marker (8-16px based on score)

**Animation**: Staggered fade-in for visual appeal

---

## 4. AI Conversation System

### 4.1 Architecture

**Component**: `ConversationManager` class
**API**: Anthropic Claude (streaming)
**Model**: `claude-sonnet-4-20250514`
**Max Tokens**: 1024 per response

### 4.2 Conversation Flow

```
User Input
    ↓
[ConversationManager.send_message()]
    ↓
Crisis Detection Check
    ├─ If crisis keywords detected → Display EMERGENCY_RESOURCES
    └─ Otherwise → Continue
    ↓
Claude API Call (with system prompt)
    ↓
Streaming Response
    ├─ Real-time display with cursor animation ("▌")
    └─ Accumulate full response
    ↓
[DatabaseManager.save_conversation()]
    ├─ User message
    ├─ AI response
    └─ Token usage
    ↓
Add to Session State conversation_history (cache last 5)
```

### 4.3 System Prompt

**Role**: Serene - empathetic AI mental wellness companion

**Key Directives**:
1. Always remind user you're not a healthcare professional
2. On crisis detection: Express concern, recommend professional help, provide French emergency numbers
3. Never give medical diagnoses
4. Never replace medical/therapeutic treatment

**Communication Style**:
- Warm and authentic
- Simple language
- Concise responses (2-4 sentences)
- Use "tu" (informal you) in French

### 4.4 Crisis Detection

**Keywords Monitored** (case-insensitive):
```python
[
    "suicide", "me tuer", "en finir",
    "mourir", "disparaître", "me faire du mal",
    "self-harm", "automutilation"
]
```

**Action**: Show emergency resources banner with numbers:
- **3114** - National suicide prevention line (24/7, free)
- **15** - SAMU (medical emergencies)
- **SOS Amitié** - 09 72 39 40 50 (24/7, listening service)

### 4.5 Conversation Storage

**Data Stored** (for each message pair):
```python
{
    id: int,
    timestamp: datetime,
    user_message: str,              # Full user input
    ai_response: str,               # Full Claude response
    tokens_used: int,               # input_tokens + output_tokens
    created_at: datetime
}
```

**Index**: `idx_conversations_timestamp` for time-based queries
**Display on Dashboard**: Shows last 5 conversations cached in session
**Metrics**: Total conversation count & average per day (last 7 days)

---

## 5. Mood Chart Implementation

### 5.1 Mood Chart Details

**Library**: Plotly Express scatter plot
**Configuration**:

```python
px.scatter(
    df_mood,
    x='timestamp',
    y='mood_score',
    color='mood_score',
    color_continuous_scale=[
        (0.0, '#4A4A4A'),   # Dark gray (low mood)
        (0.5, '#6B6B6B'),   # Medium gray
        (1.0, '#2A2A2A')    # Quasi-black (high mood)
    ],
    range_color=[0, 10]
)
```

### 5.2 Visual Styling

**Markers**:
- Shape: Circles
- Size: 10px
- Border: 1px white line
- Opacity: 0.9

**Layout**:
- Y-axis: Range [0, 11] with grid
- X-axis: Timestamp with grid
- Background: Off-white (#FAF8F3)
- Font: Inter sans-serif
- Height: 350px
- No color scale bar (minimal aesthetic)

**Hover Template**:
```
<b>DD/MM/YYYY à HH:MM</b>
Score: X/10
```

### 5.3 Period Selector

**Radio Button Options**:
- "Aujourd'hui" (1 day)
- "7 jours" (7 days) 
- "30 jours" (30 days) - Default selection
- "90 jours" (90 days)

**Data Query**: Uses `db.get_mood_history(days=N)` to filter from database

---

## 6. Database Schema & Models

### 6.1 Complete Database Schema

**File**: `/src/database/schema.sql`

#### Table 1: `check_ins`
```sql
CREATE TABLE IF NOT EXISTS check_ins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    mood_score INTEGER NOT NULL CHECK(mood_score BETWEEN 0 AND 10),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_check_ins_timestamp ON check_ins(timestamp);
```

#### Table 2: `conversations`
```sql
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    tokens_used INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);
```

#### Table 3: `insights_log`
```sql
CREATE TABLE IF NOT EXISTS insights_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    insight_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    based_on_data TEXT,
    tokens_used INTEGER
);
CREATE INDEX IF NOT EXISTS idx_insights_log_type_created ON insights_log(insight_type, created_at DESC);
```

### 6.2 DatabaseManager Class

**Location**: `/src/database/db_manager.py`
**Responsibility**: SQLite CRUD operations + connection management

**Key Methods**:

| Method | Purpose | Parameters | Returns |
|--------|---------|------------|---------|
| `save_checkin()` | Record mood check-in | `mood_score: int`, `notes: str = ""` | `checkin_id: int` |
| `get_mood_history()` | Retrieve check-ins | `days: int = 30` | `List[Dict]` (DESC by timestamp) |
| `save_conversation()` | Record AI exchange | `user_msg`, `ai_response`, `tokens_used` | `conv_id: int` |
| `get_conversation_history()` | Retrieve conversations | `limit: int = 50` | `List[Dict]` (ASC by timestamp) |
| `get_conversation_count()` | Count conversations | `days: int = 7` | `int` |
| `save_insight()` | Store AI insight | `type`, `content`, `based_on_data`, `tokens` | `insight_id: int` |
| `get_latest_insight()` | Get most recent insight | `insight_type: str` | `Dict or None` |

**Error Handling**:
- Raises `ValueError` for validation errors (e.g., mood_score out of range)
- Raises `sqlite3.IntegrityError` caught and re-wrapped as ValueError

### 6.3 Data Validation

**Check-in Validation**:
- `mood_score`: Must be integer 0-10 (enforced in Python + SQL CHECK constraint)
- `notes`: Optional, max 500 chars (UI), stored as TEXT

**Conversation Validation**:
- Both `user_message` and `ai_response`: Cannot be empty
- `tokens_used`: Optional, default 0

**Insight Validation**:
- `insight_type` and `content`: Required, cannot be empty

### 6.4 Query Patterns

**Recent Check-ins** (for dashboard):
```python
SELECT * FROM check_ins
WHERE timestamp >= (NOW - 30 days)
ORDER BY timestamp DESC
```

**Conversation History** (with limit):
```python
SELECT * FROM conversations
ORDER BY timestamp ASC
LIMIT 50
```

**Conversation Count** (time-filtered):
```python
SELECT COUNT(*) FROM conversations
WHERE timestamp >= (NOW - 7 days)
```

**Latest Insight by Type**:
```python
SELECT * FROM insights_log
WHERE insight_type = ?
ORDER BY created_at DESC
LIMIT 1
```

---

## 7. AI Insights Generation

### 7.1 InsightsGenerator Class

**Location**: `/src/llm/insights_generator.py`
**Purpose**: Generate personalized, adaptive AI insights based on user data
**Caching**: 24-hour cache (configurable via `REGENERATE_INSIGHTS_AFTER_HOURS`)

### 7.2 Adaptive Insight Levels

**System Prompt Formatting**:
```python
maturity_level = {
    "early": days_count < 3,           # Newly started
    "developing": 3 <= days_count < 7, # Building pattern
    "mature": days_count >= 7          # Rich dataset
}
```

**Early Stage** (< 3 days):
- Opening: "C'est un excellent début ! 🌱"
- Content: Light analysis of available data
- Closing: Strong encouragement to continue daily
- Tone: Very encouraging, focus on engagement

**Developing Stage** (3-6 days):
- Opening: "Belle régularité ! 📈"
- Content: Preliminary observations + emerging trends
- Note: "Quelques jours de plus m'aideront à affiner mon analyse"
- Tone: Encouraging, recognition of progress

**Mature Stage** (≥ 7 days):
- Complete analysis: Trends, patterns, mood triggers
- 2-3 key observations
- 1-2 concrete suggestions for the week
- Tone: Professional but warm

**Format**: Markdown, max 250 words, never blocking/negative

### 7.3 Data Context Building

**Data Sources**:
1. **Mood Data**: Last 30 days check-ins
2. **Conversation Count**: Last 30 days interactions
3. **Recent Conversation Excerpts**: Last 5 user messages (truncated to 200 chars each)

**Context Format**:
```
Nombre de jours de données: 10
Nombre de conversations: 5
Score d'humeur moyen: 6.8/10

Notes de check-ins récents:
- Journée stressante au travail
- Belle promenade ce matin

Extraits de conversations récentes:
- Je me sens fatigué ces derniers jours...
- Difficile de me concentrer au travail
```

### 7.4 Caching Logic

**Regeneration Check**:
```python
def _should_regenerate_insights(self) -> bool:
    latest = db.get_latest_insight("weekly")
    if not latest:
        return True  # No existing insight
    
    age = datetime.now() - datetime.fromisoformat(latest['created_at'])
    return age > timedelta(hours=24)  # Regenerate if > 24 hours old
```

**Display Flow**:
1. User loads dashboard
2. InsightsGenerator checks age of last insight
3. If < 24 hours: Return cached version
4. If > 24 hours: Generate new insight
5. Save to `insights_log` table with metadata
6. Display with loading skeleton animation

### 7.5 Token Usage Tracking

**Data Collected**:
```python
{
    "tokens_used": usage.input_tokens + usage.output_tokens,
    "based_on_data": {
        "days_count": 30,
        "maturity_level": "mature",
        "conv_count": 15,
        "avg_mood": 7.2
    }
}
```

**Purpose**: Monitor API costs and understand which insights use more tokens

---

## 8. UI/UX Architecture

### 8.1 Design System: "Gallery Minimalist"

**Inspiration**: Contemporary art galleries, Bauhaus, Scandinavian minimalism

**Color Palette**:
```python
COLORS = {
    "ivory": "#FAF8F3",            # Main background
    "white": "#FFFFFF",
    "black": "#000000",
    "charcoal": "#1A1A1A",         # Primary text
    "gray_dark": "#4A4A4A",        # Secondary text
    "gray_medium": "#6B6B6B",
    "gray_light": "#9E9E9E",
    "line_dark": "#2A2A2A",        # Thin lines
    "line_light": "#E0E0E0"
}
```

**Typography**:
- **Serif**: Cormorant Garamond (titles, elegant)
  - h1: 3rem, weight 300
  - h2: 2rem, weight 300
  - h3: 1.5rem, weight 400
- **Sans-serif**: Inter (body, clean)
  - Default: 0.9375rem, weight 300
  - Forms: 0.875rem, weight 300

**Geometric Elements**:
- No border-radius (all 0px)
- Thin borders (1px or 2px solid)
- Subtle shadows (`0 1px 2px rgba(0,0,0,0.03)`)
- Generous whitespace
- Vertical lines as separators

### 8.2 Page Navigation

**Navigation Model**: Streamlit sidebar with custom buttons
**Pages**:
1. **Home** - Hero section + feature overview
2. **Check-in** - Daily mood tracking form
3. **Conversation** - AI chat interface
4. **Dashboard** - Analytics & insights

**Disclaimer Gate**: Must accept before accessing main app

### 8.3 Key UI Components

**File**: `/src/ui/ui_components/mood_components.py`

#### `mood_display_card()`
- Large mood score (3.5rem)
- Label (uppercase, small)
- Geometric separator line
- Used in: Check-in form after slider

#### `stats_banner()`
- Shows total check-ins in period
- "Museum label" style with left border accent
- Used in: History section

#### `history_card()`
- Date/time label
- Score + label
- Optional user notes (italic)
- Geometric marker (square, 8-16px)
- Animated entrance

#### `empty_state()`
- Title + description
- Geometric separator
- "Did you know?" tip box
- Used when no data exists

#### `page_header()`
- Page title (3rem, serif)
- Description text
- Bottom border

### 8.4 Forms

**Check-in Form**:
- Slider (0-10) with custom styling
- Mood display card updates in real-time
- Notes textarea (max 500 chars, optional)
- Submit button (black background, uppercase, all-caps text)

**Conversation Interface**:
- Chat message display with custom bubbles
- User messages: Black background, white text, left-aligned
- AI messages: White background, charcoal text, right-aligned
- Chat input: Built-in Streamlit chat_input component
- Avatar styling: Geometric squares with "M" (Moi) and "S" (Serene)

### 8.5 Animations (CSS)

**Keyframe Animations**:
- `fadeIn`: 0.8s opacity change
- `fadeInUp`: 0.5-0.7s from bottom with opacity
- `fadeInDown`: 0.4s from top with opacity
- `scaleIn`: Zoom effect for mood cards

**Transitions**: 0.3s cubic-bezier for smooth state changes
**Accessibility**: Respects `prefers-reduced-motion` media query

---

## 9. Application Flow & State Management

### 9.1 Main App Flow

```
app.py (entry point)
    │
    ├─ Load CSS (get_main_css())
    │
    ├─ Check disclaimer_acknowledged in session_state
    │   │
    │   ├─ False → show_disclaimer() → Disclaimer page
    │   │           After accept → Set session_state["disclaimer_acknowledged"] = True
    │   │
    │   └─ True → Main app
    │           │
    │           ├─ Sidebar navigation (4 buttons)
    │           │   └─ Updates session_state["current_page"]
    │           │
    │           └─ Route to page based on current_page:
    │               ├─ "Home" → show_home()
    │               ├─ "Check-in" → show_checkin()
    │               ├─ "Conversation" → show_conversation()
    │               └─ "Dashboard" → show_dashboard()
```

### 9.2 Check-in Page Flow

```
show_checkin()
    │
    ├─ Display form
    │   ├─ Slider (0-10)
    │   ├─ Mood display card
    │   └─ Notes textarea
    │
    ├─ Form submission
    │   │
    │   ├─ Get database (cached singleton)
    │   ├─ Validate mood_score
    │   ├─ Call db.save_checkin(score, notes)
    │   ├─ Display success message
    │   └─ Clear form
    │
    ├─ Load mood history (db.get_mood_history(30))
    │
    └─ Display history cards
        └─ If empty → Show empty state
```

### 9.3 Conversation Page Flow

```
show_conversation()
    │
    ├─ Load conversation manager (cached singleton)
    │   │
    │   └─ If API key missing → Show error + return
    │
    ├─ Initialize session_state["conversation_history"] if needed
    │   └─ Load last 5 conversations from DB
    │
    ├─ Display conversation history
    │   └─ Render each as chat messages
    │
    ├─ Wait for chat_input()
    │   │
    │   ├─ Check for crisis keywords → Show emergency banner if detected
    │   │
    │   ├─ Call manager.send_message(user_input)
    │   │   └─ Stream response from Claude API
    │   │   └─ Save to DB after completion
    │   │
    │   └─ Add to session_state["conversation_history"]
```

### 9.4 Dashboard Page Flow

```
show_dashboard()
    │
    ├─ Section 1: Mood Metrics
    │   ├─ Period selector (radio button)
    │   ├─ Load mood_data = db.get_mood_history(days=N)
    │   │
    │   └─ If data exists:
    │       ├─ Display large central metric (latest score)
    │       ├─ Calculate stats (avg, min, max)
    │       ├─ Display 3 stat cards
    │       ├─ Render Plotly scatter chart
    │       │
    │       └─ If empty:
    │           └─ Show "Start tracking" empty state
    │
    ├─ Section 2: Conversation Activity
    │   ├─ Load conv_history = db.get_conversation_history()
    │   │
    │   └─ If data exists:
    │       ├─ Calculate metrics (total, avg per day)
    │       ├─ Display 2 stat cards
    │       │
    │       └─ If empty:
    │           └─ Show "Start conversation" empty state
    │
    └─ Section 3: AI Insights
        ├─ Get InsightsGenerator (cached singleton)
        │
        ├─ Show loading skeleton
        │
        ├─ Call generator.get_adaptive_insight()
        │   ├─ Check if regeneration needed (24h cache)
        │   ├─ Return cached or generate new
        │   └─ Save to DB if new
        │
        ├─ Display insight with styling
        │
        └─ Show insight metadata in expander
            └─ Generation date, tokens used, freshness status
```

### 9.5 Session State Caching

**Cached Singletons** (using `@st.cache_resource`):
```python
@st.cache_resource
def get_database():
    return DatabaseManager("serene.db")

@st.cache_resource
def get_conversation_manager():
    return ConversationManager(get_database())

@st.cache_resource
def get_insights_generator():
    return InsightsGenerator(get_database())
```

**Session State Variables**:
```python
st.session_state = {
    'disclaimer_acknowledged': bool,
    'current_page': str,
    'conversation_history': list  # Last 5 conversations
}
```

---

## 10. Current Features & Implementation Status

### Story 1.1: Foundation + Disclaimers ✅ COMPLETE
- [x] Minimalist Gallery UI design system
- [x] Disclaimer screen with emergency resources
- [x] Navigation menu
- [x] Basic home page with feature cards

### Story 1.2: Quick Check-in + Database ✅ COMPLETE
- [x] Check-in form with mood slider (0-10)
- [x] Notes textarea
- [x] SQLite database schema
- [x] Save check-ins with validation
- [x] Display history (30 days)
- [x] Mood score interpretation
- [x] Museum-style history cards

### Story 1.3: Conversation ✅ COMPLETE
- [x] Claude API integration
- [x] Streaming responses
- [x] Crisis detection
- [x] Save conversation history
- [x] Display last 5 conversations
- [x] Error handling for missing API key
- [x] Emergency resources display

### Story 1.4: Dashboard + Insights ✅ COMPLETE
- [x] Mood chart (Plotly scatter)
- [x] Period selector (1/7/30/90 days)
- [x] Metrics display (avg, min, max)
- [x] Conversation activity metrics
- [x] AI insights generation
- [x] Adaptive insight levels (early/developing/mature)
- [x] 24-hour insight caching
- [x] Token usage tracking

### Testing ✅ COMPREHENSIVE
- [x] Unit tests for DatabaseManager (60+ test cases)
- [x] Fixtures for mock database
- [x] Validation tests
- [x] Integration tests

---

## 11. Notable Implementation Details

### 11.1 No User Authentication
- **Rationale**: MVP simplicity, local-only data
- **Trade-off**: Single user per device
- **Future**: Could add user profiles for family use

### 11.2 Stateless Conversations
- Conversations stored in DB but **not used as context** for future messages
- Each conversation is independent (no multi-turn context memory)
- **Implication**: Claude doesn't know about previous conversations
- **Benefit**: Simpler architecture, lower API costs
- **Trade-off**: Less personalized over time

### 11.3 Emoji Removal in Minimalister Mode
- AI insights generated with emojis (from prompts)
- CSS + regex removes them for visual consistency
- `remove_emojis()` function in dashboard.py

### 11.4 Conversation Display Limit
- Database stores all conversations
- UI displays only last 5 in conversation history
- Dashboard shows stats for last 100 conversations
- Full history available but not displayed (privacy consideration)

### 11.5 Session State vs Persistent State
- **Session State** (Streamlit): user page, conversation cache (ephemeral)
- **Persistent State** (SQLite): mood, conversations, insights (permanent)
- Conversation history reloaded from DB on page refresh

---

## 12. Security & Privacy Considerations

### ✅ Privacy Measures
- ✅ **Local-only storage**: All data in `serene.db` on user's device
- ✅ **No cloud sync**: Data never uploaded
- ✅ **No user accounts**: No authentication infrastructure
- ✅ **No analytics**: No tracking/telemetry
- ✅ **SQLite**: No external database connections

### ⚠️ Security Notes
- **SQLite file not encrypted**: Database file stored in plaintext
- **API key exposure**: ANTHROPIC_API_KEY in .env file (must be kept secure)
- **No HTTPS**: Running locally (no SSL needed, unless self-hosted)
- **Session vulnerability**: Browser session shared across tabs/windows

### 🔐 Recommendations for Production
1. Encrypt SQLite database at rest
2. Use environment variables from secure vaults
3. Add user authentication + per-user data isolation
4. Implement rate limiting
5. Add activity logging
6. GDPR/HIPAA compliance review

---

## 13. Dependencies & Versions

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | ≥1.40.0 | Web framework |
| anthropic | ≥0.40.0 | Claude API client |
| plotly | ≥5.18.0 | Interactive charts |
| pandas | ≥2.1.0 | Data manipulation |
| python-dotenv | ≥1.0.0 | Env var management |
| pytest | ≥8.0.0 | Testing framework |
| pytest-mock | ≥3.14.0 | Test mocks |
| streamlit-shadcn-ui | ≥0.1.19 | UI components (optional) |

---

## 14. Configuration & Setup

### Environment Variables (`.env`)
```env
ANTHROPIC_API_KEY=sk-ant-...     # Claude API key
DATABASE_PATH=serene.db           # SQLite path (default)
DEBUG_MODE=false                  # Debug logging
```

### Streamlit Config (`.streamlit/config.toml`)
- Page layout: `wide`
- Page icon: "◼" (minimalist black square)
- Title: "Serene"

---

## 15. Testing Architecture

**Test Files**: `/tests/` directory
**Framework**: pytest with fixtures

### Key Test Fixtures
```python
@pytest.fixture
def mock_db():
    """In-memory SQLite database for testing"""
    return DatabaseManager(":memory:")

@pytest.fixture
def sample_checkins(mock_db):
    """Pre-populated database with 5 check-ins"""
    for score in [3, 7, 5, 8, 6]:
        mock_db.save_checkin(score, f"Note {score}")
    return mock_db
```

### Test Coverage
- **DatabaseManager**: 60+ tests covering all CRUD operations
- **Validation**: Boundary tests, error cases
- **Data integrity**: Schema, indexes, constraints

---

## 16. Known Limitations & Future Enhancements

### Current Limitations
1. ❌ No multi-user support (single shared database)
2. ❌ No conversation context (stateless conversations)
3. ❌ No mood trend predictions
4. ❌ No habit tracking beyond mood
5. ❌ No sleep/exercise tracking
6. ❌ No medication log
7. ❌ No therapist integration
8. ❌ No export/backup feature
9. ❌ No mobile app (Streamlit only)
10. ❌ No offline mode (requires API key at startup)

### Proposed Enhancements
- [ ] User profiles for multi-user support
- [ ] Conversation context memory (long-term)
- [ ] Mood trend prediction (ML model)
- [ ] Custom insights by user preferences
- [ ] Integration with calendar (identify triggers)
- [ ] Notification system for check-in reminders
- [ ] Data export (CSV/PDF report)
- [ ] Dark mode toggle
- [ ] Multilingual support
- [ ] Voice input for check-ins
- [ ] Integration with Fitbit/Apple Health

---

## 17. Conclusion

**Serene** is a thoughtfully designed mental wellness companion that prioritizes:

1. **Privacy**: Local-only, zero cloud storage
2. **Simplicity**: Clean, minimalist interface
3. **Empathy**: AI conversations + adaptive insights
4. **Responsibility**: Crisis detection + emergency resources
5. **Transparency**: Clear disclaimers about limitations

The architecture is modular and extensible, with clear separation between database, LLM, and UI layers. The codebase is well-tested and documented, making it suitable for further development.

**Current Stage**: MVP with all planned Story features implemented. Ready for user testing and feedback.

