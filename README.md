# MH.SYS — AI ORCHESTRATOR Portfolio

> **Muhammad Hasnain** — Neural Hub OS v2.4.0 — FastAPI + Static HTML Portfolio  
> 🔗 [GitHub](https://github.com/HassnainKhan001) · [LinkedIn](https://www.linkedin.com/in/muhammad-hasnain-28840b382/)

---

## 🚀 Quick Start

### Option 1 — Double-click launcher (Recommended)
```
Double-click:  start.bat
```
This installs dependencies, starts the server, and opens your browser automatically.

---

### Option 2 — Manual (PowerShell / CMD)
```powershell
# 1. Install dependencies (one-time)
pip install -r requirements.txt

# 2. Start the server
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

Then open → **http://localhost:8080**

---

## 📁 Project Structure

```
Portfolio.Developer/
│
├── main.py              ← FastAPI app + AI Agent logic
├── requirements.txt     ← Python dependencies
├── start.bat            ← One-click launcher
│
├── index.html           ← Homepage / Hero
├── projects.html        ← Deployed Infrastructure
├── services.html        ← Core Capabilities
├── diagnostic.html      ← AI Chat Interface  ← calls /api/agent
├── neural-net.html      ← Technical Architecture
├── contact.html         ← Neural Uplink       ← calls /api/contact
└── index.css            ← Shared design system
```

---

## 🔌 API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `GET`  | `/` | Homepage |
| `GET`  | `/api/health` | System health check |
| `GET`  | `/api/kb` | Full knowledge base (JSON) |
| `POST` | `/api/agent` | AI agent — natural language query |
| `POST` | `/api/contact` | Contact form submission |
| `GET`  | `/api/docs` | Swagger UI |

### Agent Query Example
```bash
curl -X POST http://localhost:8080/api/agent \
  -H "Content-Type: application/json" \
  -d '{"query": "What are your skills?", "session_id": "test"}'
```

### Supported Query Intents
| Query Keywords | Intent |
|----------------|--------|
| `hi`, `hello` | Greeting |
| `skills`, `stack`, `tech` | Skills matrix |
| `projects`, `deployed` | Project manifest |
| `price`, `cost`, `budget` | Pricing tiers |
| `available`, `hire` | Availability |
| `automation`, `n8n` | Automation systems |
| `ai`, `chatbot`, `rag` | AI systems |
| `architecture`, `microservice` | Software architecture |
| `process`, `pipeline` | Engineering pipeline |
| `status`, `uptime` | System status |

---

## 🛠 Requirements

- Python 3.9+
- pip

Dependencies installed automatically by `start.bat`:
```
fastapi
uvicorn[standard]
python-multipart
pydantic
```
"# MY-PORTFOLIO" 
