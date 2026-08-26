"""
Muhammad Hasnain — AI Security Master
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

# ─── SMTP ─────────────────────────────────────
SMTP_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "hassnainpasha001@gmail.com",
    "receiver_email": "hassnainpasha001@gmail.com",
    "app_password": "ixyl adjz hjwj lpod",
}

# ─── App ──────────────────────────────────────
app = FastAPI(
    title="MH.SEC — Muhammad Hasnain AI Security Portfolio",
    description="AI Security Master portfolio with intelligent conversational assistant.",
    version="4.0.0",
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

# ─── Knowledge Base ───────────────────────────
KB = {
    "name": "Muhammad Hasnain",
    "title": "AI Security Master",
    "email": "hassnainpasha001@gmail.com",
    "linkedin": "https://www.linkedin.com/in/muhammad-hasnain-28840b382/",
    "github": "https://github.com/HassnainKhan001",
}

# ─── Conversation Sessions ────────────────────
SESSIONS: dict = {}

# ─── Models ───────────────────────────────────
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

# ─── Guardrail ────────────────────────────────
OFF_TOPIC = [
    "recipe", "cook", "movie", "song", "weather", "sports", "football",
    "cricket", "joke", "poem", "capital of", "calculate", "math problem",
    "translate", "news", "history of", "president", "celebrity"
]

WORK_KEYS = [
    "hasnain", "muhammad", "you", "your", "work", "project", "skill",
    "service", "audit", "llm", "red team", "prompt", "injection", "rag",
    "security", "supply chain", "python", "fastapi", "experience", "hire",
    "contact", "portfolio", "case study", "jailbreak", "safetensors",
    "who", "what", "how", "tell me", "hello", "hi", "hey", "help",
    "can you", "do you", "are you", "price", "cost", "rate", "available",
    "threat", "vulnerability", "owasp", "mitre", "nist", "adversarial",
    "model", "ai", "machine learning", "neural", "vector", "pipeline"
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
            f"Nice to meet you, {name}! 👋 I'm Hasnain's AI assistant. What would you like to know about his AI security work?",
            f"Hey {name}! Great to have you here. Ask me anything about Hasnain's security expertise!",
            f"Cool, {name}! I'm here to tell you all about Hasnain's AI security mastery. What's on your mind?"
        ])

    greeting_name = f" {name}" if name else ""

    # ── Greeting ──────────────────────────────
    if re.search(r"\b(hi|hello|hey|sup|howdy|greetings|yo)\b", q):
        return random.choice([
            f"Hey{greeting_name}! 👋 Welcome! I'm the AI assistant for Muhammad Hasnain — AI Security Master. What would you like to know?",
            f"Hello{greeting_name}! Great to see you here. Hasnain breaks AI systems before attackers do. Curious how? Ask away! 🔐",
            f"Hey{greeting_name}! I'm here to tell you everything about Hasnain's work in AI security. What's your question?"
        ])

    # ── Who is / Identity ─────────────────────
    if re.search(r"\b(who is|who are|about him|introduce|tell me about|what does he do)\b", q) or \
       re.search(r"\b(hasnain|muhammad)\b", q) and re.search(r"\b(who|what|about)\b", q):
        return random.choice([
            "Hasnain is an AI Security Master 🔐 — he breaks LLMs, finds prompt injections, audits RAG pipelines, and secures AI systems. 15+ audits done. 200+ vulnerabilities found. Want details on a specific area?",
            "Think of him as the guy who attacks AI systems *before* the bad guys do 😎 — LLM red teaming, jailbreak testing, supply chain defense. Pretty elite stuff. What would you like to know more about?",
            "Muhammad Hasnain = AI Security Master. He's found 200+ vulnerabilities, completed 15+ LLM audits, and has a 99.7% exploit block rate. Basically, your AI has a problem — he'll find it. 💪 Ask me more!"
        ])

    # ── What can you do / capabilities ───────
    if re.search(r"\b(what can|what do|capabilities|offer|services|what are)\b", q):
        return random.choice([
            "Hasnain offers 3 core services: 🔴 LLM Red Teaming, 📄 RAG Pipeline Audits, and 🛡️ AI Supply Chain Defense. All NDA-protected with full reports. Want details on any of these?",
            "He specializes in: attacking LLMs to find weaknesses, auditing RAG pipelines for injection risks, and verifying AI model integrity. Basically — if your AI has a vulnerability, he'll expose it. Which interests you?",
            "Think offensive AI security 🎯 — red teaming, jailbreak testing, prompt injection hunting, supply chain verification. Every engagement comes with a full written report. Want to know more?"
        ])

    # ── LLM Red Teaming ───────────────────────
    if re.search(r"\b(red team|jailbreak|llm|prompt inject|adversarial|attack|exploit)\b", q):
        return random.choice([
            "LLM Red Teaming is his bread and butter 🔥 — he uses PyRIT, Garak & custom fuzzers to break your AI with real attack scenarios. Found a jailbreak or injection? You'll know exactly what to fix. Want to start an audit?",
            "He actively tries to jailbreak your LLM 💀 — system prompt extraction, goal hijacking, guardrail bypass. Then gives you a full remediation roadmap. OWASP LLM01 aligned. Sound like what you need?",
            "Prompt injection, jailbreaks, training data extraction — Hasnain's done it all. He goes in as an attacker so you can defend properly. 99.7% exploit block rate post-fix. Want to talk about your system?"
        ])

    # ── RAG ───────────────────────────────────
    if re.search(r"\b(rag|vector|retrieval|pipeline|document|embedding|pinecone|qdrant|langchain)\b", q):
        return random.choice([
            "RAG pipelines are full of hidden injection risks 🚨 — Hasnain audits them end-to-end: vector DB auth, document payload poisoning, privilege escalation. Works with Pinecone, Qdrant, LangChain. Is your RAG stack secured?",
            "He's found critical bugs in RAG pipelines where documents could override system instructions — scary stuff 😬. His audit covers access control, ingestion security, and context overflow attacks. Want one for your system?",
            "RAG audit = checking if your documents can be weaponized against your own AI. Hasnain does this with precision. Covers Milvus, Qdrant, Pinecone, LangChain setups. Is your pipeline exposed?"
        ])

    # ── Supply Chain ──────────────────────────
    if re.search(r"\b(supply chain|model weight|safetensors|pickle|poison|backdoor|model integr)\b", q):
        return random.choice([
            "He checks if your model weights are safe 🔍 — SafeTensors vs unsafe Pickle deserialization, training set backdoor scanning, open-source model integrity. One bad model file = game over. Is yours verified?",
            "AI supply chain attacks are real and underestimated ⚠️. Hasnain scans model weights, dependency trees, and training data for poisoning vectors. OWASP LLM03-LLM05 aligned. Need a check?",
            "Unsafe Pickle files in model weights can mean arbitrary code execution 😱 — Hasnain caught this for a client. He runs full model integrity scans. Want yours audited?"
        ])

    # ── Projects / Case Studies ───────────────
    if re.search(r"\b(project|case study|case studies|audit|built|portfolio|work|example|show me)\b", q):
        return random.choice([
            "His top case studies: 🔴 Enterprise RAG Prompt Injection Audit | 🔍 AI Supply Chain Scanner | 🛡️ Nexus SecFlow Agent Engine | 🔒 Aura Guard Chatbot Defense. Each one NDA-protected with full reports. Want details on any?",
            "He's audited enterprise RAG pipelines, built model weight scanners, hardened multi-agent systems with RBAC, and defended chatbots against jailbreaks. All documented. Want to see what matched your use case?",
            "Real audits, real findings 💥 — RAG injection discovered, unsafe Pickle caught before deployment, 99.7% jailbreak block rate achieved. Solid track record. Which project sounds most relevant to you?"
        ])

    # ── Skills / Stack ────────────────────────
    if re.search(r"\b(skill|stack|tech|tool|expertise|use|toolchain|language|framework)\b", q):
        return random.choice([
            "His toolkit: PyRIT, Garak, Inspect AI, PickleScan, SafeTensors — all the offensive AI security tools. Plus Python, FastAPI, LangChain for building secure systems. OWASP LLM Top 10 + MITRE ATLAS aligned 🎯",
            "On the offensive side: PyRIT, Garak, custom fuzzers. On the defensive: SafeTensors verification, RBAC design, guardrail engineering. He covers both ends of the attack surface. What specifically are you looking for?",
            "Think red team tools meets developer skills 🔥 — PyRIT, Garak, Inspect AI for attacks; Python, FastAPI, LangChain for building. OWASP + MITRE ATLAS standards. Pretty complete stack."
        ])

    # ── Process / How it works ────────────────
    if re.search(r"\b(process|how|approach|steps|phases|method|audit work|what happens)\b", q):
        return random.choice([
            "Simple 4-step process 🎯: Recon & Surface Mapping → Adversarial Exploitation → Impact Assessment → Hardening + Report. You get a full written report at the end. Want to start?",
            "He maps your attack surface, hits it with real exploits, measures the damage, then fixes everything with a clear report 📋. NDA signed first, always. What system are you thinking about securing?",
            "Audit flow: 1️⃣ Map attack surface → 2️⃣ Run real attacks (injections, jailbreaks) → 3️⃣ Assess impact → 4️⃣ Fix + deliver report. Clean, professional, thorough. Sound right for your needs?"
        ])

    # ── Pricing / Cost ────────────────────────
    if re.search(r"\b(price|cost|rate|fee|how much|budget|quote|charge|affordable)\b", q):
        return random.choice([
            "Pricing depends on audit scope 💼 — LLM red team, RAG audit, or full AI architecture review. Reach out at hassnainpasha001@gmail.com and he'll send a custom proposal. He responds within 48 hours!",
            "No fixed prices — every engagement is scoped to your system 🎯. Drop a message at hassnainpasha001@gmail.com for a quote. Fast response, NDA included.",
            "Scope-based pricing 🔐. Tell him what you've got — LLM, RAG, agent system — and he'll send a tailored proposal. Email: hassnainpasha001@gmail.com. 48-hour response guarantee."
        ])

    # ── Hire / Contact / Availability ─────────
    if re.search(r"\b(hire|contact|available|reach|engage|email|work with|get in touch|start)\b", q):
        return random.choice([
            f"Hasnain is open for new engagements! 🚀 Shoot him an email at hassnainpasha001@gmail.com — he responds within 48 hours. All engagements are NDA-protected from day one.",
            f"Ready to go! ✅ Email hassnainpasha001@gmail.com or hit up the contact page. He'll get back within 48 hours with a scoped proposal.",
            f"He's available! Just email hassnainpasha001@gmail.com or connect on LinkedIn 🔗. 48-hour response SLA, full NDA, structured audit plan. Easy process."
        ])

    # ── Stats / Numbers ───────────────────────
    if re.search(r"\b(stats|numbers|track record|results|how many|success|achievements|credentials)\b", q):
        return random.choice([
            "The numbers: ✅ 15+ LLM Audits | 🐛 200+ Vulnerabilities Found | 🛡️ 99.7% Exploit Block Rate | 📅 5+ Years Dev Experience. Consistent. Reliable. Elite.",
            "15+ completed AI security audits, 200+ real vulnerabilities found, 99.7% block rate after remediation 💪. Not just promises — proven results.",
            "Track record speaks: 15 audits, 200+ bugs, 99.7% block rate post-fix. Every engagement NDA-protected with a full structured report. Real results 🔥"
        ])

    # ── Philosophy / Mindset ──────────────────
    if re.search(r"\b(philosophy|mindset|approach|how do you think|why|different|unique|edge)\b", q):
        return random.choice([
            "His edge? He was a developer first 💡 — so he attacks AI systems knowing exactly how they're built. That's why he finds what others miss. Attacker mindset, engineer precision.",
            "Think like the attacker, defend like the engineer 🧠 — that's Hasnain's philosophy. 5 years building software = knowing exactly where the bodies are buried in AI systems.",
            "He's not just a security tester — he's an ex-developer who switched to breaking things 😎. That combo is rare and powerful. Finds vulnerabilities that pure security folks miss."
        ])

    # ── Small talk / thanks ───────────────────
    if re.search(r"\b(thanks|thank you|awesome|great|nice|cool|perfect|love it|impressive)\b", q):
        return random.choice([
            "Glad I could help! 😊 Anything else you'd like to know about Hasnain's work?",
            "Anytime! 🙌 Feel free to ask anything else about Hasnain's AI security expertise.",
            "Happy to! If you're thinking about an audit, just say the word 🔐"
        ])

    # ── How are you ───────────────────────────
    if re.search(r"\b(how are you|how r u|you good|you okay)\b", q):
        return random.choice([
            "Doing great, thanks for asking! 😄 I'm here all day to tell you about Hasnain's AI security work. What's on your mind?",
            "All systems secure 🟢 Ready to help! Ask me about Hasnain's audits, services, or how to work with him.",
        ])

    # ── Default / Fallback ────────────────────
    return random.choice([
        f"Good question{greeting_name}! I can tell you about Hasnain's LLM red teaming, RAG audits, supply chain defense, pricing, or how to get started. What interests you? 🔐",
        f"I'm specifically here to chat about Hasnain's AI security expertise{greeting_name} 😊 — try asking about his projects, skills, or how to hire him!",
        f"Hmm, I'm not sure I caught that{greeting_name}. Ask me about Hasnain's audits, capabilities, case studies, or contact info and I'll give you the full picture! 🎯"
    ])


# ─── API Routes ───────────────────────────────

@app.get("/api/health", tags=["System"])
async def health_check():
    return {
        "status": "ONLINE",
        "system": "MH.SEC",
        "version": "4.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

@app.post("/api/chat", tags=["Assistant"])
async def chat_endpoint(payload: ChatPayload):
    """Conversational AI Assistant — Hasnain's work only."""
    msg = payload.message.strip()
    if not msg:
        return {"response": "Hey! Ask me anything about Hasnain's AI Security work 🔐"}

    if not is_work_related(msg):
        return {
            "response": "I'm Hasnain's dedicated AI Security assistant 🔐 — I only know about his work, audits, and security expertise. What would you like to know about that?"
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
            "message": "I'm Hasnain's AI Security assistant 🔐 — I only discuss his work. Ask about his audits, skills, or how to hire him!",
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
        f"Budget: {payload.mission_budget}\n"
        f"Directive: {payload.project_directive}\n"
        f"---------------------------------------\n\n"
    )
    try:
        with open("inquiries.log", "a", encoding="utf-8") as f:
            f.write(log_entry)
    except OSError:
        logger.warning("Local logging failed.")

    try:
        msg = MIMEText(log_entry)
        msg['Subject'] = f"New Portfolio Inquiry: {payload.commander_name}"
        msg['From'] = SMTP_CONFIG["sender_email"]
        msg['To'] = SMTP_CONFIG["receiver_email"]
        with smtplib.SMTP(SMTP_CONFIG["smtp_server"], SMTP_CONFIG["smtp_port"]) as server:
            server.starttls()
            server.login(SMTP_CONFIG["sender_email"], SMTP_CONFIG["app_password"])
            server.send_message(msg)
        logger.info("Email delivered.")
    except Exception as e:
        logger.error(f"SMTP failed: {e}")


@app.post("/api/contact", tags=["Contact"])
async def submit_contact(payload: ContactPayload):
    await send_email_notification(payload)
    return {
        "ok": True, "status": "RECEIVED",
        "message": f"Thanks {payload.commander_name}! Hasnain will get back to you within 48 hours. All information is strictly NDA-protected. 🔐"
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
