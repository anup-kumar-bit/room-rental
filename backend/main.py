import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.routes import auth_route, dropdown_route

# -----  Basic Config   -----
app = FastAPI()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("Room-rental")


# ------ Same response shape for HTTPException (e.g. 401/403 from auth) ------
@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "data": None},
        headers=exc.headers,
    )


# ------  Health Checker ------
@app.get("/health", tags=["Health"])
def health():
    logging.info("Server is Live")
    return {"report": "Health is ok "}

# ------ All Working Apis ------
app.include_router(auth_route.authRouter)
app.include_router(dropdown_route.dropdownRouter)

