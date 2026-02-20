import os
import httpx
from typing import Optional, List
from .schemas import ErrorCluster

async def summarize_with_llm(clusters: List[ErrorCluster], levels: dict, total_lines: int) -> Optional[str]:
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if not api_key:
        return "LLM is not configured. Set LLM_API_KEY to enable summaries."

    prompt = _build_prompt(clusters, levels, total_lines)

    if provider != "openai":
        return f"Unsupported LLM_PROVIDER='{provider}'. Supported: openai."

    url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions")
    headers = {"Authorization": f"Bearer {api_key}"}

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful SRE assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]

def _build_prompt(clusters: List[ErrorCluster], levels: dict, total_lines: int) -> str:
    top = "\n".join([f"- ({c.count}x) {c.signature}" for c in clusters]) or "- (none)"
    return f"""You are an incident assistant. Analyze these log signals and write:
1) A 3-5 bullet incident summary
2) Likely root cause hypotheses (ranked)
3) Recommended next steps (5 bullets)
4) Risk/impact note (1-2 lines)

Context:
- total_lines: {total_lines}
- level_counts: {levels}
- top_error_clusters:
{top}

Be concrete. Avoid inventing details. If unsure, say what's missing.
""".strip()
