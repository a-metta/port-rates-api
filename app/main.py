import asyncio
import datetime
from enum import unique
from glob import iglob
import json
from wsgiref import headers
import aiohttp
from app.models.hls.hls_rates import HLSRate, pr_codes_mapping
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

unique_origins = rates_database_df["Origin Code"].drop_duplicates().tolist()
unique_destinations = rates_database_df["Destination Code"].drop_duplicates().tolist()


port_codes = json.load(
    open(os.path.join(os.path.dirname(__file__), "data/sea-ports-codes.json"))
)

port_code_to_country = {
    port_code.get("port code"): port_code.get("country") for port_code in port_codes
}


async def main():
    updated_rates_df = pd.DataFrame(
        columns=[
            "Carriers",
            "Countries",
            "Origin",
            "Destination",
            "Country",
            "20GP",
            "40GP",
            "40HQ",
            "ETD",
            "Transit time",
            "via",
            "Validity",
            "Handling fee",
            "Remark",
        ]
    )
    async with aiohttp.ClientSession(
        base_url="https://www.hlsratex.com",
        headers={"Content-Type": "application/json"},
    ) as session:
        for unique_origin in unique_origins:
            for unique_destination in unique_destinations:
                if unique_destination == "nan":
                    continue
                async with session.post(
                    url="/DtsService/BookingApi/SearchAgentFCLPricing",
                    data=json.dumps(
                        {
                            "Filter": {
                                "type": "FCL",
                                "origin": unique_origin,
                                "destination": unique_destination,
                                "warehouse": "",
                                "warehouse_name": "",
                                "earliestEtd": datetime.date.today().strftime(
                                    "%Y-%m-%d"
                                ),
                                "UserID": "0110195211",
                            }
                        }
                    ),
                ) as response:
                    rates_raw = await response.json()
                    rates: list[HLSRate] = [HLSRate(**rate) for rate in rates_raw]
                    for rate in rates:
                        shipping_company = pr_codes_mapping.get(rate.PrCode, None)
                        if shipping_company is None:
                            continue
                        updated_rates_df = updated_rates_df._append(
                            {
                                "Carriers": shipping_company,
                                "Countries": port_code_to_country.get(
                                    rate.PolAMSCode, None
                                ),
                                "Origin": rate.PolName,
                                "Destination": rate.PldName,
                                "Country": port_code_to_country.get(
                                    rate.PldAMSCode, None
                                ),
                                "20GP": rate.GP20,
                                "40GP": rate.GP40,
                                "40HQ": rate.HQ40,
                                "ETD": rate.EffectiveDate,
                                "Transit time": rate.PolPodTT,
                                "via": rate.PolName,
                                "Validity": rate.ExpiryDate,
                                "Handling fee": 0,
                                "Remark": rate.Remark,
                            },
                            ignore_index=True,
                        )
    updated_rates_df.to_excel(
        os.path.join(os.path.dirname(__file__), "data/updated_rates.xlsx"),
        index=False,
    )


asyncio.run(main())


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)
