import json
import os

from .routers.rates import rates_router
from fastapi import FastAPI

json_codes_file = open(
    os.path.join(os.path.dirname(__file__), "sea-ports-codes.json"), "r"
)
sea_port_codes = json.load(json_codes_file)

app = FastAPI()

app.include_router(rates_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
