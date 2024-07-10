from dotenv import load_dotenv

load_dotenv()

import logging
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.api.routers.chat import chat_router
from app.settings import init_settings
from app.observability import init_observability
from fastapi.staticfiles import StaticFiles


app = FastAPI()

init_settings()
init_observability()

environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set
code_space = os.getenv("CODESPACE_NAME") #get the name of the codespace if set
github_api = os.getenv("NEXT_PUBLIC_CHAT_API") #get the codespaces api format 

if environment == "dev":
    logger = logging.getLogger("uvicorn")

    if code_space and github_api:
        logger.warning("Running in development mode and code spaces - allowing CORS for github codespaces origins")
        origin_8000 = github_api.replace("/api/chat","")
        origin_8000 = origin_8000.replace("${CODESPACE_NAME}", f"{code_space}")
        origin_3000 = origin_8000.replace("8000", "3000")
        origins = [origin_8000, origin_3000]
    else:
        logger.warning("Running in development mode - allowing CORS for all origins")
        origins = ["*"]
                   
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Redirect to documentation page when accessing base URL
    @app.get("/")
    async def redirect_to_docs():
        return RedirectResponse(url="/docs")


def mount_static_files(directory, path):
    if os.path.exists(directory):
        app.mount(path, StaticFiles(directory=directory), name=f"{directory}-static")


# Mount the data files to serve the file viewer
mount_static_files("data", "/api/files/data")
# Mount the output files from tools
mount_static_files("tool-output", "/api/files/tool-output")

app.include_router(chat_router, prefix="/api/chat")


if __name__ == "__main__":
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", "8000"))
    reload = True if environment == "dev" else False

    uvicorn.run(app="main:app", host=app_host, port=app_port, reload=reload)
