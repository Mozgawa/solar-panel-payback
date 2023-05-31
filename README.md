# PYSOLAR

[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://python.org/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/ambv/black)

## What is pysolar?

`pysolar` is a tool used for calculating payback of solar panels.

# Prerequisites

Before installing the `pysolar`, ensure that the following software is installed on your system.

- Docker
- Git

# Quick start

Create `.env` file containing necessary envvars, which will be described later

Clone package

    git clone https://github.com/Mozgawa/solar-panel-payback

Build pysolar image

    docker-compose build

Start pysolar server

    docker-compose up -d

# Authorization

Requests have to contain Basic Auth authorization with login and password configured as `PYSOLAR_USER` and `PYSOLAR_PASS` envvars.

# How to use it?

There are two endpoints, one calculates the payback and the other counts Wp for the fastest possible payback.

`payback`:

    curl -X POST -u pysolaruser:HDE6upsiaCWRm0L -H "Content-Type: application/json" -d '{"consumption": 2000.0, "cost": 3000.0, "wp": 4000.0}' http://localhost:8000/api/v1/payback

returns:

    {
        "paybackYears": 53.127427682432526
    }

`shortest-payback`:

    curl -X GET -u pysolaruser:HDE6upsiaCWRm0L http://localhost:8000/api/v1/shortest-payback?consumption=2000&start=1000&stop=100000&step=1000

returns:

    {
        "solarPanelsWp": "7900.0"
    }

# Environment variables

Environment variables used by `pysolar` has to be defined in `.env` file:

| Varaible | Description | Example value |
| -------- | ----------- | ------------- |
| PROVIDER | OS user for pyrcs | 5414492999998 |
| BELPEX_PATH | OS user for pyrcs | data/BelpexFilter.xlsx |
| RLP_PATH | OS user for pyrcs | data/rlp0n2023-electricity-all-dsos.xlsb |
| SPP_PATH | OS user for pyrcs | data/spp-2023-ex-ante-and-ex-post_v2.0.xlsx |
| SPP_SHEET_NAME | OS user for pyrcs | Ex-ante 2023 (IP8) |
| PYSOLAR_USER | Username for basic FastAPI authentication | pysolaruser |
| PYSOLAR_PASS | Password for basic FastAPI authentication | HDE6upsiaCWRm0L |
