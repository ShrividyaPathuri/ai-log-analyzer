from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class LogEntry(BaseModel):
    line_no: int
    timestamp: Optional[str] = None
    level: Optional[str] = None
    service: Optional[str] = None
    message: str
    raw: str

class ErrorCluster(BaseModel):
    signature: str
    count: int
    sample_lines: List[int] = Field(default_factory=list)
    sample_messages: List[str] = Field(default_factory=list)

class AnalyzeReport(BaseModel):
    total_lines: int
    parsed_lines: int
    unparsed_lines: int
    levels: Dict[str, int]
    top_clusters: List[ErrorCluster]
    llm_summary: Optional[str] = None
