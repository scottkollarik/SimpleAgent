import os
import importlib.util
import json
from typing import List, Dict, Callable

TOOLS_DIR = os.path.join(os.path.dirname(__file__), "tools")

def load_tools() -> List[Dict]:
    tools = []
    for tool_name in os.listdir(TOOLS_DIR):
        tool_path = os.path.join(TOOLS_DIR, tool_name)
        if not os.path.isdir(tool_path):
            continue

        logic_file = os.path.join(tool_path, "logic.py")
        json_file = os.path.join(tool_path, "tool.json")

        if os.path.exists(logic_file) and os.path.exists(json_file):
            with open(json_file, "r") as f:
                meta = json.load(f)

            spec = importlib.util.spec_from_file_location(f"tools.{tool_name}.logic", logic_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            meta["module"] = module
            meta.setdefault("strict", False)
            meta.setdefault("keywords", [])
            tools.append(meta)

    return tools

def score_tool(tool: Dict, chunk: str) -> float:
    keywords = tool.get("keywords", [])
    if not keywords:
        return 0.0  # Unlikely match if no keywords

    score = 0
    for kw in keywords:
        if kw.lower() in chunk.lower():
            score += 1
    return score / len(keywords)

def choose_tools(prompt: str, tools: List[Dict], llm_tool: Dict) -> List[Dict]:
    chunks = [chunk.strip() for chunk in prompt.split(".") if chunk.strip()]
    selected = []

    for chunk in chunks:
        best_tool = None
        best_score = 0

        for tool in tools:
            score = score_tool(tool, chunk)
            if score > best_score:
                best_tool = tool
                best_score = score

        # Apply fallback if strict and score too low
        if best_tool:
            if best_tool.get("strict", False) and best_score < 0.5:
                selected.append((llm_tool, chunk))
            else:
                selected.append((best_tool, chunk))
        else:
            selected.append((llm_tool, chunk))

    return selected

def run_prompt(prompt: str, llm_helper: Callable[[str], str] = None) -> Dict:
    tools = load_tools()

    # Runtime-defined LLM fallback tool with dynamic `run` method
    llm_tool = {
        "name": "LLM",
        "module": type("LLMFallback", (), {
            "run": lambda text, llm_helper=None: llm_helper(text) if llm_helper else text
        }),
        "strict": False,
        "keywords": []
    }

    steps = []
    full_response = []

    selections = choose_tools(prompt, tools, llm_tool)

    for tool, chunk in selections:
        try:
            result = tool["module"].run(chunk, llm_helper)
            steps.append({
                "step": chunk,
                "tool": tool["name"],
                "response": result
            })
            full_response.append(result)
        except Exception as e:
            steps.append({
                "step": chunk,
                "tool": tool["name"],
                "response": f"[Tool execution error: {str(e)}]"
            })

    return {
        "response": " ".join(full_response),
        "steps": steps,
        "tool_used": ", ".join(sorted(set(s["tool"] for s in steps))),
        "timestamp": __import__("datetime").datetime.utcnow().isoformat()
    }