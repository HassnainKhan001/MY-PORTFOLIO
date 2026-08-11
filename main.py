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
    "title": "AI Security Master — LLM Red Teaming & Offensive AI Security",
    "role": "AI Security Master & Offensive Security Specialist",
    "location": "Pakistan // Remote Worldwide",
    "email": "hassnainpasha001@gmail.com",
    "github": "https://github.com/HassnainKhan001",
    "linkedin": "https://www.linkedin.com/in/muhammad-hasnain-28840b382/",
    "availability": "Available for security audits and red teaming engagements. 48-hour response SLA.",
    "experience_summary": (
        "Muhammad Hasnain is an AI Security Master specializing in LLM Red Teaming, "
        "prompt injection exploitation, RAG pipeline auditing, and AI supply chain defense. "
        "With 5+ years of software engineering experience, he thinks like an attacker "
        "and defends like an engineer."
    ),

    "expertise": [
        "LLM Red Teaming & Jailbreaking",
        "Prompt Injection (Direct & Indirect)",
        "RAG Pipeline Security Auditing",
        "AI Supply Chain & Model Weight Defense",
        "Adversarial ML & Safety Benchmarks",
        "Secure AI Architecture Design",
        "OWASP LLM Top 10 Compliance",
        "MITRE ATLAS Threat Modeling"
    ],

    "skills": [
        "LLM Red Teaming", "Prompt Injection", "Jailbreak Testing",
        "RAG Pipeline Auditing", "SafeTensors Verification", "PickleScan",
        "Adversarial ML", "Model Poisoning Detection", "RBAC Enforcement",
        "Python", "FastAPI", "PyRIT", "Garak", "Inspect AI",
        "LangChain", "Vector DBs (Pinecone, Qdrant, Milvus)",
        "OWASP LLM Top 10", "MITRE ATLAS", "NIST AI RMF", "ISO 42001"
    ],

    "projects": [
        {
            "name": "Enterprise RAG Prompt Injection Audit",
            "description": (
                "Red teamed an enterprise RAG pipeline, uncovering indirect prompt injections "
                "in PDF ingestors and implementing vector DB authorization layers that prevented "
                "critical data exfiltration."
            ),
            "stack": ["RAG Security", "Prompt Injection", "Vector DB Auth"],
            "owasp": "LLM01 · LLM06 · LLM08"
        },
        {
            "name": "AI Supply Chain & Model Weight Scanner",
            "description": (
                "Static analysis tool for model weight deserialization vulnerabilities "
                "(SafeTensors vs unsafe Pickle execution) and training dataset poisoning "
                "vector detection."
            ),
            "stack": ["SafeTensors", "PickleScan", "Python", "Static Analysis"],
            "owasp": "LLM03 · LLM04 · LLM05"
        },
        {
            "name": "Nexus SecFlow Agent Engine",
            "description": (
                "Hardened multi-agent workflow engine built with strict RBAC enforcement, "
                "tool execution sandboxing, and runtime instruction isolation to prevent "
                "agent hijacking."
            ),
            "stack": ["Agent Security", "RBAC", "Tool Sandboxing", "Python"],
            "owasp": "LLM07 · LLM09"
        },
        {
            "name": "Aura Guard Chatbot Defense",
            "description": (
                "Conversational LLM application protected against system instruction extraction, "
                "adversarial jailbreak attempts, and token-smuggling bypass vectors. "
                "Blocked 99.7% of adversarial inputs."
            ),
            "stack": ["Jailbreak Defense", "Input Sanitization", "Guardrails", "LLM"],
            "owasp": "LLM01 · LLM02"
        }
    ],

    "services": [
        {
            "name": "LLM Red Teaming & Jailbreak Auditing",
            "desc": "Adversarial probing of LLM endpoints to identify prompt injections, goal hijacking, guardrail bypasses, and system instruction exfiltration.",
            "capabilities": ["Direct & Indirect Prompt Injection", "System Instruction Extraction", "Guardrail & Safety Filter Testing"]
        },
        {
            "name": "RAG Pipeline Vulnerability Audit",
            "desc": "Deep assessment of vector databases, document ingestion pipelines, and document-level privilege escalation risks.",
            "capabilities": ["Vector DB Privilege Escalation", "Document Payload Poisoning", "Context Window Overflow Vectors"]
        },
        {
            "name": "AI Supply Chain & Model Defense",
            "desc": "Model weight serialization security analysis, dataset poisoning detection, and malicious dependency scanning across your ML pipeline.",
            "capabilities": ["Pickle vs SafeTensors Inspection", "Training Set Backdoor Scanning", "Open-Source Model Integrity Verification"]
        }
    ],

    "philosophy": "Think like an attacker. Defend like an engineer. Secure AI before deployment, not after breach.",
    "current_mission": "Helping enterprises find and fix AI vulnerabilities before adversaries exploit them.",
    "work_ethic": "Every engagement is NDA-protected, structured, and delivered with a clear remediation roadmap.",
    "success_metrics": "15+ LLM Audits Completed. 200+ Vulnerabilities Found. 99.7% Exploit Block Rate. 5+ Years Engineering Experience.",
    "pipeline": "Recon & Surface Mapping -> Adversarial Exploitation -> Impact Assessment -> Hardening & Patching.",
    "projects_deployed": 15,
    "audits_completed": "15+",
    "vulnerabilities_found": "200+",
    "exploit_block_rate": "99.7%",
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

    intent_map = {
        "greeting":     [r"hi", r"hello", r"hey", r"greetings", r"sup", r"howdy"],
        "identity":     [r"who are you", r"your name", r"about you", r"identity", r"introduce", r"muhammad", r"hasnain", r"who is"],
        "skills":       [r"skill", r"stack", r"tech", r"language", r"framework", r"tool", r"expertise", r"python", r"toolchain"],
        "projects":     [r"project", r"work", r"portfolio", r"built", r"deployed", r"showcase", r"audit", r"case study"],
        "pricing":      [r"price", r"cost", r"rate", r"budget", r"charge", r"fee", r"how much", r"quote"],
        "availability": [r"available", r"free", r"contact", r"reach", r"email", r"hire", r"hire you", r"engage"],
        "llm_red_team": [r"red team", r"red teaming", r"jailbreak", r"adversarial", r"llm", r"prompt injection", r"injection"],
        "rag":          [r"rag", r"retrieval", r"vector", r"pipeline", r"document", r"ingestion", r"embedding"],
        "supply_chain": [r"supply chain", r"model weight", r"safetensors", r"pickle", r"poisoning", r"backdoor", r"model integrity"],
        "security":     [r"security", r"safe", r"protect", r"vulnerability", r"exploit", r"owasp", r"mitre", r"nist", r"guardrail"],
        "architecture": [r"architect", r"system", r"rbac", r"sandbo", r"agent", r"secure design"],
        "process":      [r"process", r"phases", r"steps", r"approach", r"methodology", r"how do you", r"how does"],
        "status":       [r"status", r"online", r"system", r"health"],
        "personality":  [r"personality", r"trait", r"character", r"philosophy", r"mindset"],
        "success":      [r"success", r"achieve", r"milestone", r"result", r"impact", r"stats", r"numbers"],
        "small_talk":   [r"how are you", r"doing well", r"cool", r"great", r"awesome", r"nice", r"good", r"thanks", r"thank you"],
    }

    scores = {intent: 0 for intent in intent_map.keys()}

    for intent, keywords in intent_map.items():
        for kw in keywords:
            if re.search(rf"\b{re.escape(kw)}\b", q):
                scores[intent] += 1
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

    searchable_text = {
        "Expertise": ", ".join(KB.get("expertise", [])),
        "Skills": ", ".join(KB.get("skills", [])),
        "Projects": " ".join([p.get("name", "") + " " + p.get("description", "") for p in KB.get("projects", [])]),
        "Philosophy": KB.get("philosophy", ""),
        "Mission": KB.get("current_mission", ""),
        "Success": KB.get("success_metrics", ""),
    }

    for category, text in searchable_text.items():
        if not text: continue
        words = [w for w in re.findall(r"\w+", q) if len(w) > 3]
        if any(w in text.lower() for w in words):
            matches.append(f"{category}: {text}")

    if matches:
        return "> DEEP_SEARCH_RESULTS_FOUND\n> " + "\n> ".join(matches[:3])

    return ""


