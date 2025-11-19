# Serene - Quick Reference Guide

## Key File Locations & Purposes

### Core Application
| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| `app.py` | Main entry point | `main()`, `show_home()` |
| `.env.example` | Configuration template | API keys & settings |

### Database Layer (`src/database/`)
| File | Purpose | Key Features |
|------|---------|--------------|
| `db_manager.py` | SQLite CRUD operations | `DatabaseManager` class with 7 main methods |
| `schema.sql` | Database tables & indexes | 3 tables: check_ins, conversations, insights_log |

### LLM Integration (`src/llm/`)
| File | Purpose | Key Features |
|------|---------|--------------|
| `conversation_manager.py` | Claude API conversations | Streaming, crisis detection, token tracking |
| `insights_generator.py` | AI insight generation | Adaptive levels, 24h caching, metadata tracking |

### UI Components (`src/ui/`)
| File | Purpose | Key Elements |
|------|---------|--------------|
| `checkin.py` | Check-in page | Form, validation, history display |
| `conversation.py` | Conversation page | Chat UI, crisis banner, message streaming |
| `dashboard.py` | Analytics dashboard | Charts, metrics, insights, period selector |
| `disclaimer.py` | Disclaimer screen | Info cards, emergency numbers, consent button |
| `styles/serene_styles.py` | CSS & design system | Colors, typography, animations, responsive |
| `ui_components/mood_components.py` | Reusable components | mood_display_card, stats_banner, history_card |

### Utilities (`src/utils/`)
| File | Purpose | Key Content |
|------|---------|------------|
| `prompts.py` | LLM prompts & constants | System prompts, crisis keywords, emergency resources |

### Testing (`tests/`)
| File | Purpose | Test Count |
|------|---------|-----------|
| `test_database.py` | Database manager tests | 60+ test cases |
| `test_llm.py` | LLM integration tests | Tests for conversation manager |
| `test_insights.py` | Insights generator tests | Tests for adaptive generation |
| `conftest.py` | Pytest fixtures | `mock_db`, `sample_checkins` |

---

## DatabaseManager API Quick Reference

### Check-in Operations
```python
# Save a check-in
checkin_id = db.save_checkin(mood_score=7, notes="Bonne journée")

# Get mood history (last N days)
history = db.get_mood_history(days=30)  # Returns: List[Dict]
```

### Conversation Operations
```python
# Save a conversation
conv_id = db.save_conversation(
    user_message="Hello",
    ai_response="Hi there!",
    tokens_used=45
)

# Get conversation history
history = db.get_conversation_history(limit=50)  # Returns: List[Dict]

# Count conversations
count = db.get_conversation_count(days=7)  # Returns: int
```

### Insight Operations
```python
# Save an insight
insight_id = db.save_insight(
    insight_type="weekly",
    content="Your insights...",
    based_on_data='{"days": 7}',
    tokens_used=150
)

# Get latest insight
insight = db.get_latest_insight("weekly")  # Returns: Dict or None
```

### Error Handling
```python
try:
    db.save_checkin(mood_score=11)  # Invalid!
except ValueError as e:
    print(f"Validation error: {e}")
```

---

## Streamlit Session State

### Available States
```python
st.session_state = {
    'disclaimer_acknowledged': bool,      # True/False
    'current_page': str,                  # "Home", "Check-in", "Conversation", "Dashboard"
    'conversation_history': list,         # Last 5 conversations from DB
}
```

### Accessing States
```python
# Check if user accepted disclaimer
if not st.session_state.get('disclaimer_acknowledged', False):
    show_disclaimer()

# Get current page
page = st.session_state.current_page

# Update state
st.session_state.current_page = "Dashboard"
st.rerun()  # Trigger re-render
```

---

## Claude API Integration

