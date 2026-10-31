# weather_ez2465

![ci](https://github.com/QMSS-G5072-2026/weather_zhang_enzo/actions/workflows/ci.yml/badge.svg)

Weather station utilities: temperature conversion, summaries and cleaning of station readings.

## Installation

```bash
$ uv add weather_ez2465
```

or, without uv, `pip install weather_ez2465`.

## Development

```bash
$ uv sync                       # create .venv and install the package with its dev and docs groups
$ uv run pytest                 # run the tests
$ uv run make html -C docs      # build the documentation
$ uv build                      # build the sdist and wheel into dist/
```

## Usage

```python
import pandas as pd
import weather_ez2465

weather_ez2465.celsius_to_fahrenheit(100)                          # 212.0
weather_ez2465.summarize_temperatures([10.0, float("nan"), 20.0])  # mean, min, max, n_missing

raw = pd.DataFrame({
    "station": ["JFK", "CPK", "JFK"],
    "date": ["2026-07-02", "2026-07-01", "2026-07-01"],
    "temp_c": [30.0, 25.0, float("nan")],
})
weather_ez2465.clean_readings(raw)   # drops missing and implausible readings, adds temp_f, sorts
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`weather_ez2465` was created by Enzo Zhang. It is licensed under the terms of the MIT license.

## Credits

`weather_ez2465` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `qmss-pkgs-cookiecutter` [template](https://github.com/QMSS-G5072-2026/qmss-pkgs-cookiecutter), a uv-based fork of [`py-pkgs-cookiecutter`](https://github.com/py-pkgs/py-pkgs-cookiecutter).
