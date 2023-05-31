"""Solar payback calculation."""

from os import getenv
from typing import Optional

import numpy as np
import pandas as pd

from pysolar.log import get_logger

logger = get_logger(__name__)


def load_data() -> Optional[pd.DataFrame]:
    """Load and preprocess the DataFrame."""
    logger.info("Loading belpex data")
    belpex = pd.read_excel(getenv("BELPEX_PATH"), header=0)
    belpex = belpex.sort_values(by="Date").reset_index(drop=True)
    belpex.rename(columns={"Date": "cet"}, inplace=True)
    belpex["cet"] += pd.offsets.DateOffset(years=1)  # type: ignore

    logger.info("Loading rlp data")
    rlp = pd.read_excel(getenv("RLP_PATH"), skiprows=2, header=0)
    rlp.rename(columns={"Min": "Minute"}, inplace=True)
    rlp["cet"] = pd.to_datetime(rlp[["Year", "Month", "Day", "h", "Minute"]])
    rlp = pd.DataFrame({"cet": rlp["cet"], "rlp": rlp[getenv("PROVIDER")]})

    logger.info("Loading spp data")
    spp = pd.read_excel(getenv("SPP_PATH"), sheet_name=getenv("SPP_SHEET_NAME"), header=0)
    spp = pd.DataFrame({"cet": spp["UTC"], "spp": spp[getenv("PROVIDER")]})  # type: ignore
    spp = spp.iloc[4:]

    # Because belpex data is hourly it needs to be resampled
    rlp.set_index("cet", inplace=True)
    rlp = rlp["rlp"].resample("H").sum()  # type: ignore
    rlp = rlp.reset_index()

    spp.set_index("cet", inplace=True)
    spp = spp["spp"].resample("H").mean()  # type: ignore
    spp = spp.reset_index()

    logger.info("Merging tables belpex, spp and rlp")
    df = pd.merge(pd.merge(rlp, spp, on="cet"), belpex, on="cet")

    return df


def calculate(df: pd.DataFrame, consumption: float, cost: float, wp: float) -> float:
    """Calculate."""
    # consumption at the moment
    df["consumption"] = consumption * df["rlp"]

    # cost in euros in a given hour by multiplying the consumption at the moment by
    # the price of electricity, then dividing by 1000 as the price in the table is given in EUR/kWh
    df["cost"] = df["consumption"] * df["Euro"] / 1000

    # electricity produced
    df["pv_yield"] = wp * df["spp"] / 1000

    # difference between the electricity produced at a given moment and the current consumed
    df["diff"] = df["pv_yield"] - df["consumption"]

    # profit or possibly the loss resulting from the tariff
    df["profit"] = np.where(
        df["diff"] >= 0, 0.8 * df["cost"] * df["diff"], (1.2 * df["cost"] + 0.12) * df["diff"]
    )

    # savings calculated as consumption multiplied by rlp and cost plus profit or possibly loss
    df["savings"] = (df["consumption"] * df["cost"]) + df["profit"]

    # annual sum of savings resulting from the use of panels
    savings = df["savings"].sum()

    # if the annual savings is greater than 0, then dividing the total installation cost
    # by this amount, we will get the expected return expressed in years
    return cost / savings if savings > 0 else float("inf")  # type: ignore
