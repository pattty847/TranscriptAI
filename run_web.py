#!/usr/bin/env python3
"""
Run Subtext web UI. Reachable on this machine and on your home network.

  uv run python run_web.py

Then open:
  - On this PC:  http://127.0.0.1:8765
  - From phone/tablet (same Wi‑Fi):  http://<THIS_PC_IP>:8765

Find this PC's IP: Windows: ipconfig  |  macOS/Linux: ip addr
"""
import sys
from pathlib import Path

# Run from project root so src.* imports work
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    import uvicorn
    # 0.0.0.0 = listen on all interfaces (localhost + LAN IP)
    uvicorn.run(
        "src.web.server:app",
        host="0.0.0.0",
        port=8765,
        reload=False,
    )
