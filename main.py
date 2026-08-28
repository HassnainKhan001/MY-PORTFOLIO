"""
Muhammad Hasnain — Software Engineer & Developer Portfolio
Portfolio Backend + Conversational AI Assistant
"""

import re
import random
import logging
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ─── Logging ──────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# ─── SMTP Configuration ───────────────────────
SMTP_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "hassnainpasha001@gmail.com",
    "receiver_email": "hassnainpasha001@gmail.com",
    "app_password": "ixyl adjz hjwj lpod",
}

# ─── App Definition ───────────────────────────
app = FastAPI(
    title="Muhammad Hasnain — Developer Portfolio",
    description="Software Developer & Engineer portfolio with conversational AI assistant.",
    version="4.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

@app.on_event("startup")
async def startup_event():
    logger.info("Portfolio Engine // INITIALIZED")
    print("\n[+] SERVER IS LIVE: http://127.0.0.1:8000")
    print("[*] Press CTRL+C to shutdown.\n")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent

# ─── Knowledge Base ───────────────────────────
KB = {
    "name": "Muhammad Hasnain",
    "title": "Software Engineer & Full-Stack Developer",
    "email": "hassnainpasha001@gmail.com",
    "linkedin": "https://www.linkedin.com/in/muhammad-hasnain-28840b382/",
    "github": "https://github.com/HassnainKhan001",
    "core_skills": ["Python", "FastAPI", "JavaScript", "HTML5", "Modern CSS", "REST APIs", "AI Integrations", "Workflow Automation"],
}

# ─── Conversation Sessions ────────────────────
SESSIONS: dict = {}

# ─── Request Models ───────────────────────────
class AgentQuery(BaseModel):
    query: str
    session_id: str = "anonymous"

class ChatPayload(BaseModel):
    message: str

class ContactPayload(BaseModel):
    commander_name: str
    return_email: str
    mission_budget: str = ""
    project_directive: str

# ─── Guardrails ───────────────────────────────
OFF_TOPIC = [
    "recipe", "cook", "movie", "song", "weather", "sports", "football",
    "cricket", "joke", "poem", "capital of", "calculate", "math problem",
    "translate", "news", "history of", "president", "celebrity"
]

WORK_KEYS = [
    "hasnain", "muhammad", "you", "your", "work", "project", "skill",
    "service", "web", "frontend", "backend", "python", "fastapi", "experience", "hire",
    "contact", "portfolio", "case study", "api", "rest", "database",
    "who", "what", "how", "tell me", "hello", "hi", "hey", "help",
    "can you", "do you", "are you", "price", "cost", "rate", "available",
    "architecture", "automation", "workflow", "model", "ai", "software",
    "javascript", "html", "css"
]

def is_work_related(q: str) -> bool:
    q_low = q.lower()
    if any(t in q_low for t in OFF_TOPIC):
        return False
    return any(k in q_low for k in WORK_KEYS)

# ─── Conversational Engine ────────────────────
def get_response(msg: str, session_id: str = "anonymous") -> str:
    q = msg.lower().strip()
    session = SESSIONS.setdefault(session_id, {})
    name = session.get("name", "")

    # ── Name capture ──────────────────────────
    nm = re.search(r"\b(?:my name is|i am|i'm|call me)\s+([\w]+)", q)
    if nm:
        name = nm.group(1).title()
        session["name"] = name
        return random.choice([
            f"Nice to meet you, {name}! 👋 I'm Hasnain's AI portfolio assistant. What would you like to know about his projects or skills?",
            f"Hey {name}! Great to meet you. Ask me anything about Hasnain's work and experience!",
            f"Glad to connect, {name}! I can walk you through Hasnain's technical background, projects, or available services."
        ])

    greeting_name = f" {name}" if name else ""

    # ── Greeting ──────────────────────────────
    if re.search(r"\b(hi|hello|hey|sup|howdy|greetings|yo)\b", q):
        return random.choice([
            f"Hey{greeting_name}! 👋 Welcome! I'm the assistant for Muhammad Hasnain. How can I help you today?",
            f"Hello{greeting_name}! Glad to see you here. Feel free to ask about Hasnain's projects, tech stack, or services.",
            f"Hey{greeting_name}! I can share details on Hasnain's development experience, featured work, and contact channels. What's on your mind?"
        ])

    # ── Who is / Identity ─────────────────────
    if re.search(r"\b(who is|who are|about him|introduce|tell me about|what does he do)\b", q) or \
       re.search(r"\b(hasnain|muhammad)\b", q) and re.search(r"\b(who|what|about)\b", q):
        return random.choice([
            "Muhammad Hasnain is a Software Engineer & Full-Stack Developer specializing in building high-performance web applications, scalable backend APIs with FastAPI & Python, and intelligent software workflows.",
            "Hasnain builds modern digital products — from responsive frontends to robust async Python backends and AI-powered workflow automations. Check out the Projects page to see his work!",
            "Muhammad Hasnain is a passionate developer focused on clean code, scalable architecture, and delivering impactful solutions for teams and businesses."
        ])

    # ── Services / Capabilities ───────────────
    if re.search(r"\b(what can|what do|capabilities|offer|services|what are)\b", q):
        return random.choice([
            "Hasnain offers full-stack web development, backend & REST API engineering (FastAPI/Python), AI & LLM integration, and custom workflow automation. Check out the Services page for a full breakdown!",
            "Core services include: 💻 Full-Stack Web Development, ⚡ High-Throughput REST APIs, 🤖 AI & Conversational Integrations, and 🔄 Workflow Automations. Which of these interests you?",
            "Whether you need an MVP built from scratch, a high-performance backend, or smart automation pipelines, Hasnain can help bring your concept to production."
        ])

    # ── Projects ──────────────────────────────
    if re.search(r"\b(project|projects|built|portfolio|work|example|show me|case study)\b", q):
        return random.choice([
            "Featured projects include: 🚀 This interactive FastAPI Portfolio Assistant, 📊 The Interactive Architecture Topology Visualizer, and 📬 The Async Notification & Contact Engine. Visit the Projects page to explore all of them!",
            "Hasnain has built multiple web platforms, custom APIs, and AI integrations. Check out the Projects page for direct demos and links to source code.",
            "You can explore live demos and technical breakdowns directly on the Projects page. Are you interested in web apps, APIs, or AI tools?"
        ])

    # ── Skills / Stack ────────────────────────
    if re.search(r"\b(skill|skills|stack|tech|tool|tools|language|framework)\b", q):
        return random.choice([
            "Hasnain's core tech stack: Python, FastAPI, JavaScript, Modern CSS, HTML5, RESTful APIs, Pydantic, Uvicorn, AsyncIO, and AI integrations (OpenAI/LLM pipelines).",
            "Key skills: Backend API development with Python/FastAPI, modern responsive web UI development, database integrations, asynchronous task handling, and smart workflow automation.",
            "He focuses on modern, performant technologies — primarily Python (FastAPI/AsyncIO) on the backend and clean, modular modern JavaScript/CSS on the frontend."
        ])

    # ── Hire / Contact / Availability ─────────
    if re.search(r"\b(hire|contact|available|reach|engage|email|work with|get in touch|start)\b", q):
        return random.choice([
            f"Hasnain is open for new opportunities and freelance projects! Reach out via email at hassnainpasha001@gmail.com or fill out the Contact page form.",
            f"You can easily connect with Hasnain! Drop a message at hassnainpasha001@gmail.com or via LinkedIn. He typically responds within 24–48 hours.",
            f"Ready to collaborate? Head over to the Contact page or send an email directly to hassnainpasha001@gmail.com to get started."
        ])

    # ── Pricing / Cost ────────────────────────
    if re.search(r"\b(price|cost|rate|fee|how much|budget|quote|charge|affordable)\b", q):
        return random.choice([
            "Project rates depend on scope, requirements, and timeline. Send a brief summary of your project to hassnainpasha001@gmail.com or via the Contact page for a custom quote!",
            "Pricing is tailored to the project needs — whether a full application, MVP prototype, or API integration. Get in touch on the Contact page to discuss details.",
        ])

    # ── Small talk / thanks ───────────────────
    if re.search(r"\b(thanks|thank you|awesome|great|nice|cool|perfect|love it|impressive)\b", q):
        return random.choice([
            "Glad I could help! 😊 Let me know if you have any other questions about Hasnain's work.",
            "You're welcome! Feel free to ask anything else or head over to the Contact page to get in touch.",
            "Happy to help! Have an awesome day! 🚀"
        ])

    # ── How are you ───────────────────────────
    if re.search(r"\b(how are you|how r u|you good|you okay)\b", q):
        return random.choice([
            "Doing great, thanks for asking! 😄 How can I assist you with Hasnain's portfolio today?",
            "All systems running smoothly! 🟢 Feel free to ask about Hasnain's skills, projects, or services.",
        ])

    # ── Fallback ──────────────────────────────
    return random.choice([
        f"Good question{greeting_name}! I can tell you about Hasnain's skills, featured projects, services, or how to contact him. What would you like to know?",
        f"I'm Hasnain's portfolio assistant 😊 — try asking about his tech stack, recent projects, or how to work together!",
        f"I'm here to help with questions about Hasnain's software development work. Feel free to explore the Projects or Contact page as well!"
    ])


# ─── API Routes ───────────────────────────────

@app.get("/api/health", tags=["System"])
async def health_check():
    return {
        "status": "ONLINE",
        "system": "MH.SYS",
        "version": "4.1.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

@app.get("/api/kb", tags=["KnowledgeBase"])
async def get_knowledge_base():
    return KB

@app.post("/api/chat", tags=["Assistant"])
async def chat_endpoint(payload: ChatPayload):
    """Conversational AI Assistant endpoint."""
    msg = payload.message.strip()
    if not msg:
        return {"response": "Hello! How can I assist you with Hasnain's portfolio today?"}

    if not is_work_related(msg):
        return {
            "response": "I'm Hasnain's portfolio assistant — I'm happy to chat about his development projects, skills, services, or how to work together. What would you like to explore?"
        }

    reply = get_response(msg)
    return {"response": reply}

@app.post("/api/agent", tags=["Assistant"])
async def agent_query(payload: AgentQuery):
    """Agent endpoint with session tracking."""
    query = payload.query.strip()
    if not query:
        return JSONResponse(status_code=400, content={"error": "Empty query."})

    if not is_work_related(query):
        return {
            "ok": True, "session_id": payload.session_id,
            "message": "I'm Hasnain's portfolio assistant. Ask me about his software development skills, projects, or how to hire him!",
            "intent": "guardrail", "data": {}, "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    reply = get_response(query, payload.session_id)
    return {
        "ok": True, "session_id": payload.session_id, "query": query,
        "message": reply, "intent": "conversational", "data": {},
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


async def send_email_notification(payload: ContactPayload):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"--- INQUIRY RECEIVED: {timestamp} ---\n"
        f"From: {payload.commander_name} <{payload.return_email}>\n"
        f"Subject/Budget: {payload.mission_budget}\n"
        f"Message: {payload.project_directive}\n"
        f"---------------------------------------\n\n"
    )
    try:
        with open("inquiries.log", "a", encoding="utf-8") as f:
            f.write(log_entry)
    except OSError:
        logger.warning("Local logging failed.")

    try:
        msg = MIMEText(log_entry)
        msg['Subject'] = f"Portfolio Inquiry from {payload.commander_name}"
        msg['From'] = SMTP_CONFIG["sender_email"]
        msg['To'] = SMTP_CONFIG["receiver_email"]
        with smtplib.SMTP(SMTP_CONFIG["smtp_server"], SMTP_CONFIG["smtp_port"]) as server:
            server.starttls()
            server.login(SMTP_CONFIG["sender_email"], SMTP_CONFIG["app_password"])
            server.send_message(msg)
        logger.info("Email delivered successfully.")
    except Exception as e:
        logger.warning(f"SMTP delivery note (may require local configuration): {e}")


@app.post("/api/contact", tags=["Contact"])
async def submit_contact(payload: ContactPayload):
    await send_email_notification(payload)
    return {
        "ok": True, "status": "RECEIVED",
        "message": f"Thank you, {payload.commander_name}! Hasnain has received your inquiry and will respond within 24–48 hours."
    }

@app.post("/api/contact/form", tags=["Contact"])
async def submit_contact_form(
    commander_name: str = Form(...),
    return_email: str = Form(...),
    mission_budget: str = Form(""),
    project_directive: str = Form(...),
):
    payload = ContactPayload(
        commander_name=commander_name,
        return_email=return_email,
        mission_budget=mission_budget,
        project_directive=project_directive,
    )
    return await submit_contact(payload)


# ─── HTML Pages ───────────────────────────────
HTML_PAGES = {
    "/":           "index.html",
    "/projects":   "projects.html",
    "/services":   "services.html",
    "/diagnostic": "diagnostic.html",
    "/neural-net": "neural-net.html",
    "/contact":    "contact.html",
}

for route, filename in HTML_PAGES.items():
    filepath = BASE_DIR / filename
    def make_handler(fp):
        async def handler():
            return FileResponse(fp, media_type="text/html")
        return handler
    app.add_api_route(
        path=route, endpoint=make_handler(filepath),
        methods=["GET"], response_class=HTMLResponse, tags=["Pages"],
    )

# ─── Static Assets (MUST be last) ─────────────
app.mount("/", StaticFiles(directory=str(BASE_DIR), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
