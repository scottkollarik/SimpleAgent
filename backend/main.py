# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import json
from orchestrator import run_prompt
from llm_wrapper import call_llm

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask")
async def ask(request: PromptRequest):
    try:
        result = run_prompt(request.prompt, call_llm)
        return {
            **result,
            "agent_reasoning": json.dumps(result["steps"], indent=2),
            "system_prompt": "Modular agent execution plan",
        }
    except Exception as e:
        return {
            "response": f"Internal error: {str(e)}",
            "steps": [],
            "tool_used": "none",
            "system_prompt": "Execution failed",
            "agent_reasoning": "[]",
            "timestamp": datetime.utcnow().isoformat()
        }