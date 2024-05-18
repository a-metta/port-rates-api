import asyncio
import datetime
from wsgiref import headers
import aiohttp
from .routers.rates import rates_router
from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI()

app.include_router(rates_router)

rates_database_df = pd.read_excel(
    os.path.join(os.path.dirname(__file__), "data/Database_enhanced.xlsx"),
    sheet_name="EMEA FCL Import Rates",
)

origin_destination_list = list(
    zip(rates_database_df["Origin Code"], rates_database_df["Destination Code"])
)


async def main():
    async with aiohttp.ClientSession(
        base_url="https://www.hlsratex.com",
        headers={"Content-Type": "application/json"},
    ) as session:
        for i in range(0, 1):
            origin, destination = origin_destination_list[i]
            async with session.post(
                url="/DtsService/BookingApi/SearchAgentFCLPricing",
                data={
                    "Filter": {
                        "type": "FCL",
                        "origin": origin,
                        "destination": destination,
                        "warehouse": "",
                        "warehouse_name": "",
                        "earliestEtd": datetime.date.today().strftime("%Y-%m-%d"),
                        "UserID": "0110195211",
                    }
                },
            ) as response:
                print(await response.json())


asyncio.run(main())


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)
