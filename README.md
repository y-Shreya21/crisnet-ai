# 🚨 CrisisNet AI

### Multi-Agent Disaster Response Intelligence System
**Transforming Fragmented Disaster Data into Actionable Emergency Decisions**

---

CrisisNet AI is an advanced multi-agent disaster response platform designed to assist emergency operations centers, government agencies, and humanitarian groups. By orchestrating specialized, collaborative agents, the system aggregates, verifies, and analyzes real-time weather feeds, disaster headlines, and public infrastructure data to formulate risk threat scores and coordinate tactical action plans.

Built as a submission for the **Kaggle AI Agents Capstone Project**, CrisisNet AI showcases the integration of **Google Agent Development Kit (ADK)**, **Model Context Protocol (MCP)**, **OpenStreetMap (OSM) resource intelligence**, and a custom visual analytics **Streamlit dashboard**.

---

## 🎯 Key Capabilities & Features

1. **Multi-Agent Orchestration:** Deploys a team of 6 collaborative agents managing Weather, News, Resource location mapping, Risk analysis, and Action plans, overseen by a central Coordinator.
2. **Google ADK Integration (ADK 2.0):** Agents are fully converted into `google.adk` compatible nodes, enabling seamless agent-to-agent delegation, prompt instructions management, and graph-based `Workflow` execution.
3. **Model Context Protocol (MCP) Server:** Features a built-in FastMCP server registering tools (`weather_tool`, `news_tool`, `maps_tool`) allowing third-party tools, IDEs (Cursor/VSCode), and LLM clients to fetch live disaster data directly.
4. **Real-World Resource GIS Discovery:** Integrates with OpenStreetMap via the **Overpass API** to dynamically discover nearby hospitals, fire stations, and shelters within a 10km radius of any target coordinates.
5. **Robust Security & Safety Guard:** Includes a sanitization and validation layer (`prompt_guard.py` & `validator.py`) to block command injections, path traversals, SQL exploits, and template injection attempts.
6. **Streamlit Command Center:** A dark-themed, glassmorphic visual dashboard that maps assets dynamically and exports compiled report files.

---

## 🏗️ System Architecture

```text
       User Request (Location & Coordinates)
                       ↓
         ┌───────────────────────────┐
         │  Security Validation      │ ← Input Sanitization & Prompt Guard
         └───────────────────────────┘
                       ↓
         ┌───────────────────────────┐
         │     Coordinator Agent     │ ← Manages execution flow
         └───────────────────────────┘
                       ↓
   ┌───────────────────┼───────────────────┐
   ↓                   ↓                   ↓
┌──────────────┐   ┌────────────┐   ┌──────────────┐
│Weather Agent │   │ News Agent │   │Resource Agent│
└──────────────┘   └────────────┘   └──────────────┘
   │                   │                   │
   │ (Open-Meteo API)  │ (NewsAPI)         │ (OSM / Overpass)
   └───────────────────┼───────────────────┘
                       ↓
         ┌───────────────────────────┐
         │    Risk Assessment Agent  │ ← Evaluates weather & news indicators
         └───────────────────────────┘
                       ↓
         ┌───────────────────────────┐
         │ Emergency Planning Agent  │ ← Formulates action protocols
         └───────────────────────────┘
                       ↓
         ┌───────────────────────────┐
         │   Final Output Verifier   │ ← Validates schema integrity
         └───────────────────────────┘
                       ↓
         Report Compiler & Download / Streamlit Map
```

---

## 📁 Repository Structure

```text
crisisnet-ai/
│
├── Agents/
│   ├── coordinator.py         # Main synchronous & ADK orchestrator
│   ├── adk_agents.py          # Google ADK agent and workflow declarations
│   ├── weather_agent.py       # Weather data analyzer
│   ├── news_agent.py          # News headline analyzer
│   ├── resource_agent.py      # OSM Overpass API intelligence mapping
│   ├── risk_agent.py          # Safety threat scoring calculator
│   └── emergency_planner.py   # Tactical recommendation planner
│
├── Security/
│   ├── validator.py           # DataType, coordinate limits, & shape validation
│   └── prompt_guard.py        # Prompt injection & shell injection protection
│
├── Tools/
│   ├── weather_tool.py        # Open-Meteo REST service connection
│   └── news_tool.py           # NewsAPI REST service connection
│
├── tests/
│   ├── test_agents.py         # Agent behavior and fallback unit tests
│   └── test_security.py       # Validation and malicious filters tests
│
├── app.py                     # Console demo execution
├── mcp_server.py              # Model Context Protocol (FastMCP) server
├── streamlit_app.py           # Snowflake/Streamlit Dashboard web client
├── requirements.txt           # Project dependencies
├── DEPLOYMENT.md              # Installation and deployment runbook
├── .env.example               # Config variable templates
└── README.md                  # Main project overview
```

---

## ⚡ Quick Start & Execution

For detailed setup, environment keys configuration, and running the FastMCP server, see [DEPLOYMENT.md](file:///Users/shreyayadav/crisenet/crisnet-ai/DEPLOYMENT.md).

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure keys
```bash
cp .env.example .env
# Edit .env to add your GOOGLE_API_KEY
```

### 3. Run the visual dashboard
```bash
streamlit run streamlit_app.py
```

### 4. Run the automated test suite
```bash
python3 -m unittest discover -s tests
```

---

## 🏆 Kaggle Capstone Submission Details

- **Track:** Agents for Good
- **Mandatory Criteria Met:**
  - **Multi-Agent System:** 6 agents communicating and delegating tasks.
  - **Google ADK:** Native integration of Google GenAI SDK and ADK 2.0 Graph Workflow.
  - **MCP Server:** FastMCP integration exposing tools for IDEs and LLM clients.
  - **Security Features:** Multi-level sanitization filters and output schema validators.
  - **Deployability:** Packaged for Streamlit Cloud with offline fallback capabilities.
  - **Agent Skills / Tool Usage:** Connects dynamically with Weather, News, and OpenStreetMap APIs.

---

## 👩‍💻 Author
- **Shreya Yadav**
- *Machine Learning Engineer | AI Research Enthusiast*
