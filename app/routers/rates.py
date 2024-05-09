from aiohttp import ClientSession
from fastapi import APIRouter


rates_router = APIRouter(
    prefix="/rates",
    tags=["rates"],
)


async def fetch_rates(
    session: ClientSession, source_location: str, destination_location: str
):
    hls_data = {}
    async with session.post(
        url="/DtsService/BookingApi/SearchAgentFCLPricing",
        data={
            "Filter": {
                "type": "FCL",
                "origin": "CNSHA",
                "origin_name": "SHANGHAI, CHINA",
                "destination": "USLAX",
                "destination_name": "LOS ANGELES, CA",
                "warehouse": "",
                "warehouse_name": "",
                "earliestEtd": "2024-05-08",
                "UserID": "0110195211",
            }
        },
    ) as response:
        pass


@rates_router.get("/")
async def get_rates(source_location: str, destination_location: str):
    async with ClientSession(base_url="https://www.hlsratex.com") as session:
        rates = await fetch_rates(session, source_location, destination_location)
    return {"rates": "USD 1.00 = EUR 0.85"}
