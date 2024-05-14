from enum import Enum
from re import S
from typing import Optional
from pydantic import BaseModel


pr_codes_mapping = {
    "COSU": "COSCO",
    "CMDU": "CMA",
    "ONEY": "ONE",
    "HLCU": "HPL",
    "MEDU": "MSC",
    "MAEU": "MSK",
}


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
    Charges: list[any]
    CommodityDetail: str
    EffectiveDate: str
    ExpiryDate: str
    GP20: int
    GP40: int
    HQ40: int
    HQ45: int
    ID: str
    NOR40: int
    PldAMSCode: str
    PldName: str
    PlrAMSCode: str
    PlrName: str
    PodAMSCode: str
    PodName: str
    PodPldTT: int
    PolAMSCode: str
    PolName: str
    PolPodTT: int
    PolViaTT: int
    PrCode: str
    PricingType: str
    Remark: str
    SOC20: int
    SOC40: int
    SOC40HQ: int
    SOC45: int
    SOCNOR40: int
    ServiceCode: str
    TruckFee20: int
    TruckFee40: int
    ViaAMSCode: str
    ViaName: str
    isSOC20: bool
    isSOC40: bool
    isSOC40HQ: bool
    isSOC45: bool
    isSOCNOR40: bool


class HLSRatesRequest(BaseModel):
    Filter: HLSFilter
