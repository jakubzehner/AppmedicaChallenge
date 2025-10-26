FROM ghcr.io/astral-sh/uv:python3.12-alpine
ADD . /app

WORKDIR /app
RUN uv sync --locked --compile-bytecode

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "appmedica:app", "--host", "0.0.0.0", "--port", "8000"]