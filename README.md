# AI Log Analyzer (FastAPI)

Upload logs → parse → cluster error patterns → optional LLM incident summary.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Swagger UI: http://localhost:8000/docs

## Analyze sample logs
```bash
curl -s -X POST "http://localhost:8000/analyze?use_llm=false" \
  -F "file=@sample_logs/app.log" | python -m json.tool
```

## Docker
```bash
docker build -t ai-log-analyzer .
docker run --rm -p 8000:8000 ai-log-analyzer
```

## Tests
```bash
pytest -q
```
