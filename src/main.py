# python
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse

from src.articles.router import router as article_router
from src.auth.router import router as auth_router
from src.core.config import settings
from src.core.exceptions import setup_exception_handlers
from src.order.router import router as booking_router
from src.restaurant.router import router as restaurant_router
from src.user.router import router as user_router
from src.user.router_admin import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
	print("✅ Logging configured at DEBUG level")
	mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
	db = mongo_client["pm_project"]
	app.state.mongo_client = mongo_client
	app.state.mongo_db = db
	print("✅ MongoDB client initialized")
	yield
	mongo_client.close()
	print("👋 App shutting down and MongoDB client closed")


app = FastAPI(
	title="FastAPI Best Practices Project",
	description="A FastAPI project following best practices",
	version="1.0.0",
	lifespan=lifespan
)

# Add CORS middleware
# Allow only domain names in settings.ALLOWED_HOSTS to access the API
app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.ALLOWED_HOSTS,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Allow only IP addresses in settings.ALLOWED_HOSTS to access the API
# @app.middleware("http")
# async def restrict_ip(request: Request, call_next):
# 	x_forwarded_for = request.headers.get("x-forwarded-for")
#
# 	if x_forwarded_for:
# 		client_ip = x_forwarded_for.split(",")[0].strip()
# 	else:
# 		client_ip = request.client.host
#
# 	if client_ip not in settings.ALLOWED_HOSTS:
# 		logging.warning(f"Forbidden: {client_ip} access")
#
# 		return JSONResponse(
# 			status_code=403,
# 			content={"detail": f"Forbidden: {client_ip} not allowed"}
# 		)
# 	return await call_next(request)

setup_exception_handlers(app)

app.include_router(router=user_router, prefix="/user")
app.include_router(router=auth_router, prefix="/auth")

app.include_router(router=restaurant_router, prefix="/restaurant")

app.include_router(router=article_router, prefix="/article")
app.include_router(router=booking_router, prefix="/booking")
app.include_router(router=admin_router, prefix="/admin")


@app.get("/")
def read_root():
	return {"message": "Hello guys!"}


@app.get("/{full_path:path}")
def catch_all(full_path: str):
	return HTMLResponse(content="", status_code=404)


if __name__ == "__main__":
	# Ensure the project root (parent of `Server`) is on sys.path so
	# the reloader subprocess can import "Server.main"
	project_root = Path(__file__).resolve().parents[1]
	if str(project_root) not in sys.path:
		sys.path.insert(0, str(project_root))

	# Lưu ý khi chạy trên máy thật thì host="
	# Chạy bằng main:app
	uvicorn.run("main:app", host="0.0.0.0", port=1412, reload=True, forwarded_allow_ips="*")
