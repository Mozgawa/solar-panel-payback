"""Test payback."""

from pysolar import calculate


def test_calculate(sample_dataframe):
    consumption = 1
    cost = 1
    wp = 50000

    expected_result = 33.0

    result = calculate(sample_dataframe, consumption, cost, wp)
    assert round(result) == expected_result


def test_calculate_zero_savings(sample_dataframe):
    consumption = 2000
    cost = 10000
    wp = 5000

    sample_dataframe["savings"] = 0

    result = calculate(sample_dataframe, consumption, cost, wp)
    assert result == float("inf")
