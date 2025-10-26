from fastapi.routing import APIRouter

health_router = APIRouter(prefix="/health", tags=["health"])


@health_router.get("", status_code=200)
def health():
    return {"status": "ok"}
