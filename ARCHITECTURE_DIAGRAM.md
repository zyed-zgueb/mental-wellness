# Serene Architecture Diagram

## High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE LAYER (Streamlit)                 │
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ Home Page    │  │ Check-in     │  │ Conversation │  │ Dashboard  │ │
│  │              │  │ Page         │  │ Page         │  │ Page       │ │
│  │ • Hero       │  │              │  │              │  │            │ │
│  │ • Features   │  │ • Form       │  │ • Chat UI    │  │ • Charts   │ │
│  │ • CTA        │  │ • History    │  │ • Messages   │  │ • Metrics  │ │
│  │              │  │   Cards      │  │ • Crisis     │  │ • Insights │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘ │
│         ▲                 ▲                  ▲                 ▲        │
│         │                 │                  │                 │        │
│         └─────────────────┴──────────────────┴─────────────────┘        │
│                            │                                            │
│                    Disclaimer Gate                                      │
│                    (Session State)                                      │
│                                                                         │
└─────────────────────┬───────────────────────────────────────────────────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
         ▼            ▼            ▼
    ┌─────────┐ ┌──────────┐ ┌─────────────┐
    │Database │ │Conversa- │ │ Insights    │
    │Manager  │ │tion      │ │ Generator   │
    │         │ │ Manager  │ │             │
    └────┬────┘ └────┬─────┘ └─────┬───────┘
         │           │             │
         │ SQLite    │ Claude API  │ Claude API
         │           │             │
         ▼           ▼             ▼
    ┌──────────────────┐    ┌──────────────┐
    │                  │    │              │
    │  Serene.db       │    │ Claude API   │
    │  (Local SQLite)  │    │ (Streaming)  │
    │                  │    │              │
    │ • check_ins      │    └──────────────┘
    │ • conversations  │
    │ • insights_log   │
    │                  │
    └──────────────────┘
```

## Data Flow Diagram

### Check-in Flow
```
User Input (Slider + Notes)
         │
         ▼
    [Validation]
    mood_score: 0-10
    notes: max 500 chars
         │
         ▼
  [DatabaseManager]
  save_checkin()
         │
         ▼
   SQLite: check_ins
    (INSERT)
         │
         ▼
   Success Message
         │
         ▼
  [Read & Display]
  get_mood_history(30)
         │
         ▼
   History Cards (Last 30 days)
```

### Conversation Flow
```
User Message
    │
    ▼
[Crisis Detection]
├─ Detected → Show Emergency Banner
└─ Safe → Continue
    │
    ▼
[Claude API Call]
send_message()
├─ System Prompt: Role Definition
├─ Stream Response
└─ Accumulate tokens
    │
    ▼
[Streaming Display]
Real-time chat bubble
with cursor animation
    │
    ▼
[Save to Database]
save_conversation()
├─ user_message
├─ ai_response
└─ tokens_used
    │
    ▼
[Cache in Session]
conversation_history
(Last 5 only)
```

### Dashboard Mood Chart Flow
```
User Selects Period
(1/7/30/90 days)
    │
    ▼
[Query Database]
get_mood_history(days=N)
    │
    ▼
[Calculate Metrics]
├─ Latest Score
├─ Average Score
├─ Min/Max Scores
└─ Delta vs Average
    │
    ▼
[Transform for Plotly]
Pandas DataFrame
├─ timestamp (X-axis)
└─ mood_score (Y-axis)
    │
    ▼
[Render Chart]
Scatter Plot
├─ Grayscale coloring
├─ Geometric markers
└─ Interactive hover
```

### Insights Generation Flow
```
User Views Dashboard
    │
    ▼
[Check Cache]
get_latest_insight()
    │
    ├─ If exists & < 24h old
    │  └─ Return cached
    │
    └─ If missing or > 24h old
       │
       ▼
    [Gather Data]
    ├─ get_mood_history(30)
    ├─ get_conversation_count(30)
    ├─ get_conversation_history(5)
    └─ Calculate avg_mood
       │
       ▼
    [Determine Maturity]
    ├─ days < 3    → "early"
    ├─ 3-6 days    → "developing"
    └─ ≥ 7 days    → "mature"
       │
       ▼
    [Build Context]
    Data summary for prompt
       │
       ▼
    [Claude API]
    generate_adaptive_summary()
    (500 tokens max)
       │
       ▼
    [Save to Database]
    save_insight()
    ├─ content
    ├─ maturity_level
    ├─ based_on_data (JSON)
    └─ tokens_used
       │
       ▼
    [Display]
    Insight + Metadata
```

## Component Interaction Diagram

```
┌──────────────────────────────────────────────────────┐
│                  STREAMLIT UI                        │
│  (Multiple .py files in src/ui/)                     │
└────────────┬─────────────────────────────────────────┘
             │
     ┌───────┴────────┬──────────────┬────────────────┐
     │                │              │                │
     ▼                ▼              ▼                ▼
