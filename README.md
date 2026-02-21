# AI Log Analyzer (FastAPI + LLM)

## 🚀 Overview

AI Log Analyzer is a backend service that parses application logs, clusters error patterns, and generates structured incident summaries.  
It is designed to simulate real-world SRE / backend debugging workflows.

The system:
- Parses structured and unstructured logs
- Detects error clusters
- Aggregates log severity levels
- Optionally generates LLM-based incident summaries
- Provides REST API via FastAPI
- Includes Docker support and CI testing

---

## 🏗 Architecture

Client → FastAPI API → Parser → Analyzer → (Optional) LLM → JSON Response

- **Parser**: Regex-based log parsing with fallback support
- **Analyzer**: Error clustering + signature normalization
- **LLM module**: Generates incident summaries (optional)
- **Tests**: Pytest-based validation
- **CI**: GitHub Actions

---

## 🧠 Engineering Decisions

- Used regex-based parsing to handle heterogeneous log formats
- Normalized dynamic values (IDs, timestamps) to improve clustering
- Designed modular separation: parser / analyzer / llm
- Added CI pipeline to validate test coverage on every push
- Dockerized for reproducible deployment

---

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

## 🔮 Future Improvements

- Add vector database for semantic log clustering
- Add real-time streaming log ingestion
- Add UI dashboard for visualizing incidents
- Deploy to cloud (Render / AWS / Railway)

