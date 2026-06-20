# 🚨 CrisisNet AI

### Multi-Agent Disaster Response Intelligence System

**Transforming Disaster Data into Actionable Decisions**

CrisisNet AI is a multi-agent disaster response intelligence platform designed to support emergency management teams, government agencies, and humanitarian organizations during natural disasters. The system leverages specialized AI agents to collect, analyze, and synthesize information from multiple sources, enabling faster decision-making and more effective disaster response planning.

Built as part of the Kaggle AI Agents: Intensive Vibe Coding Capstone Project, CrisisNet AI demonstrates how agent-based architectures can improve situational awareness, risk assessment, and emergency coordination during high-impact events such as floods, cyclones, earthquakes, and wildfires.

---

## 🌍 Problem Statement

Natural disasters generate large volumes of fragmented information across weather services, news channels, emergency alerts, geographic information systems, and public reports. Emergency responders often struggle to consolidate this information quickly enough to make informed decisions.

Key challenges include:

* Fragmented disaster intelligence across multiple platforms
* Delayed response due to manual information gathering
* Difficulty assessing real-time risk levels
* Limited visibility into available emergency resources
* Inefficient coordination during rapidly evolving situations

Traditional systems provide information but rarely transform it into actionable response plans.

---

## 💡 Solution

CrisisNet AI functions as a virtual Emergency Operations Center powered by multiple collaborating AI agents.

Instead of relying on a single AI assistant, the platform uses specialized agents responsible for weather monitoring, news intelligence, resource assessment, and risk evaluation. A central Coordinator Agent orchestrates communication between agents and generates a comprehensive disaster response report.

The platform converts scattered disaster-related information into structured intelligence, helping stakeholders make faster and more informed decisions.

---

## 🏗️ System Architecture

The platform follows a modular multi-agent architecture.

### Coordinator Agent

Responsible for:

* Task orchestration
* Agent communication
* Workflow management
* Response aggregation

### Weather Intelligence Agent

Responsible for:

* Weather monitoring
* Rainfall analysis
* Severe weather alerts
* Environmental risk indicators

### News Intelligence Agent

Responsible for:

* Disaster-related news analysis
* Situation monitoring
* Affected area identification
* Incident summarization

### Resource Planning Agent

Responsible for:

* Shelter identification
* Hospital availability assessment
* Emergency resource tracking
* Infrastructure awareness

### Risk Assessment Agent

Responsible for:

* Severity estimation
* Disaster impact analysis
* Risk scoring
* Priority assessment

### Emergency Planning Agent

Responsible for:

* Response plan generation
* Action recommendation
* Resource allocation guidance
* Decision-support reporting

---

## ⚙️ Current Workflow

```text
User Query
    ↓
Coordinator Agent
    ↓
 ┌─────────────────┐
 │ Weather Agent   │
 └─────────────────┘
    ↓
 ┌─────────────────┐
 │ News Agent      │
 └─────────────────┘
    ↓
 ┌─────────────────┐
 │ Resource Agent  │
 └─────────────────┘
    ↓
 ┌─────────────────┐
 │ Risk Agent      │
 └─────────────────┘
    ↓
Emergency Planning Agent
    ↓
Disaster Response Report
```

---

## 🔒 Security Features

The platform incorporates security-focused design principles:

* Input validation
* Prompt injection protection
* Controlled tool access
* Agent isolation
* Output verification

These safeguards help improve reliability and reduce the risk of unsafe agent behavior.

---

## 🧠 Agent Technologies

This project demonstrates several modern AI agent concepts:

* Multi-Agent Systems
* Agent Orchestration
* Tool-Augmented Agents
* Modular Agent Design
* Secure Agent Architectures
* Decision-Support Systems

Future versions will integrate:

* Google Agent Development Kit (ADK)
* Model Context Protocol (MCP)
* Real-time weather APIs
* News intelligence services
* Geographic information systems

---

## 🛠️ Technology Stack

### Programming Language

* Python

### AI & Agent Frameworks

* Google ADK (Planned)
* MCP (Planned)

### Backend

* Python
* REST APIs

### Frontend

* Streamlit (Planned)

### Data Sources

* Weather APIs
* News APIs
* Mapping Services

### Version Control

* Git
* GitHub

---

## 📁 Project Structure

```text
crisisnet-ai/
│
├── Agents/
│   ├── coordinator.py
│   ├── weather_agent.py
│   ├── news_agent.py
│   ├── resource_agent.py
│   ├── risk_agent.py
│   └── emergency_planner.py
│
├── Security/
│   ├── validator.py
│   └── prompt_guard.py
│
├── app.py
├── requirements.txt
├── README.md
└── architecture.png
```

---

## 🚀 Getting Started

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/crisisnet-ai.git
```

Navigate to the project directory:

```bash
cd crisisnet-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

---

## 📊 Sample Output

```text
CRISISNET AI DISASTER REPORT

Location: Assam

Risk Level: HIGH
Risk Score: 8.7/10

Affected Areas:
• Kamrup
• Barpeta

Available Resources:
• Shelters: 12
• Hospitals: 5
• Rescue Teams: 8

Recommended Actions:
1. Open emergency shelters
2. Deploy rescue teams
3. Issue evacuation alerts
4. Stock medical supplies
5. Monitor weather continuously
```

---

## 🎯 Future Enhancements

* Real-time weather intelligence
* Live disaster monitoring dashboard
* Satellite imagery analysis
* Autonomous response planning
* Multi-modal disaster detection
* Google ADK integration
* MCP-enabled tool ecosystem
* Streamlit deployment

---

## 🏆 Kaggle Capstone Submission

Track: **Agents for Good**

CrisisNet AI demonstrates how collaborative AI agents can assist humanitarian operations by transforming fragmented disaster information into actionable emergency intelligence.

The project showcases the practical application of multi-agent systems, tool-augmented reasoning, secure AI architectures, and real-world decision-support workflows.

---

## 👩‍💻 Author

**Shreya Yadav**

B.Tech Computer Science and Engineering
Machine Learning Engineer | AI Research Enthusiast
