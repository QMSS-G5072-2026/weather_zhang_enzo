# read version from installed package
from importlib.metadata import version

from .weather_ez2465 import celsius_to_fahrenheit, clean_readings, summarize_temperatures

__version__ = version("weather_ez2465")

__all__ = ["celsius_to_fahrenheit", "clean_readings", "summarize_temperatures"]