### ConversationManager
```python
from src.llm.conversation_manager import ConversationManager

# Initialize
manager = ConversationManager(db)

# Send message (streaming)
for chunk in manager.send_message("Hello"):
    print(chunk, end="", flush=True)

# Detect crisis
if manager.detect_crisis("I want to hurt myself"):
    # Show emergency resources
    st.warning(EMERGENCY_RESOURCES)
```

### InsightsGenerator
```python
from src.llm.insights_generator import InsightsGenerator

# Initialize
gen = InsightsGenerator(db)

# Get adaptive insight (with caching)
insight = gen.get_adaptive_insight()

# Check maturity level
level = gen._get_data_maturity_level(days=5)  # "early", "developing", "mature"
```

---

## UI Components Usage

### mood_display_card()
```python
from src.ui.ui_components.mood_components import mood_display_card

html = mood_display_card(
    mood_score=7,
    mood_emoji="",
    mood_label="Bien",
    mood_color="#6B6B6B"
)
st.markdown(html, unsafe_allow_html=True)
```

### history_card()
```python
from src.ui.ui_components.mood_components import history_card

for i, checkin in enumerate(history):
    html = history_card(
        checkin=checkin,
        mood_emoji="",
        mood_label=get_mood_label(checkin['mood_score']),
        mood_color=get_mood_color(checkin['mood_score']),
        formatted_date="01/12/2024",
        formatted_time="14:30",
        index=i
    )
    st.html(html)
```

---

## Environment Variables

### Required
```env
ANTHROPIC_API_KEY=sk-ant-...    # Claude API key (required for conversations)
```

### Optional
```env
DATABASE_PATH=serene.db          # SQLite database path (default: serene.db)
DEBUG_MODE=false                 # Debug logging (default: false)
```

### How to Set
1. Copy `.env.example` to `.env`
2. Add your ANTHROPIC_API_KEY
3. Restart the Streamlit app

---

## Common Workflows

### Adding a New Check-in
```python
from src.database.db_manager import DatabaseManager

db = DatabaseManager("serene.db")
try:
    checkin_id = db.save_checkin(
        mood_score=7,
        notes="Great day at work!"
    )
    print(f"Saved check-in #{checkin_id}")
except ValueError as e:
    print(f"Error: {e}")
```

### Displaying Mood Chart
```python
import plotly.express as px
from src.database.db_manager import DatabaseManager

db = DatabaseManager("serene.db")
mood_data = db.get_mood_history(days=30)
df = pd.DataFrame(mood_data)
df['timestamp'] = pd.to_datetime(df['timestamp'])

fig = px.scatter(df, x='timestamp', y='mood_score')
st.plotly_chart(fig)
```

### Getting AI Insights
```python
from src.llm.insights_generator import InsightsGenerator

gen = InsightsGenerator(db)
insight = gen.get_adaptive_insight()  # Auto-cached for 24h
print(insight)
```

### Handling Crisis
```python
from src.llm.conversation_manager import ConversationManager
from src.utils.prompts import EMERGENCY_RESOURCES

manager = ConversationManager(db)
user_input = "I feel like ending it all"

if manager.detect_crisis(user_input):
    st.warning(EMERGENCY_RESOURCES)
    return  # Stop further processing
```

---

## Design System Constants

### Colors (from `serene_styles.py`)
```python
COLORS = {
    "ivory": "#FAF8F3",           # Main background
    "white": "#FFFFFF",
    "black": "#000000",
    "charcoal": "#1A1A1A",        # Primary text
    "gray_dark": "#4A4A4A",
    "gray_medium": "#6B6B6B",
    "gray_light": "#9E9E9E",
    "line_dark": "#2A2A2A",
    "line_light": "#E0E0E0",
}
```

### Mood Color Mapping
```python
mood_colors = {
    0-2: "Très difficile" → "#4A4A4A",
    3-4: "Difficile" → "#6B6B6B",
    5-6: "Neutre" → "#9E9E9E",
    7-8: "Bien" → "#6B6B6B",
    9-10: "Excellent" → "#4A4A4A",
}
```

