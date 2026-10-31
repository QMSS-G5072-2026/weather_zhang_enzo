"""Weather station utilities: temperature conversion, summaries, and cleaning of readings."""

import math

import pandas as pd

ABSOLUTE_ZERO_C = -273.15
MIN_PLAUSIBLE_C = -90.0
MAX_PLAUSIBLE_C = 60.0


def celsius_to_fahrenheit(celsius: float) -> float:
    """
    Convert a temperature from degrees Celsius to degrees Fahrenheit.

    Args:
        celsius: Temperature in degrees Celsius.

    Returns:
        Temperature in degrees Fahrenheit.

    Raises:
        TypeError: If `celsius` is not an int or a float.
        ValueError: If `celsius` is below absolute zero (-273.15 C).

    Examples
    --------
    >>> import weather_ez2465
    >>> weather_ez2465.celsius_to_fahrenheit(100)
    212.0
    >>> weather_ez2465.celsius_to_fahrenheit(-40)
    -40.0
    """
    if isinstance(celsius, bool) or not isinstance(celsius, (int, float)):
        raise TypeError("celsius must be a number")
    if celsius < ABSOLUTE_ZERO_C:
        raise ValueError("temperature cannot be below absolute zero")
    return celsius * 9 / 5 + 32


def summarize_temperatures(temps: list[float]) -> dict[str, float]:
    """
    Summarize a list of temperature readings, ignoring missing values (NaN).

    Args:
        temps: Temperature readings. Missing readings are stored as float("nan").

    Returns:
        A dictionary with the keys "mean", "min", "max", and "n_missing".

    Raises:
        ValueError: If there are no valid (non-missing) readings.

    Examples
    --------
    >>> import weather_ez2465
    >>> weather_ez2465.summarize_temperatures([10.0, float("nan"), 20.0])
    {'mean': 15.0, 'min': 10.0, 'max': 20.0, 'n_missing': 1}
    """
    valid = [t for t in temps if not math.isnan(t)]
    if not valid:
        raise ValueError("no valid temperature readings")
    return {
        "mean": sum(valid) / len(valid),
        "min": min(valid),
        "max": max(valid),
        "n_missing": len(temps) - len(valid),
    }


def clean_readings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw station readings.

    Steps:
        1. Drop rows where `temp_c` is missing.
        2. Drop physically implausible readings (outside -90 C to 60 C, inclusive bounds are kept).
        3. Add a `temp_f` column with the temperature in Fahrenheit.
        4. Sort by `station`, then `date`, and reset the index.

    Args:
        df: DataFrame with the columns `station`, `date`, and `temp_c`.

    Returns:
        A new, cleaned DataFrame. The input DataFrame is not modified.

    Examples
    --------
    >>> import pandas as pd
    >>> import weather_ez2465
    >>> raw = pd.DataFrame({
    ...     "station": ["JFK", "CPK", "JFK"],
    ...     "date": ["2026-07-02", "2026-07-01", "2026-07-01"],
    ...     "temp_c": [30.0, 25.0, float("nan")],
    ... })
    >>> weather_ez2465.clean_readings(raw)
      station        date  temp_c  temp_f
    0     CPK  2026-07-01    25.0    77.0
    1     JFK  2026-07-02    30.0    86.0
    """
    cleaned = df.dropna(subset=["temp_c"])
    in_range = cleaned["temp_c"].between(MIN_PLAUSIBLE_C, MAX_PLAUSIBLE_C)
    cleaned = cleaned[in_range].copy()
    cleaned["temp_f"] = cleaned["temp_c"] * 9 / 5 + 32
    return cleaned.sort_values(["station", "date"]).reset_index(drop=True)
