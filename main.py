"""
Muhammad Hasnain – AI ORCHESTRATOR
Portfolio + AI ORCHESTRATOR Backend
Run: uvicorn main:app --reload --port 8080
"""

import re
import json
import logging
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ─────────────────────────────────────────────
# App Setup
# ─────────────────────────────────────────────

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# EMAIL CONFIGURATION (REQUIRED FOR INBOX DELIVERY)
# ─────────────────────────────────────────────
# 1. Go to Google Account -> Security -> 2-Step Verification
# 2. Search for "App Passwords" and generate a new one.
# 3. Replace "PLACEHOLDER" with your 16-character App Password.
SMTP_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "hassnainpasha001@gmail.com",
    "receiver_email": "hassnainpasha001@gmail.com", # Your primary inbox
    "app_password": "ixyl adjz hjwj lpod", 
}
# ─────────────────────────────────────────────

app = FastAPI(
    title="MH.SYS – Muhammad Hasnain Portfolio",
    description="AI Automation Expert personal portfolio with integrated assistant backend.",
    version="3.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

@app.on_event("startup")
async def startup_event():
    logger.info("MH.SYS // Portfolio Engine // INITIALIZED")
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

# ─────────────────────────────────────────────
# Knowledge Base (Agent Brain)
# ─────────────────────────────────────────────

KB = {
    "name": "Muhammad Hasnain",
    "title": "AI Automation Expert & Software Developer",
    "role": "Official Assistant",
    "location": "Pakistan // Remote Worldwide",
    "email": "hassnainpasha001@gmail.com",
    "github": "https://github.com/HassnainKhan001",
    "linkedin": "https://www.linkedin.com/in/muhammad-hasnain-28840b382/",
    "availability": "Currently open for new projects. I'll get back to you within 24 hours.",
    "experience_summary": "He builds high-quality software and smart AI tools that help businesses grow and run more efficiently.",
    
    "expertise": [
        "Software Development",
        "AI Automation",
        "AI Chatbot Development",
        "Full AI Integration",
        "Intelligent Systems Architecture"
    ],

    "skills": [
        "JavaScript", "TypeScript", "Node.js", "React", "Next.js", "Python", 
        "REST APIs", "AI SDKs & LLM APIs", "Databases", "Cloud Integrations"
    ],

    "projects": [
        {
            "name": "Social Media Automation Bot",
            "description": "Automates messaging, workflows, customer interactions, and platform-based automation systems.",
            "stack": ["n8n", "Python", "API Integrations"]
        },
        {
            "name": "AI Portfolio Assistant",
            "description": "An intelligent conversational assistant designed to represent portfolio projects, technical skills, and services naturally.",
            "stack": ["FastAPI", "Python", "NLP"]
        },
        {
            "name": "CRM Workflow Automation",
            "description": "Automation system connecting APIs, customer workflows, CRMs, and business operations.",
            "stack": ["Node.js", "CRM APIs", "Automations"]
        },
        {
            "name": "AI Agent Systems",
            "description": "Multi-step AI systems capable of reasoning, automation, decision support, and intelligent task execution.",
            "stack": ["LangChain", "LLMs", "Agentic Frameworks"]
        }
    ],

    "services": [
        {
            "name": "Software Architecture",
            "desc": "Designing robust, scalable, and secure backend systems and high-performance frontend interfaces.",
            "capabilities": ["Software developed by AI coding", "Full AI integrated Software", "High Quality software designs"]
        },
        {
            "name": "Business Automation",
            "desc": "Replacing human latency with deterministic algorithmic workflows. Orchestrating complex API ecosystems.",
            "capabilities": ["AI-Powered Social Media & Business Automation", "Chatbot Development for business", "AI Solutions for Modern Businesses"]
        },
        {
            "name": "Custom AI Assistants",
            "desc": "Building smart conversational AI systems that turn business data into interactive experiences.",
            "capabilities": ["Turning Ideas Into Intelligent AI Products", "Conversational AI Developer", "Custom AI Assistant Developer"]
        }
    ],

    "philosophy": "Using smart AI and automation to solve business problems and improve efficiency.",
    "current_mission": "Helping businesses leverage AI to automate workflows and scale faster.",
    "work_ethic": "Atomic consistency over 1825+ days. Hard work is the baseline; excellence is the variable.",
    "success_metrics": "$2M+ operational value generated. 50+ successful deployments. 99.9% system reliability.",
    "pipeline": "AI Orchestration -> Process Optimization -> Intelligent Deployment.",
    "projects_deployed": 54,
    "automation_value": "$2.1M",
    "uptime": "99.98%",
    "experience_years": 5
}

# ─────────────────────────────────────────────
# Agent Engine
# ─────────────────────────────────────────────

# In-memory session storage (Memory Module)
SESSIONS = {}

class AgentQuery(BaseModel):
    query: str
    session_id: str = "anonymous"


def classify_intent(q: str) -> str:
    """Professional Semantic Engine using word boundaries to ensure accurate intent mapping."""
    q = q.lower()
    
    # Intent map with word-boundary sensitive keywords
    intent_map = {
        "greeting":     [r"hi", r"hello", r"hey", r"greetings", r"sup", r"howdy"],
        "identity":     [r"who are you", r"your name", r"about you", r"identity", r"introduce", r"muhammad", r"hasnain"],
        "skills":       [r"skill", r"stack", r"tech", r"language", r"framework", r"tool", r"code", r"expertise", r"python", r"javascript"],
        "projects":     [r"project", r"work", r"portfolio", r"built", r"deployed", r"showcase", r"working on", r"doing", r"current"],
        "pricing":      [r"price", r"cost", r"rate", r"budget", r"charge", r"fee", r"how much", r"quote"],
        "availability": [r"available", r"free", r"contact", r"reach", r"email", r"hire", r"hire you"],
        "automation":   [r"automat", r"n8n", r"make", r"zapier", r"workflow", r"pipeline", r"bot"],
        "ai":           [r"ai", r"chatbot", r"rag", r"llm", r"gpt", r"openai", r"agent", r"neural"],
        "architecture": [r"architect", r"system", r"microservice", r"scalab", r"backend", r"infra"],
        "process":      [r"process", r"phases", r"steps", r"approach", r"methodology"],
        "status":       [r"status", r"uptime", r"online", r"system", r"health", r"monitor"],
        "personality":  [r"personality", r"trait", r"character", r"vibe", r"philosophy", r"mindset"],
        "work_ethic":   [r"work ethic", r"consistency", r"hard work", r"disciplin", r"grit", r"grind"],
        "success":      [r"success", r"achieve", r"milestone", r"result", r"impact", r"value"],
        "roi":          [r"roi", r"return", r"overhead", r"money", r"save", r"value generation"],
        "security":     [r"security", r"safe", r"data", r"protect", r"privacy", r"encryption"],
        "partnership":  [r"partnership", r"partner", r"collaboration", r"long term", r"working together"],
        "industries":   [r"industries", r"sectors", r"real estate", r"fintech", r"ecommerce", r"saas"],
        "small_talk":   [r"how are you", r"doing well", r"cool", r"great", r"awesome", r"nice", r"interesting", r"good", r"thanks", r"thank you"],
    }
    
    scores = {intent: 0 for intent in intent_map.keys()}
    
    for intent, keywords in intent_map.items():
        for kw in keywords:
            # Use regex word boundaries \b to avoid substring matches
            if re.search(rf"\b{re.escape(kw)}\b", q):
                scores[intent] += 1
                # Boost multi-word matches
                if " " in kw:
                    scores[intent] += 2
                    
    best_intent = max(scores, key=scores.get)
    if scores[best_intent] > 0:
        return best_intent
        
    return "fallback"


def search_kb(query: str) -> str:
    """Deep search fallback: scan the KB for any relevant keywords in the user's query."""
    q = query.lower()
    matches = []
    
    # Flatten KB skills and projects for searching (using .get() for safety)
    searchable_text = {
        "Skills": ", ".join(KB.get("skills", [])),
        "Projects": " ".join([p.get("name", "") + " " + p.get("description", "") for p in KB.get("projects", [])]),
        "Philosophy": KB.get("philosophy", ""),
        "Work Ethic": KB.get("work_ethic", ""),
        "Success": KB.get("success_metrics", ""),
        "Current Mission": KB.get("current_mission", "")
    }
    
    for category, text in searchable_text.items():
        if not text: continue
        # Check if any word from query (longer than 3 chars) is in the category text
        words = [w for w in re.findall(r"\w+", q) if len(w) > 3]
        if any(w in text.lower() for w in words):
            matches.append(f"{category}: {text}")
            
    if matches:
        return "> DEEP_SEARCH_RESULTS_FOUND\n> " + "\n> ".join(matches[:3])
    
    return ""


def build_response(intent: str, query: str, session_id: str = "anonymous") -> dict:
    """Official AI Portfolio Assistant response logic."""
    session = SESSIONS.get(session_id, {})
    user_name = session.get("user_name", "")
    
    # Check if user is asking technical questions to adjust depth
    is_technical = any(word in query.lower() for word in ["stack", "architecture", "api", "backend", "scalability", "distributed"])
    
    # Name capture
    name_match = re.search(r"\b(my name is|i am|i'm|call me) ([\w\s]{2,20})\b", query.lower())
    if name_match:
        user_name = name_match.group(2).strip().title()
        SESSIONS.setdefault(session_id, {})["user_name"] = user_name
        return {
            "intent": "name_intro",
            "message": f"It's a pleasure to meet you, {user_name}. I've noted your identity. How can I assist you with Muhammad Hasnain's portfolio today?",
            "data": {"user_name": user_name}
        }

    responses = {
        "greeting": f"Hello! I am Hasnain's AI Assistant. I can help you with questions about his software projects, AI automation, and how he can help your business. How can I assist you today?",
        "identity": f"Muhammad Hasnain is an {KB['title']}. {KB['experience_summary']} He focuses on using smart AI to make businesses more efficient.",
        "skills": f"He specializes in software development and AI automation, using tools like {', '.join(KB['skills'][:4])} to build smart, scalable systems.",
        "projects": f"Muhammad has built several successful projects, including social media automation tools, business workflows, and custom AI assistants.",
        "services": f"His services include custom AI development, business automation, and building smart software that grows with your company.",
        "availability": f"He is currently taking on new projects! You can reach him at {KB['email']} or via LinkedIn to discuss your ideas.",
        "automation": "Yes, he builds automation systems that help businesses save time by handling repetitive tasks using AI and smart integrations.",
        "ai": "He specializes in building smart AI tools and assistants that can understand data and help automate complex business processes.",
        "architecture": "He builds systems with a focus on speed, reliability, and security, ensuring they can grow as your business grows.",
        "personality": "Muhammad is a professional and results-driven developer who values clear communication and high-quality work.",
        "success": "His projects have helped businesses automate their workflows and save hundreds of hours of manual work.",
        "roi": "Most of his AI and automation solutions pay for themselves quickly by reducing manual work and improving business efficiency.",
        "industries": "He has experience working with businesses in Real Estate, FinTech, E-commerce, and SaaS.",
        "status": "I'm online and ready to help! All systems are running smoothly.",
        "small_talk": "I'm doing great! How can I help you learn more about Muhammad's work today?",
    }

    # Special technical detail boost
    if is_technical and intent in ["skills", "projects", "architecture"]:
        if intent == "skills":
            responses["skills"] = f"His tech stack includes {', '.join(KB['skills'])}. He specializes in building AI pipelines and automated backend systems."
        elif intent == "architecture":
            responses["architecture"] = "He builds scalable software using a modern stack, microservices, and smart data search (RAG) for high performance."

    if intent in responses:
        return {"intent": intent, "message": responses[intent]}

    # Fallback with Deep Search
    kb_results = search_kb(query)
    if kb_results:
        return {
            "intent": "deep_search",
            "message": f"I've found some information related to your query: {kb_results}. Would you like more details on this?",
            "data": {},
        }

    return {
        "intent": "fallback",
        "message": "I don't have that information yet, but I can tell you about Muhammad's projects, automation services, or technical skills.",
        "data": {},
    }


# ─────────────────────────────────────────────
# API Routes
# ─────────────────────────────────────────────

@app.get("/api/health", tags=["System"])
async def health_check():
    """System health endpoint."""
    return {
        "status": "ONLINE",
        "system": "MH.SYS",
        "version": "2.4.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "latency_ms": 12,
        "node": "US-EAST-1",
    }


@app.get("/api/kb", tags=["Agent"])
async def get_knowledge_base():
    """Return the full public knowledge base (no sensitive data)."""
    return {
        "name": KB["name"],
        "title": KB["title"],
        "location": KB["location"],
        "skills": KB["skills"],
        "projects": KB["projects"],
        "services": KB["services"],
        "pipeline": KB["pipeline"],
        "stats": {
            "projects_deployed": KB["projects_deployed"],
            "automation_value": KB["automation_value"],
            "uptime": KB["uptime"],
            "experience_years": KB["experience_years"],
        },
    }


@app.post("/api/agent", tags=["Agent"])
async def agent_query(payload: AgentQuery):
    """
    Main AI agent endpoint.
    Accepts a natural language query and returns a structured response.
    """
    query = payload.query.strip()
    if not query:
        return JSONResponse(
            status_code=400,
            content={"error": "QUERY_EMPTY", "message": "No input received. State your directive."},
        )

    logger.info(f"Agent query | session={payload.session_id} | query={query!r}")

    intent = classify_intent(query)
    response = build_response(intent, query, payload.session_id)

    return {
        "ok": True,
        "session_id": payload.session_id,
        "query": query,
        "intent": response["intent"],
        "message": response["message"],
        "data": response.get("data", {}),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


# Pydantic model for JSON contact submissions
class ContactPayload(BaseModel):
    commander_name: str
    return_email: str
    mission_budget: str = ""
    project_directive: str


async def send_email_notification(payload: ContactPayload):
    """
    Handles email dispatch logic via SMTP. 
    Logs locally to inquiries.log and attempts to send to Gmail.
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"--- INQUIRY RECEIVED: {timestamp} ---\n"
        f"From: {payload.commander_name} <{payload.return_email}>\n"
        f"Budget: {payload.mission_budget}\n"
        f"Directive: {payload.project_directive}\n"
        f"---------------------------------------\n\n"
    )
    
    # 1. Local Persistence (Always save locally just in case)
    with open("inquiries.log", "a", encoding="utf-8") as f:
        f.write(log_entry)
        
    # 2. SMTP Delivery Attempt
    if SMTP_CONFIG["app_password"] == "PLACEHOLDER":
        logger.warning("SMTP skipped: App Password is still 'PLACEHOLDER'. Logging only to inquiries.log.")
        return

    try:
        msg = MIMEText(log_entry)
        msg['Subject'] = f"🚀 New Portfolio Inquiry: {payload.commander_name}"
        msg['From'] = SMTP_CONFIG["sender_email"]
        msg['To'] = SMTP_CONFIG["receiver_email"]

        with smtplib.SMTP(SMTP_CONFIG["smtp_server"], SMTP_CONFIG["smtp_port"]) as server:
            server.starttls() # Secure connection
            server.login(SMTP_CONFIG["sender_email"], SMTP_CONFIG["app_password"])
            server.send_message(msg)
            
        logger.info(f"TRANSMISSION_DELIVERED to {SMTP_CONFIG['receiver_email']} via SMTP.")
    except Exception as e:
        logger.error(f"SMTP Transmission Failed: {str(e)}")


@app.post("/api/contact", tags=["Contact"])
async def submit_contact(payload: ContactPayload):
    """
    Contact form submission handler.
    Accepts JSON body and logs/stores the inquiry.
    """
    logger.info(
        f"Contact submission | name={payload.commander_name!r} | "
        f"email={payload.return_email!r} | budget={payload.mission_budget!r}"
    )

    # 1. Deliver the "Email" (Notification)
    await send_email_notification(payload)

    # 2. Auto-agent response based on project directive
    intent = classify_intent(payload.project_directive)
    agent_resp = build_response(intent, payload.project_directive)

    return {
        "ok": True,
        "status": "TRANSMISSION_RECEIVED",
        "message": (
            f"Thanks for reaching out, {payload.commander_name}! "
            f"I've received your message and Muhammad will get back to you within 24 hours."
        ),
        "agent_preview": agent_resp["message"],
        "received_at": datetime.utcnow().isoformat() + "Z",
    }


@app.post("/api/contact/form", tags=["Contact"])
async def submit_contact_form(
    commander_name: str = Form(...),
    return_email: str = Form(...),
    mission_budget: str = Form(""),
    project_directive: str = Form(...),
):
    """HTML form POST fallback (application/x-www-form-urlencoded)."""
    payload = ContactPayload(
        commander_name=commander_name,
        return_email=return_email,
        mission_budget=mission_budget,
        project_directive=project_directive,
    )
    result = await submit_contact(payload)
    return result


@app.get("/JARVIS.webp", tags=["Assets"])
async def get_jarvis_asset():
    """Serves the user's JARVIS blueprint image."""
    img_path = BASE_DIR / "JARVIS.webp"
    return FileResponse(img_path)


# ─────────────────────────────────────────────
# Static Page Routes (explicit HTML endpoints)
# ─────────────────────────────────────────────

HTML_PAGES = {
    "/":             "index.html",
    "/projects":     "projects.html",
    "/services":     "services.html",
    "/diagnostic":   "diagnostic.html",
    "/neural-net":   "neural-net.html",
    "/contact":      "contact.html",
}

for route, filename in HTML_PAGES.items():
    filepath = BASE_DIR / filename

    # Build a closure to capture filepath correctly
    def make_handler(fp):
        async def handler():
            return FileResponse(fp, media_type="text/html")
        return handler

    app.add_api_route(
        path=route,
        endpoint=make_handler(filepath),
        methods=["GET"],
        response_class=HTMLResponse,
        tags=["Pages"],
    )


# ─────────────────────────────────────────────
# Mount Static Assets (CSS, images, fonts, etc.)
# Must come LAST so API routes take priority
# ─────────────────────────────────────────────

app.mount("/", StaticFiles(directory=str(BASE_DIR), html=True), name="static")


# ─────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
