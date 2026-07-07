# 🎬 CrisisNet AI - Submission Demo & Video Script

This document provides a structured walkthrough script, narration guide, and demo scenarios designed for judges evaluating the Kaggle AI Agents Capstone submission.

---

## 📽️ Demo Video Structure (5-Minute Script)

### Segment 1: The Hook & Project Vision (0:00 - 0:45)
* **Visual:** Visual Streamlit dashboard main page with the title "CrisisNet AI" and a dark EOC aesthetic.
* **Narrator Script:**
  > "Welcome. During a natural disaster, emergency responders have a major problem: fragmented information. Weather details, news alerts, and hospital locations are scattered across disparate web APIs. 
  > CrisisNet AI solves this by building a cooperative multi-agent disaster intelligence system. It acts as a real-time Emergency Operations Center, orchestrating weather analyzers, news scrapers, and GIS coordinates mapping agents to instantly generate critical disaster intelligence reports."

### Segment 2: Multi-Agent Local Orchestration (0:45 - 2:00)
* **Visual:** Narrator types `Assam` into the input bar and clicks **Analyze Disaster**. Show the spinner.
* **Narrator Script:**
  > "Let's enter a target location: 'Assam'. When we click 'Analyze Disaster', the system launches Phase 0: Location Intelligence Agent, resolving 'Assam' into geographic coordinates. 
  > Instantly, downstream workers trigger tool calls: our Weather Agent queries live atmospheric conditions; the News Agent pulls verified local flood reports; and the Resource Agent maps critical infrastructure within a 25km radius."

### Segment 3: Threat Analytics & Mapping UI (2:00 - 3:15)
* **Visual:** Point to the color-coded Plotly Gauge Chart showing the risk score and explainable reasoning. Zoom in on the Interactive GIS Map showing the red disaster marker and surrounding hospitals/shelters.
* **Narrator Script:**
  > "Here, our Risk Assessment Agent evaluates weather metrics, news indicators, and resource scarcity, scoring the threat severity. For Assam, the score is elevated to 'HIGH' or 'CRITICAL', triggering specific emergency plan actions from our Planning Agent. 
  > Responders can view nearby facilities on our interactive GIS map, complete with legends and address lists, and download compiled Markdown, PDF, and Text reports for offline tactical dispatch."

### Segment 4: Security Shield & Google ADK (3:15 - 4:30)
* **Visual:** Scroll to the Security Health Dashboard indicating active validation checkpoints. Toggle the radio button in the sidebar to "Google ADK Graph Workflow" and enter an API Key.
* **Narrator Script:**
  > "CrisisNet AI enforces zero-trust security. The EOC Security panel displays real-time checks validating coordinates boundaries and blocking prompt injections. 
  > Next, we show Google ADK integration. By toggling to the live ADK mode, the coordinator delegates execution across vertex workflow nodes, utilizing Gemini models to orchestrate agent communication graph-style. If the live connection fails or is rate-limited, the system falls back seamlessly to local multi-agent rule orchestration."

### Segment 5: Conclusion & Social Value (4:30 - 5:00)
* **Visual:** Return to the full overview page and show the download buttons.
* **Narrator Script:**
  > "CrisisNet AI bridges the gap between raw web feeds and rescue actions. It leverages Google ADK, MCP tools, and Overpass APIs to save critical response minutes. This is CrisisNet AI—AI Agents for Good. Thank you."

---

## 📝 Hands-On Judging Test Scenarios

To test the system immediately, input the following strings in the Streamlit dashboard:

### Scenario 1: Flood Alert in Northeast India
* **Location Input:** `Assam` or `Guwahati`
* **Expected Result:** High/Critical threat level, high precipitation levels, local flood news headlines, maps plotting nearby medical colleges and community centers.

### Scenario 2: Central Region Offline Test
* **Location Input:** `Delhi` or `Mumbai`
* **Expected Result:** Medium threat index, lower precipitation indicators, hospital counts mapped in central NCR/Maharashtra regions.

### Scenario 3: Extreme Input Injection Test
* **Location Input:** `Assam; DROP TABLE incidents;` or `{{7*7}}`
* **Expected Result:** The security shield logs the request, filters malicious SQL characters or template characters, and sanitizes input to avoid SQL Injection or Remote Code Execution.
