# 🎭 Broadway Researcher

An intelligent multi-agent system that researches Broadway shows and provides comprehensive reports with reviews, ratings, and ticket purchasing recommendations. Built with Tavily Search API for real-time web research and OpenAI for intelligent analysis.

## 🎯 Motivation

Broadway ticket research is fragmented across multiple sources. This system consolidates reviews, ratings, and ticket information into a single, actionable report—helping theatergoers make informed decisions quickly.

## 🏗️ Architecture

### How It Works - Multi-Agent Flow

```
Input: "Hamilton"
    │
    ├─→ Agent 1: Validate show name
    │   ├─ Corrects spelling
    │   └─ Returns: "Hamilton" (verified)
    │
    ├─→ Agent 2: Search reviews & ratings
    │   ├─ Uses Tavily API to find reviews
    │   └─ Returns: Summary of critic ratings
    │
    ├─→ Agent 3: Search ticket options
    │   ├─ Uses Tavily API to find vendors
    │   └─ Returns: Ticket purchasing recommendations
    │
    ├─→ Agent 4: Get show image
    │   └─ Returns: Show poster/image URL
    │
    ├─→ Agent 5: Create TLDR report (for UI)
    │   └─ Returns: 20-line summary
    │
    └─→ Agent 6: Create extended report (for download)
        └─ Returns: Detailed research document
            │
            ▼
    Output: UI shows TLDR + Image
            Download button provides extended report
```

## 🛠️ Tech Stack

### Core Technologies
- **Streamlit**: Modern web interface
- **Tavily API**: Real-time web search for reviews, ratings, and ticket information
- **OpenAI GPT-4.1**: Intelligent analysis, summarization, and report generation
- **LangChain**: LLM integration and prompt management
- **Python 3.8+**: Backend implementation

### API Usage
- **Tavily**: Search engine for real-time Broadway show data
  - Reviews and ratings search
  - Ticket vendor information
  - Image retrieval
- **OpenAI**: Language model for analysis
  - Name standardization
  - Content summarization
  - Report generation

## 📦 Project Structure

```
broadway-researcher/
├── user_interface.py              # Streamlit web UI
├── main.py                         # CLI orchestrator
├── requirements.txt                # Python dependencies
├── .env                            # API keys (create this)
├── agents/
│   ├── standardize_name.py        # Agent 1: Name validation
│   ├── ratings_agent.py           # Agent 2: Reviews search
│   ├── tickets_agent.py          # Agent 3: Ticket search
│   ├── image_agent.py            # Agent 4: Image retrieval
│   ├── compile_report.py         # Agent 5: TLDR report
│   └── extended_report_agent.py  # Agent 6: Extended report
└── README.md                      
```

## 🎨 Design Rationale

### Agent Architecture
Each agent has a single, focused responsibility:
- **Separation of Concerns**: Each agent handles one specific task
- **Modularity**: Easy to test, maintain, and extend
- **Reusability**: Agents can be composed in different workflows

### Two Report Versions
- **TLDR (UI)**: Quick, scannable overview for fast decision-making
- **Extended (Download)**: Comprehensive research document for detailed planning

## 🔮 Future Improvements Ideas

- [ ] Integrate seat quality recommendations
- [ ] Cache frequently searched shows
- [ ] Add comparison feature (compare 2-3 shows)
- [ ] Add price alerts and notifications
- [ ] Integration with calendar and booking systems

## 📊 Metrics & Success

**Key Performance Indicators:**
- Search accuracy: Validates show name correctly
- Report relevance: Provides actionable ticket purchasing guidance
- User satisfaction: Clear, concise reports under 20 lines for UI
