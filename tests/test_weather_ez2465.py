"""Tests for the weather_ez2465 package (adapted from the HW6 tests)."""

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

import weather_ez2465
from weather_ez2465 import (
    celsius_to_fahrenheit,
    clean_readings,
    summarize_temperatures,
)


def test_version_is_defined():
    """The package exposes its version as a string."""
    assert isinstance(weather_ez2465.__version__, str)


# =============================================================================
# UNIT TESTS
# =============================================================================


@pytest.mark.parametrize(
    "celsius, expected",
    [
        (0, 32.0),            # freezing point of water
        (100, 212.0),         # boiling point of water
        (-40, -40.0),         # the point where both scales meet
        (37, 98.6),           # body temperature (returns 98.60000000000001)
        (-273.15, -459.67),   # absolute zero itself is allowed
        (21.5, 70.7),         # a float input
    ],
)
def test_celsius_to_fahrenheit(celsius, expected):
    """Known reference points convert correctly; approx absorbs floating point rounding."""
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected)


@pytest.mark.parametrize(
    "bad_input, expected_error",
    [
        ("25", TypeError),        # a string, even if it looks like a number
        (None, TypeError),        # a missing value
        (True, TypeError),        # a bool is rejected although bool is a subclass of int
        ([10.0], TypeError),      # a list instead of a single number
        (-273.16, ValueError),    # just below absolute zero
        (-500, ValueError),       # far below absolute zero
    ],
)
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    """Inputs that are not numbers raise TypeError; values below absolute zero raise ValueError."""
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)


def test_summarize_temperatures():
    """Mean, min and max ignore the NaN reading, and the NaN is counted as missing."""
    # Arrange
    temps = [10.0, float("nan"), 20.0, 30.0]

    # Act
    result = summarize_temperatures(temps)

    # Assert
    assert set(result) == {"mean", "min", "max", "n_missing"}
    assert result["mean"] == pytest.approx(20.0)
    assert result["min"] == 10.0
    assert result["max"] == 30.0
    assert result["n_missing"] == 1


def test_summarize_temperatures_all_missing():
    """A list without any valid reading raises ValueError, as the docstring specifies."""
    with pytest.raises(ValueError, match="no valid temperature readings"):
        summarize_temperatures([float("nan"), float("nan")])


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def raw_readings():
    """Raw station readings with one missing value, one sensor error (999.0) and unsorted rows."""
    return pd.DataFrame({
        "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
        "date": ["2026-07-02", "2026-07-01", "2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
    })


def test_raw_readings_fixture(raw_readings):
    """The fixture has the expected columns, five rows and exactly one missing temperature."""
    assert list(raw_readings.columns) == ["station", "date", "temp_c"]
    assert len(raw_readings) == 5
    assert raw_readings["temp_c"].isna().sum() == 1
    assert raw_readings[["station", "date"]].isna().sum().sum() == 0


# =============================================================================
# TESTING DATAFRAMES
# =============================================================================


def test_clean_readings(raw_readings):
    """clean_readings drops the NaN and the 999.0 row, adds temp_f and sorts by station, then date."""
    # Arrange: worked out by hand.
    #   Dropped: JFK 2026-07-01 (temp_c is NaN) and CPK 2026-07-02 (999.0 is above 60 C).
    #   Kept and sorted by station: CPK, JFK, LGA.
    #   temp_f = temp_c * 9 / 5 + 32: 25 -> 77.0, 30 -> 86.0, 28 -> 82.4
    expected = pd.DataFrame({
        "station": ["CPK", "JFK", "LGA"],
        "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [25.0, 30.0, 28.0],
        "temp_f": [77.0, 86.0, 82.4],
    })

    # Act
    result = clean_readings(raw_readings)

    # Assert: same values, column order, dtypes and a fresh 0, 1, 2 index
    assert_frame_equal(result, expected)


def test_clean_readings_does_not_modify_input(raw_readings):
    """The docstring promises a new DataFrame, so the input must be left unchanged."""
    original = raw_readings.copy()
    clean_readings(raw_readings)
    assert_frame_equal(raw_readings, original)


def test_clean_readings_keeps_bounds_and_sorts_dates():
    """Readings exactly at -90 C and 60 C are kept, and rows of one station are sorted by date."""
    raw = pd.DataFrame({
        "station": ["JFK", "JFK", "JFK"],
        "date": ["2026-07-03", "2026-07-01", "2026-07-02"],
        "temp_c": [60.0, -90.0, 60.1],
    })
    result = clean_readings(raw)
    assert result["date"].tolist() == ["2026-07-01", "2026-07-03"]
    assert result["temp_c"].tolist() == [-90.0, 60.0]
