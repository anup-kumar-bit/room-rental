import logging

from fastapi import FastAPI

from app.routes import auth_route

# -----  Basic Config   -----
app = FastAPI()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("Room-rental")


# ------  Health Checker ------
@app.get("/health", tags=["Health"])
def health():
    logging.info("Server is Live")
    return {"report": "Health is ok "}

# ------ All Working Apis ------
app.include_router(auth_route.authRouter)

