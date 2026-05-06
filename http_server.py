import os
import json
import asyncio
import sys
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

PORT = int(os.environ.get("PORT", 8080))
CREDS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
CREDS_FILE = "/tmp/gcp_creds.json"
if CREDS and CREDS.strip().startswith("{"):
      with open(CREDS_FILE, "w") as f:
                f.write(CREDS)
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDS_FILE


async def handle_mcp(request):
      body = await request.body()
    proc = await asyncio.create_subprocess_exec(
              sys.executable, "-m", "analytics_mcp",
              stdin=asyncio.subprocess.PIPE,
              stdout=asyncio.subprocess.PIPE,
              stderr=asyncio.subprocess.PIPE,
              env=os.environ.copy()
    )
    stdout, stderr = await proc.communicate(input=body)
    if proc.returncode != 0:
              return JSONResponse({"error": stderr.decode()}, status_code=500)
          return JSONResponse(json.loads(stdout.decode()))


async def health(request):
      return JSONResponse({"status": "ok"})


app = Starlette(routes=[
      Route("/mcp", handle_mcp, methods=["POST"]),
      Route("/health", health),
])

if __name__ == "__main__":
      uvicorn.run(app, host="0.0.0.0", port=PORT)
