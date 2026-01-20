from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from models import TopicRequest, ResumeRequest, StudyRequest, InterviewQuestions
from agent import question_agent, resume_agent, study_agent
import json
import time

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_RETRIES = 3
TIMEOUT_SECONDS = 20


def safe_json_parse(text: str, default: dict):
    """Strip markdown fences, parse JSON, return default if fails"""
    text = text.strip().replace("```json", "").replace("```", "")
    try:
        return json.loads(text)
    except Exception:
        return default


def call_agent_with_retry(agent, prompt: str, default: dict):
    """Retry AI call safely"""
    last_output = ""
    for attempt in range(MAX_RETRIES):
        try:
            result = agent.run_sync(prompt)
            last_output = result.output_text
            parsed = safe_json_parse(last_output, default)
            if parsed is not None:
                return parsed
        except Exception:
            pass
        time.sleep(1)
    raise HTTPException(
        status_code=500,
        detail=f"AI failed after {MAX_RETRIES} attempts. Last output: {last_output}"
    )


@app.get("/")
def root():
    return {"status": "OK"}


@app.post("/generate-questions", response_model=InterviewQuestions)
def generate_questions(req: TopicRequest):
    default = {"technical": [], "behavioral": [], "system_design": []}
    prompt = f"Return ONLY JSON with keys: technical, behavioral, system_design. Topic: {req.topic}"
    data = call_agent_with_retry(question_agent, prompt, default)
    try:
        return InterviewQuestions(**data)
    except ValidationError:
        return default


@app.post("/analyze-resume")
def analyze_resume(req: ResumeRequest):
    default = {"score": 0, "strengths": [], "weaknesses": [], "suggestions": []}
    prompt = f"Analyze this resume. Return ONLY JSON: {req.resume_text}"
    data = call_agent_with_retry(resume_agent, prompt, default)
    # Return validated structure
    return {"feedback": data}


@app.post("/study-plan")
def study_plan(req: StudyRequest):
    default = {"daily_plan": [], "tips": []}
    prompt = f"Create a study plan. Return ONLY JSON: {req.goal}"
    data = call_agent_with_retry(study_agent, prompt, default)
    return {"notes": data}
