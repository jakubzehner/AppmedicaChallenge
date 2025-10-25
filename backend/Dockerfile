FROM ghcr.io/astral-sh/uv:alpine
ADD . /app

WORKDIR /app
RUN uv sync --locked --compile-bytecode

CMD ["uv", "run", "src/main.py"]