### Typography
- **Titles**: Cormorant Garamond, weight 300-400
- **Body**: Inter, weight 300-400
- **Sizes**: h1=3rem, h2=2rem, body=0.9375rem

---

## Testing Commands

### Run all tests
```bash
pytest tests/
```

### Run specific test file
```bash
pytest tests/test_database.py
```

### Run specific test class
```bash
pytest tests/test_database.py::TestSaveCheckin
```

### Run with verbose output
```bash
pytest tests/ -v
```

### Check test coverage
```bash
pytest tests/ --cov=src
```

---

## Common Issues & Solutions

### "ANTHROPIC_API_KEY not found"
**Problem**: Conversation page shows error
**Solution**: 
1. Create `.env` file
2. Add `ANTHROPIC_API_KEY=sk-ant-...`
3. Restart Streamlit

### "mood_score must be between 0 and 10"
**Problem**: Check-in validation error
**Solution**: User tried to save score < 0 or > 10. UI slider prevents this, but API validation catches it.

### "Conversation history not showing"
**Problem**: Last 5 conversations not displayed
**Solution**: 
1. Check database exists (`serene.db`)
2. Verify conversations were saved
3. Check `db.get_conversation_history()` returns data

### "Insights not generating"
**Problem**: Skeleton animation shows but insight doesn't appear
**Solution**:
1. Check API key is valid
2. Check database has at least 1 check-in
3. Check Claude API quota/credits
4. Check logs for API errors

### Database file permissions
**Problem**: "database is locked" error
**Solution**:
1. Ensure only one instance of app is running
2. Check file permissions: `chmod 644 serene.db`
3. Delete and recreate database if corrupted

---

## Performance Considerations

### Database Queries
- **Indexed**: `timestamp` on all tables for fast range queries
- **Limit**: Conversation history limited to last 50 by default
- **Cache**: Dashboard insights cached for 24 hours

### API Calls
- **Streaming**: Conversations use streaming (lower latency)
- **Token Tracking**: All API responses tracked for cost monitoring
- **Max Tokens**: 1024 for conversations, 500 for insights

### UI Performance
- **Caching**: Singletons used for DB, manager, generator
- **Session State**: Conversation history cached in memory (last 5)
- **Charts**: Plotly used for interactive, performant visualizations

---

## Folder Structure for Quick Navigation

```
mental-wellness/
├── CODEBASE_OVERVIEW.md ← Full documentation
├── ARCHITECTURE_DIAGRAM.md ← Visual diagrams
├── QUICK_REFERENCE.md ← This file
│
├── app.py ← Start here
├── requirements.txt
├── .env.example
│
├── src/
│   ├── database/db_manager.py ← Database layer
│   ├── llm/conversation_manager.py ← AI conversations
│   ├── llm/insights_generator.py ← AI insights
│   ├── ui/checkin.py ← Check-in page
│   ├── ui/conversation.py ← Conversation page
│   ├── ui/dashboard.py ← Dashboard page
│   ├── ui/styles/serene_styles.py ← CSS & design
│   └── utils/prompts.py ← LLM prompts
│
└── tests/
    ├── test_database.py ← 60+ tests
    └── conftest.py ← Test fixtures
```

---

## Getting Started

### 1. Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add ANTHROPIC_API_KEY
```

### 2. Run App
```bash
streamlit run app.py
```

### 3. Run Tests
```bash
pytest tests/
```

### 4. First Check-in
1. Accept disclaimer
2. Go to "Check-in" tab
3. Move slider to set mood (0-10)
4. Add optional notes
5. Click "Enregistrer Check-in"

### 5. Have a Conversation
1. Go to "Conversation" tab
2. Type a message
3. Wait for Serene's streaming response
4. View history on right side

### 6. View Insights
1. Go to "Dashboard" tab
2. See mood chart with selector
3. View conversation activity
4. Read AI-generated insights (auto-cached)

