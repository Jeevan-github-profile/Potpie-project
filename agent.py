from pydantic_ai import Agent
from pydantic_ai.providers.openrouter import OpenRouterProvider
from pydantic_ai.models.openrouter import OpenRouterModel

# ⚡ Replace with your real API key
provider = OpenRouterProvider(api_key="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")


model = OpenRouterModel("gpt-4o-mini", provider=provider)

question_agent = Agent(
    model=model,
    system_prompt=(
        "You are a FAANG interview coach.\n"
        "Return ONLY JSON with keys: technical, behavioral, system_design.\n"
        "Each must be an array of strings.\n"
        "No markdown. No explanation."
    )
)

resume_agent = Agent(
    model=model,
    system_prompt="You are an expert technical recruiter. Return only JSON."
)

study_agent = Agent(
    model=model,
    system_prompt="You are a career mentor. Return only JSON with daily_plan and tips."
)

def call_agent_with_retry(agent, prompt: str, default: dict):
    """Retry AI call safely; fallback to default if empty"""
    for attempt in range(MAX_RETRIES):
        try:
            result = agent.run_sync(prompt)
            output = (result.output_text or "").strip()
            if not output:
                # Empty output → use default immediately
                return default
            parsed = safe_json_parse(output, default)
            if parsed is not None:
                return parsed
        except Exception:
            pass
    return default  # Never fail with 500

