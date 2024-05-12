import json
import os


json_codes_file = open(
    os.path.join(os.path.dirname(__file__), "sea-ports-codes.json"), "r"
)
sea_port_codes = json.load(json_codes_file)
