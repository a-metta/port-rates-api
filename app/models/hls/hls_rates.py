from enum import Enum
from typing import Optional
from pydantic import BaseModel


class HLSRateType(Enum):
    FCL = "FCL"
    LCL = "LCL"
    AIR = "AIR"


class HLSFilter(BaseModel):
    type: HLSRateType
    origin: str
    origin_name: Optional[str]
    destination: str
    destination_name: Optional[str]
    earliest_etd: str


class HLSRate(BaseModel):
    Filter: HLSFilter


class HLSRatesRequest(BaseModel):
    pass
