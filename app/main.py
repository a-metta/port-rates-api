import json
import os
from fuzzywuzzy import process, fuzz
from openpyxl import load_workbook
import pandas as pd
from .routers.rates import rates_router
from fastapi import FastAPI

from app.routers import rates


app = FastAPI()

app.include_router(rates_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
