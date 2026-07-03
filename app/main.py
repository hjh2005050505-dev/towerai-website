from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .agent import tower_agent
from .database import init_db, save_lead
from .knowledge_base import load_products, load_scenarios

app = FastAPI(title="塔外智能 TowerOS 企业智能体应用平台")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str

class LeadRequest(BaseModel):
    name: str = ""
    company: str = ""
    contact: str
    interest: str = ""
    message: str = ""

@app.on_event("startup")
def startup() -> None:
    init_db()

@app.get("/favicon.ico")
def favicon() -> Response:
    return Response(status_code=204)

@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request, "products": load_products(), "scenarios": load_scenarios(), "active": "home"})

@app.get("/product", response_class=HTMLResponse)
def product(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("product.html", {"request": request, "products": load_products(), "active": "product"})

@app.get("/scenarios", response_class=HTMLResponse)
def scenarios(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("scenarios.html", {"request": request, "scenarios": load_scenarios(), "active": "scenarios"})

@app.get("/agent", response_class=HTMLResponse)
def agent(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("agent.html", {"request": request, "active": "agent"})

@app.get("/about", response_class=HTMLResponse)
def about(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("about.html", {"request": request, "active": "about"})

@app.get("/api/scenarios")
def api_scenarios() -> dict[str, object]:
    return {"scenarios": load_scenarios()}

@app.post("/api/chat")
def api_chat(payload: ChatRequest) -> dict[str, object]:
    answer = tower_agent.reply(payload.message)
    return {"reply": answer.reply, "intent": answer.intent, "recommended": answer.recommended}

@app.post("/api/lead")
def api_lead(payload: LeadRequest) -> dict[str, object]:
    lead_id = save_lead(payload.name, payload.company, payload.contact, payload.interest, payload.message)
    return {"ok": True, "lead_id": lead_id}
