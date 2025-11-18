# python
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.user.router import router as user_router
from src.core.config import settings
from src.core.exceptions import setup_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
	print("✅ Logging configured at DEBUG level")
	# mongo_client = AsyncDatabase(os.environ["MONGODB_URL"])
	# app.state: State
	# app.state.mongo_client = mongo_client
	print("✅ MongoDB client initialized")
	yield  # app runs here
	# noinspection PyTypeChecker
	# mongo_client.close()  # ✅ works fine in Motor >= 3.0
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



@app.get("/")
def read_root():
	return {"message": "Hello guys!"}


if __name__ == "__main__":
	# Ensure the project root (parent of `Server`) is on sys.path so
	# the reloader subprocess can import "Server.main"
	project_root = Path(__file__).resolve().parents[1]
	if str(project_root) not in sys.path:
		sys.path.insert(0, str(project_root))

	# Lưu ý khi chạy trên máy thật thì host="
	# Chạy bằng main:app
	uvicorn.run("main:app", host="0.0.0.0", port=1412, reload=True)
