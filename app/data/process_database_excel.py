import pandas as pd
import json
import os

json_codes_file = open(
    os.path.join(os.path.dirname(__file__), "sea-ports-codes.json"), "r"
)
sea_port_codes = json.load(json_codes_file)


sea_ports_df = pd.DataFrame.from_records(sea_port_codes)

rates_database_df = pd.read_excel(
    os.path.join(os.path.dirname(__file__), "Database.xlsx"),
    sheet_name="EMEA FCL Import Rates",
)

origins = rates_database_df["Origin"].unique().tolist()
destinations = rates_database_df["Destination"].unique().tolist()

origin_matches = []
for index, row in rates_database_df.iterrows():
    country = row["Countries"]
    origin = row["Origin"]
    destination = row["Destination"]
    if (
        not isinstance(country, str)
        or not isinstance(origin, str)
        or not isinstance(destination, str)
    ):
        continue

    origin_port_name_result = sea_ports_df[
        sea_ports_df["port name"].str.contains(origin)
        & ~sea_ports_df["port name"].str.contains("=")
    ]
    destination_port_name_result = sea_ports_df[
        sea_ports_df["port name"].str.contains(destination)
    ]
    if not origin_port_name_result.empty:
        rates_database_df.at[index, "Origin Code"] = origin_port_name_result.iloc[0][
            "port code"
        ]
    if not destination_port_name_result.empty:
        rates_database_df.at[index, "Destination Code"] = (
            destination_port_name_result.iloc[0]["port code"]
        )

rates_database_df.to_excel(
    os.path.join(os.path.dirname(__file__), "Database_enhanced.xlsx"),
    sheet_name="EMEA FCL Import Rates",
    index=False,
)

# print(origin_matches)


merged_df = pd.concat([rates_database_df, sea_ports_df], ignore_index=True, sort=False)

print(merged_df)