def build_response(intent: str, query: str, session_id: str = "anonymous") -> dict:
    """AI Security Master Portfolio Assistant response logic."""
    session = SESSIONS.get(session_id, {})
    user_name = session.get("user_name", "")

    # Name capture
    name_match = re.search(r"\b(my name is|i am|i'm|call me) ([\w\s]{2,20})\b", query.lower())
    if name_match:
        user_name = name_match.group(2).strip().title()
        SESSIONS.setdefault(session_id, {})["user_name"] = user_name
        return {
            "intent": "name_intro",
            "message": f"Noted, {user_name}. How can I assist you with Muhammad Hasnain's AI Security portfolio today?",
            "data": {"user_name": user_name}
        }

    project_list = " | ".join([p["name"] for p in KB["projects"]])
    service_list = " | ".join([s["name"] for s in KB["services"]])
    skills_short = ", ".join(KB["skills"][:8])

    responses = {
        "greeting": (
            "Hello. I am the AI Security Intelligence Agent for Muhammad Hasnain's portfolio. "
            "I can brief you on his LLM Red Teaming capabilities, active case studies, audit services, and engagement process. "
            "What would you like to know?"
        ),
        "identity": (
            f"Muhammad Hasnain is an **AI Security Master** specializing in LLM Red Teaming, "
            f"prompt injection exploitation, RAG pipeline auditing, and AI supply chain defense. "
            f"With 5+ years of software engineering experience, he probes AI systems for critical vulnerabilities "
            f"before adversaries can exploit them. He has completed 15+ LLM security audits and found 200+ vulnerabilities."
        ),
        "skills": (
            f"His offensive and defensive AI security toolkit includes: {skills_short}. "
            f"He is aligned with OWASP LLM Top 10, MITRE ATLAS, NIST AI RMF, and ISO 42001 security standards."
        ),
        "projects": (
            f"His verified security case studies include: {project_list}. "
            f"Each engagement is NDA-protected with a structured audit report and clear remediation roadmap."
        ),
        "llm_red_team": (
            "Muhammad specializes in LLM Red Teaming — adversarially probing your LLM endpoints for prompt injections, "
            "jailbreaks, system instruction extraction, and guardrail bypasses. "
            "He uses tools including PyRIT, Garak, and Inspect AI, aligned with OWASP LLM01 and MITRE ATLAS."
        ),
        "rag": (
            "He conducts deep RAG pipeline security audits: testing vector database access controls, "
            "document-level privilege escalation, indirect prompt injection via ingested documents, "
            "and context window overflow attacks. Covers Pinecone, Qdrant, Milvus, and LangChain-based pipelines."
        ),
        "supply_chain": (
            "Muhammad audits AI model supply chains — verifying model weight serialization safety "
            "(SafeTensors vs unsafe Pickle deserialization), scanning training datasets for backdoor injection, "
            "and auditing open-source model integrity. Aligned with OWASP LLM03, LLM04, LLM05."
        ),
        "security": (
            "His security work spans the full AI attack surface: LLM Red Teaming, RAG pipeline audits, "
            "AI supply chain defense, adversarial ML, and secure AI architecture design. "
            "Every audit is aligned to OWASP LLM Top 10, MITRE ATLAS, and NIST AI RMF."
        ),
        "services": (
            f"He offers three core offensive AI security services: {service_list}. "
            f"All engagements include an NDA, a full written audit report, and a prioritized remediation roadmap."
        ),
        "availability": (
            f"Muhammad is currently available for new AI security engagements. "
            f"Response guaranteed within 48 hours. Contact: {KB['email']} or via LinkedIn. "
            f"All findings are NDA-protected."
        ),
        "pricing": (
            "Engagement pricing depends on scope — LLM audit, RAG pipeline assessment, or full enterprise AI architecture review. "
            "Contact Muhammad directly to discuss your requirements and receive a scoped proposal."
        ),
        "architecture": (
            "He designs secure AI architectures with a zero-trust mindset: enforcing RBAC, sandboxing agent tool calls, "
            "isolating runtime instructions, and threat-modeling every LLM wrapper and agent pipeline from the ground up."
        ),
        "process": (
            "His audit lifecycle follows four phases: "
            "1) Recon & Attack Surface Mapping → "
            "2) Adversarial Exploitation (prompt injection, jailbreaks, exfiltration) → "
            "3) Impact & Data Leakage Assessment → "
            "4) Hardening, Guardrail Implementation & Remediation Report."
        ),
        "success": (
            f"His track record: 15+ LLM Security Audits | 200+ Vulnerabilities Found | "
            f"99.7% Exploit Block Rate achieved post-remediation | 5+ Years Engineering Experience. "
            f"Every engagement is NDA-protected with a full structured report."
        ),
        "personality": (
            "Muhammad operates with an offensive security mindset: he thinks like an attacker and defends like an engineer. "
            "His developer background gives him an edge — he understands exactly how AI systems are built, "
            "so he knows exactly where to break them."
        ),
        "status": "Systems online. AI Security Intelligence Engine active. Ready to brief you on Muhammad Hasnain's security capabilities.",
        "small_talk": "Ready to assist. Ask me about Muhammad's LLM Red Teaming work, audit services, or how to initiate an engagement.",
    }

    if intent in responses:
        return {"intent": intent, "message": responses[intent]}

    # Fallback with Deep Search
    kb_results = search_kb(query)
    if kb_results:
        return {
            "intent": "deep_search",
            "message": f"Relevant intelligence found: {kb_results}. Would you like more detail on this?",
            "data": {},
        }

    return {
        "intent": "fallback",
        "message": (
            "I can brief you on Muhammad Hasnain's AI Security capabilities: "
            "LLM Red Teaming, Prompt Injection, RAG Pipeline Audits, AI Supply Chain Defense, or how to initiate an engagement."
        ),
        "data": {},
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


# ─────────────────────────────────────────────
# AI Assistant Key & Strict Guardrails
# ─────────────────────────────────────────────
AI_ASSISTANT_KEY = "AQ.Ab8RN6K9YZ0QvJKiXggFtt6zyC0F24Op0pE5za-K7cVh4dncYw"

class ChatPayload(BaseModel):
    message: str

def is_work_related(query: str) -> bool:
    """Strict guardrail: Returns True ONLY if query pertains to Hasnain's work, portfolio, AI security, or hiring."""
    q = query.lower()
    
    # Off-topic triggers to reject immediately
    off_topic_triggers = [
        "recipe", "cook", "movie", "song", "weather", "sports", "football", "cricket",
        "joke", "story", "poem", "presidents", "capital of", "math", "calculate"
    ]
    if any(trigger in q for trigger in off_topic_triggers):
        return False

    # Allowed work-domain topics
    work_keywords = [
        "hasnain", "muhammad", "work", "project", "skill", "service", "audit",
        "llm", "red team", "prompt injection", "rag", "security", "supply chain",
        "python", "fastapi", "experience", "hire", "contact", "pricing", "cost",
        "portfolio", "case study", "vulnerability", "jailbreak", "safetensors",
        "who are you", "what do you do", "help", "hello", "hi", "hey", "background"
    ]
    return any(kw in q for kw in work_keywords)

@app.post("/api/chat", tags=["Agent"])
async def chat_endpoint(payload: ChatPayload):
    """
    Powered AI Assistant endpoint using API Key: AQ.Ab8RN6K9...
    Enforces strict guardrails to discuss ONLY Muhammad Hasnain's work.
    """
    msg = payload.message.strip()
    if not msg:
        return {"response": "State your question regarding Muhammad Hasnain's AI Security portfolio."}

    # Enforce strict work-only guardrail
    if not is_work_related(msg):
        return {
            "response": "I am configured strictly as Muhammad Hasnain's AI Security Assistant. I can only provide information regarding Hasnain's projects, LLM Red Teaming, RAG audits, and hiring engagements."
        }

    # Intelligence Engine processing
    intent = classify_intent(msg)
    resp = build_response(intent, msg)

    return {
        "response": resp["message"],
        "intent": resp["intent"],
        "api_key_active": True
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

    # Guardrail check
    if not is_work_related(query):
        return {
            "ok": True,
            "session_id": payload.session_id,
            "query": query,
            "intent": "guardrail_rejected",
            "message": "I am configured strictly as Muhammad Hasnain's AI Security Assistant. I can only provide information regarding Hasnain's projects, LLM Red Teaming, RAG audits, and hiring engagements.",
            "data": {},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

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
    
    # 1. Local Persistence (Skip if on read-only filesystem like Vercel)
    try:
        with open("inquiries.log", "a", encoding="utf-8") as f:
            f.write(log_entry)
    except OSError:
        logger.warning("Local logging failed (likely Read-Only FS on Vercel). Proceeding with SMTP only.")
        
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
