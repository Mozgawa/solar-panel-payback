"""Solar panel payback API."""

from os import getenv
from typing import Dict

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from pysolar import calculate, load_data
from pysolar.log import get_logger
from pysolar.models import SolarPanelPaybackRequest

app = FastAPI(title="PYSOLAR server")

logger = get_logger(__name__)


def authenticate(credentials: HTTPBasicCredentials = Depends(HTTPBasic())) -> bool:
    """Check the authentication credentials."""
    username = getenv("PYSOLAR_USER")
    password = getenv("PYSOLAR_PASS")
    if credentials.username == username and credentials.password == password:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials"
    )


@app.on_event("startup")
async def startup_event() -> None:
    """Startup event."""
    try:
        app.df = load_data()  # type: ignore
    except Exception as err:
        logger.error(f"{err}")
        raise HTTPException(
            status_code=500, detail="Failed to load data. Please try again later."
        )


@app.post("/api/{version}/payback", response_class=JSONResponse)
def payback(
    request: SolarPanelPaybackRequest,
    version: str,  # pylint: disable=unused-argument
    _: bool = Depends(authenticate),
) -> Dict[str, float]:
    """Compute payback."""
    try:
        result = {
            "paybackYears": calculate(
                app.df, request.consumption, request.cost, request.wp  # type: ignore
            )
        }
    except Exception as err:
        logger.error(f"{err}")
        raise HTTPException(status_code=500, detail="Failed to calculate. Please try again later.")
    return result


@app.get("/api/{version}/shortest-payback", response_class=JSONResponse)
def shortest_payback(
    version: str,  # pylint: disable=unused-argument
    consumption: float,
    start: int = 0,
    stop: int = 100000,
    step: int = 1000,
    _: bool = Depends(authenticate),
) -> Dict[str, int]:
    """Compute shortest payback."""
    if stop > 10000000:
        raise HTTPException(
            status_code=400, detail="Value is too big. Maximum allowed value is 10000000."
        )
    try:
        result = {
            "solarPanelsWp": min(
                ((calculate(app.df, consumption, 1000 + wp, wp), wp) for wp in range(start, stop, step)),  # type: ignore
                key=lambda x: x[0],
            )[1]
        }
    except Exception as err:
        logger.error(f"{err}")
        raise HTTPException(
            status_code=500, detail="Failed to calculate. Please try again later."
        )
    return result
