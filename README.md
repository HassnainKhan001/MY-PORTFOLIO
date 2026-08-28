# Muhammad Hasnain — Software Engineer & Developer Portfolio

> **Muhammad Hasnain** — Full-Stack Developer & Software Engineer Portfolio  
> 🔗 [GitHub](https://github.com/HassnainKhan001) · [LinkedIn](https://www.linkedin.com/in/muhammad-hasnain-28840b382/)

---

## 🚀 Quick Start

### Option 1 — Double-click launcher
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
portfolio/
│
├── main.py              ← FastAPI backend + AI Assistant logic
├── requirements.txt     ← Python dependencies
├── start.bat            ← One-click launcher
│
├── index.html           ← Homepage / Hero & Highlights
├── projects.html        ← Project Showcase & Case Studies
├── services.html        ← Capabilities & Services
├── neural-net.html      ← System Architecture & Lifecycle
├── diagnostic.html      ← Interactive AI Portfolio Assistant
├── contact.html         ← Contact & Collaboration Form
└── index.css            ← Sleek dark modern design system
```

---

## 🔌 API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `GET`  | `/` | Homepage |
| `GET`  | `/api/health` | System health check |
| `GET`  | `/api/kb` | Knowledge base (JSON) |
| `POST` | `/api/chat` | AI portfolio assistant |
| `POST` | `/api/contact` | Contact form submission |
| `GET`  | `/api/docs` | Swagger UI |

---

## 🛠 Tech Stack

- **Backend**: Python 3.9+, FastAPI, Uvicorn, Pydantic
- **Frontend**: HTML5, Modern CSS (Glassmorphism + Dark Slate), Vanilla JavaScript
- **Styling**: Google Fonts (Plus Jakarta Sans, Inter, JetBrains Mono), Material Symbols
