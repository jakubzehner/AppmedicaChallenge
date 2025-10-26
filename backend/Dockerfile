FROM ghcr.io/astral-sh/uv:python3.12-alpine
RUN apk add --update curl
ADD . /app

WORKDIR /app
RUN uv sync --locked --compile-bytecode

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=5 \
    CMD [ "curl", "--fail", "http://localhost:8000/api/health" ]

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "appmedica:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "/app/appmedica/logging.json", "--log-level", "info"]