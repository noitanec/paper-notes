import time

from fastapi import FastAPI
from loguru import logger
import uvicorn

app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info(f"Total Process time: {process_time}")
    response.headers["my-time"] = str(process_time)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0:8000", reload=True)
