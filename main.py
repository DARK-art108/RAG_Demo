import os
import sys
from pathlib import Path

import uvicorn

_ROOT = Path(__file__).resolve().parent
_SRC = str(_ROOT / "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)
_prev_pp = os.environ.get("PYTHONPATH", "")
os.environ["PYTHONPATH"] = (
    _SRC if not _prev_pp else os.pathsep.join([_SRC, _prev_pp])
)

if __name__ == "__main__":
    # Open http://127.0.0.1:<PORT>/docs (not https://). Override with PORT=9000 uv run python main.py
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("rag_demo.api:app", host="0.0.0.0", port=port, reload=True)
