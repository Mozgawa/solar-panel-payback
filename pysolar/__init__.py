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
    df["cost"] = consumption * df["rlp"] * df["Euro"] / 1000
    df["pv_yield"] = wp * df["spp"] / 1000
    df["diff"] = df["pv_yield"] - (consumption * df["rlp"])
    df["profit"] = np.where(
        df["diff"] >= 0, 0.8 * df["cost"] * df["diff"], (1.2 * df["cost"] + 0.12) * df["diff"]
    )
    df["savings"] = (consumption * df["rlp"] * df["cost"]) + df["profit"]
    df = df.dropna()
    df = df.replace(0, pd.NA).dropna()
    savings = df["savings"].sum()
    return cost / savings if savings > 0 else float("inf")  # type: ignore
