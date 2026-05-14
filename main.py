"""
Muhammad Hasnain – AI ORCHESTRATOR
Portfolio + AI ORCHESTRATOR Backend
Run: uvicorn main:app --reload --port 8080
"""

import re
import json
import logging
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

app = FastAPI(
    title="MH.SYS – Muhammad Hasnain Portfolio",
    description="AI ORCHESTRATOR personal portfolio with integrated agent backend.",
    version="2.4.0",
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
    "title": "Full AI Integrated Software Developer & Automation Engineer",
    "role": "Official AI Portfolio Assistant",
    "location": "Pakistan // Remote Worldwide",
    "email": "hassnainpasha001@gmail.com",
    "github": "https://github.com/HassnainKhan001",
    "linkedin": "https://www.linkedin.com/in/muhammad-hasnain-28840b382/",
    "availability": "Open to new missions. Response within 24h.",
    "experience_summary": "He has made many high-quality software projects, specializing in full AI-integrated solutions that drive business efficiency.",
    
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
            "name": "AI Neural Agents",
            "desc": "Building smart conversational AI systems that turn business data into interactive experiences.",
            "capabilities": ["Turning Ideas Into Intelligent AI Products", "Conversational AI & Automation Developer", "Custom AI Assistant & Automation Developer"]
        }
    ],

    "philosophy": "Orchestrating intelligence to solve human inefficiency through sovereign logic systems.",
    "current_mission": "Acting as the intelligent digital representative of Muhammad Hasnain.",
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
    
    # Flatten KB skills and projects for searching
    searchable_text = {
        "Skills": ", ".join(KB["skills"]),
        "Projects": " ".join([p["name"] + " " + p["description"] for p in KB["projects"]]),
        "Philosophy": KB["philosophy"],
        "Work Ethic": KB["work_ethic"],
        "Success": KB["success_metrics"],
        "Current Mission": KB["current_mission"]
    }
    
    for category, text in searchable_text.items():
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
        "greeting": f"Hello! I am the official AI Portfolio Assistant for Muhammad Hasnain. I can provide details on his software development, AI automation, and chatbot expertise. How can I help you?",
        "identity": f"Muhammad Hasnain is a {KB['title']}. {KB['experience_summary']} He focuses on orchestrating intelligence to solve human inefficiency through sovereign logic systems.",
        "skills": f"He specializes in software development, AI automation, and AI chatbot development, utilizing a modern stack of {', '.join(KB['skills'][:4])} to build full AI-integrated systems.",
        "projects": f"Muhammad has made many software projects including Social Media Automation Bots, CRM workflows, and AI Agent systems. His work focuses on seamless AI integration and performance.",
        "services": f"Muhammad specializes in AI chatbot development, workflow automation, WhatsApp/Telegram integration, and full-stack AI applications.",
        "availability": f"He is currently open to new professional opportunities and missions. You can reach him at {KB['email']} or connect via LinkedIn.",
        "automation": "Yes, he develops automation systems that integrate APIs, CRMs, chat platforms, and AI tools to reduce manual work and improve operational efficiency.",
        "ai": "He builds AI agents and assistants capable of reasoning, multi-step automation, and intelligent task execution for complex business needs.",
        "architecture": "He follows a modern architecture focusing on API integrations, microservices, and scalable cloud deployments to ensure system reliability.",
        "personality": "Muhammad is a disciplined and results-oriented engineer who believes in orchestrating intelligence to solve human inefficiency.",
        "success": "His systems have generated significant operational value by automating complex workflows across various industries.",
        "roi": "By reducing manual overhead and optimizing processes, his AI solutions typically deliver a strong return on investment within the first few months.",
        "industries": "He has experience working across sectors like Real Estate, FinTech, E-commerce, and SaaS.",
        "status": "I am online and operating at peak capacity. All systems related to Muhammad's portfolio are nominal.",
        "small_talk": "I'm doing great. As Muhammad's digital representative, I'm always ready to discuss his latest innovations in AI.",
    }

    # Special technical detail boost
    if is_technical and intent in ["skills", "projects", "architecture"]:
        if intent == "skills":
            responses["skills"] = f"His full stack includes {', '.join(KB['skills'])}. He specializes in RAG pipelines, FastAPI backends, and autonomous agent orchestration."
        elif intent == "architecture":
            responses["architecture"] = "He architected the Nexus OS and Jarvis systems using event-driven logic, microservices, and vector-database grounding for high-precision AI retrieval."

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
        "message": "I don’t have that information yet. However, I can tell you about Muhammad's AI projects, automation services, or technical skills.",
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

    # Auto-agent response based on project directive
    intent = classify_intent(payload.project_directive)
    agent_resp = build_response(intent, payload.project_directive)

    return {
        "ok": True,
        "status": "TRANSMISSION_RECEIVED",
        "message": (
            f"Handshake successful, Commander {payload.commander_name}. "
            f"Your directive has been logged. Expect a response within 24 hours."
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


@app.get("/jarvis_robotics.png", tags=["Assets"])
async def get_jarvis_img():
    """Serves the generated robotics image from the app data directory."""
    img_path = r"C:\Users\SAQIB COMPUTERS\.gemini\antigravity\brain\398448e3-0470-4d47-87da-aa4997ce884d\jarvis_robotics_system_1778729655143.png"
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
