"""Test server."""

import os
from unittest.mock import patch

import pandas as pd
from fastapi.testclient import TestClient

from pysolar.server import app

app.df = pd.DataFrame()
client = TestClient(app)


def test_startup_event():
    response = client.get("/")
    assert response.status_code == 404


@patch("pysolar.server.calculate")
def test_payback(mock_calculate):
    os.environ["PYSOLAR_USER"] = "admin"
    os.environ["PYSOLAR_PASS"] = "password"
    auth = ("admin", "password")
    response = client.post(
        "/api/v1/payback", json={"consumption": 2000, "cost": 10000, "wp": 5000}, auth=auth
    )
    assert response.status_code == 200
    assert response.json() == {"paybackYears": 1.0}


@patch("pysolar.server.calculate")
def test_shortest_payback(mock_calculate):
    mock_calculate.return_value.__lt__ = lambda self, other: True
    os.environ["PYSOLAR_USER"] = "admin"
    os.environ["PYSOLAR_PASS"] = "password"
    auth = ("admin", "password")
    response = client.get("/api/v1/shortest-payback?consumption=2000", auth=auth)
    assert response.status_code == 200
    assert response.json() == {"solarPanelsWp": 9900.0}
