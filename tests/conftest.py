"""Conftest."""

import pandas as pd
import pytest


@pytest.fixture
def mock_getenv(monkeypatch):
    def mock_getenv_func(env_var):
        if env_var == "BELPEX_PATH":
            return "path_to_belpex.xlsx"
        elif env_var == "RLP_PATH":
            return "path_to_rlp.xlsx"
        elif env_var == "PROVIDER":
            return "provider_name"
        elif env_var == "SPP_PATH":
            return "path_to_spp.xlsx"
        elif env_var == "SPP_SHEET_NAME":
            return "spp_sheet_name"
        else:
            return None

    monkeypatch.setattr("os.getenv", mock_getenv_func)


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame(
        {
            "rlp": [0.5, 0.8, 1.0],
            "spp": [0.6, 0.9, 1.2],
            "Euro": [0.2, 0.3, 0.4],
        }
    )
