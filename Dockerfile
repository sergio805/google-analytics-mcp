FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir analytics-mcp uvicorn starlette anyio httpx

COPY http_server.py .

ENV PORT=8080
EXPOSE 8080

CMD ["python", "http_server.py"]
