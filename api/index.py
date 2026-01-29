"""Vercel Serverless Function entrypoint.

This exposes the FastAPI `app` for the Python runtime (ASGI).
Routes are rewritten in `vercel.json` so `/verify`, `/certificate`, etc map here.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
	sys.path.insert(0, str(REPO_ROOT))


from app.main import app as fastapi_app

app = fastapi_app
