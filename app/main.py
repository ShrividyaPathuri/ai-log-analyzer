from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from .parser import parse_lines
from .analyzer import level_counts, cluster_errors
from .schemas import AnalyzeReport
from .llm import summarize_with_llm

load_dotenv()
app = FastAPI(title="AI Log Analyzer", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalyzeReport)
async def analyze(
    use_llm: bool = Query(False),
    top_k: int = Query(8, ge=1, le=20),
    file: UploadFile = File(...),
):
    raw = (await file.read()).decode("utf-8", errors="replace")
    entries, stats = parse_lines(raw)
    levels = level_counts(entries)
    clusters = cluster_errors(entries, top_k=top_k)

    report = AnalyzeReport(
        total_lines=len(raw.splitlines()),
        parsed_lines=stats["parsed"],
        unparsed_lines=stats["unparsed"],
        levels=levels,
        top_clusters=clusters,
        llm_summary=None,
    )
    if use_llm:
        report.llm_summary = await summarize_with_llm(clusters, levels, report.total_lines)

    return JSONResponse(content=report.model_dump())