┌──────────┐  ┌────────────┐  ┌──────────────┐  ┌──────────┐
│ Database │  │Conversatio │  │   Insights   │  │  Styles  │
│ Manager  │  │ n Manager  │  │  Generator   │  │   CSS    │
└────┬─────┘  └─────┬──────┘  └───────┬──────┘  └──────────┘
     │              │                 │
     │ CRUD Ops    │ Streaming Chat  │ Adaptive AI
     │              │                 │
     ▼              ▼                 ▼
 ┌────────────────────────────────────────┐
 │         LOCAL SQLITE DATABASE          │
 │         (serene.db)                    │
 │                                        │
 │  check_ins │ conversations │ insights  │
 └────────────────────────────────────────┘
```

## Page Routing & Navigation

```
                    ┌─────────────────┐
                    │  Load app.py    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Load CSS       │
                    │ & Fonts         │
                    └────────┬────────┘
                             │
                 ┌───────────▼────────────┐
                 │ Check                  │
                 │ disclaimer_acknowledged│
                 └───┬──────────────┬─────┘
                     │              │
                NO  ▼              ▼  YES
            ┌──────────────┐  ┌─────────────┐
            │  DISCLAIMER  │  │  MAIN APP   │
            │  PAGE        │  │  (Sidebar)  │
            │              │  │             │
            │ • About      │  │ ┌─────────┐ │
            │ • Limits     │  │ │Home     │ │
            │ • Emergency  │  │ ├─────────┤ │
            │ • Privacy    │  │ │Check-in │ │
            │ • Accept BTN │  │ ├─────────┤ │
            │              │  │ │Conversa │ │
            └──────┬───────┘  │ │-tion    │ │
                   │          │ ├─────────┤ │
                   └─────┬────┬─│Dashboard│ │
                         │    │ └─────────┘ │
                    [Set Flag] └─────────────┘
                         │
                         ▼
                    [Continue]
```

## Database Schema Relationships

```
┌─────────────────────────────┐
│       check_ins             │
├─────────────────────────────┤
│ id (PK) ───────┐            │
│ timestamp      │            │
│ mood_score     │            │
│ notes          │            │
│ created_at     │            │
└─────────────────────────────┘

┌─────────────────────────────┐
│     conversations           │
├─────────────────────────────┤
│ id (PK)                     │
│ timestamp (indexed)         │
│ user_message                │
│ ai_response                 │
│ tokens_used                 │
│ created_at                  │
└─────────────────────────────┘

┌─────────────────────────────┐
│      insights_log           │
├─────────────────────────────┤
│ id (PK)                     │
│ created_at (indexed)        │
│ insight_type (indexed)      │
│ content                     │
│ based_on_data (JSON)        │
│ tokens_used                 │
└─────────────────────────────┘

No direct relationships (denormalized for simplicity)
Each record is independent, indexed by timestamp
```

## Session State Management

```
                 Session Starts
                      │
                      ▼
          ┌─────────────────────────┐
          │ st.session_state init   │
          │                         │
          │ ┌─────────────────────┐ │
          │ │disclaimer_ack: False│ │
          │ └─────────────────────┘ │
          └────────────┬────────────┘
                       │
                       ▼
          ┌─────────────────────────┐
          │ User accepts disclaimer │
          │                         │
          │ Set flag to True        │
          └────────────┬────────────┘
                       │
          ┌────────────▼────────────┐
          │ Initialize Main App     │
          │                         │
          │ ┌─────────────────────┐ │
          │ │current_page: "Home" │ │
          │ ├─────────────────────┤ │
          │ │conversation_history │ │
          │ │   = []              │ │
          │ └─────────────────────┘ │
          └────────────┬────────────┘
                       │
          ┌────────────▼────────────┐
          │ User Navigation         │
          │                         │
          │ current_page switches   │
          │ between 4 pages         │
          └─────────────────────────┘
```

## API Integration Points

```
Serene App
    │
    │ (Streaming)
    ├──────────────────────────┐
    │                          │
    ▼                          ▼
Claude API (Conversation)  Claude API (Insights)
    │                          │
    ├─ Model: Sonnet 4.5       ├─ Model: Sonnet 4.5
    ├─ Max Tokens: 1024        ├─ Max Tokens: 500
    ├─ Streaming: Yes          ├─ Streaming: No
    └─ Save response          └─ Save response
        (tokens tracked)           (tokens tracked)
```

## Environment & Configuration

```
┌────────────────────────────────────────┐
│         .env (Local)                   │
├────────────────────────────────────────┤
│ ANTHROPIC_API_KEY=sk-ant-...          │
│ DATABASE_PATH=serene.db               │
│ DEBUG_MODE=false                      │
└────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│  Python dotenv loader                  │
│  (os.getenv)                           │
└────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│  Application Classes                   │
├────────────────────────────────────────┤
│ • DatabaseManager                      │
│ • ConversationManager                  │
│ • InsightsGenerator                    │
└────────────────────────────────────────┘
```

