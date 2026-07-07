# 🚀 CrisisNet AI - Deployment & Operation Guide

This document details instructions for installing dependencies, executing components, setting up the Model Context Protocol (MCP) server, and deploying to Streamlit Cloud.

---

## 📋 Table of Contents
1. [Prerequisites](#-prerequisites)
2. [Local Installation](#-local-installation)
3. [Running the Streamlit Dashboard](#-running-the-streamlit-dashboard)
4. [Using the MCP Server](#-using-the-mcp-server)
5. [Testing the Codebase](#-testing-the-codebase)
6. [Streamlit Cloud Deployment](#-streamlit-cloud-deployment)

---

## ⚙️ Prerequisites
Ensure you have the following installed locally:
- Python 3.10 or higher
- pip (Python package installer)

---

## 🛠️ Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/crisisnet-ai.git
   cd crisisnet-ai
   ```

2. **Install core requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Keys:**
   Copy the environment template and customize:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and supply:
   - `GOOGLE_API_KEY`: Required for live Google ADK reasoning and workflows.
   - `NEWS_API_KEY`: NewsAPI developer credential key.

---

## 🖥️ Running the Streamlit Dashboard

Streamlit offers a visual, dark-themed dashboard mapping emergency facilities and listing actions.

Run the dashboard:
```bash
streamlit run streamlit_app.py
```
This runs the local server at `http://localhost:8501`.

---

## 🔌 Using the MCP Server

The project includes an MCP-compliant server using Anthropic's **FastMCP**. This server registers four key tools:
1. `location_tool(location_name)` (converts textual name to Lat/Lon coordinates)
2. `weather_tool(latitude, longitude)`
3. `news_tool(location)`
4. `maps_tool(location, latitude, longitude)` (real-world Overpass OSM querying in a 25km radius)

### Launch Server
Start the server in stdio transport mode:
```bash
python3 mcp_server.py
```

### Hooking into Clients

#### 1. Claude Desktop
Add this config to your Claude Desktop config file (typically `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "crisisnet-ai": {
      "command": "python3",
      "args": ["/absolute/path/to/crisisnet-ai/mcp_server.py"]
    }
  }
}
```

#### 2. Cursor IDE
- Open Settings -> Features -> MCP.
- Click **+ Add New MCP Server**.
- Name: `CrisisNet AI`
- Type: `command`
- Command: `python3 /absolute/path/to/crisisnet-ai/mcp_server.py`

---

## 🧪 Testing the Codebase

Run the comprehensive unit and integration test suite:
```bash
python3 -m unittest discover -s tests
```

---

## ☁️ Streamlit Cloud Deployment

1. **Push your code** to a public GitHub repository.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/) and log in with your GitHub account.
3. Click **New app** and select your repository, branch (`main`), and main file path (`streamlit_app.py`).
4. Click **Advanced settings...** to add Secrets (Environment variables):
   ```toml
   GOOGLE_API_KEY = "your_real_google_api_key_here"
   NEWS_API_KEY = "e5de58fcd7614443ab5365a0c13eb20b"
   ```
5. Click **Deploy!** Streamlit will provision the container, install packages, and serve the application online.
