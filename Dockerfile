FROM python:3.9-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir fastapi uvicorn pandas numpy empyrical

EXPOSE 8001

CMD ["python", "-m", "uvicorn", "mcp_server.empyrical_mcp_server:app", "--host", "0.0.0.0", "--port", "8001"]
