from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class CfgExtractor:
    dsn: str
    query: str
    chunksize: int = 50000
