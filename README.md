<div align='center'>
<img src='https://github.com/1npo/nwsc/blob/main/resources/img/nwsc-logo.png' alt='nwsc logo by http://logomvp.com/, https://x.com/lentesdev; using https://phosphoricons.com/'>

---

**U.S. National Weather Service Client**

A full-coverage National Weather Service API client for the terminal. Made for weather nerds.

---

*Under active development as of July 2024*

</div>

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Demos](#demos)
- [Installation](#installation)
  - [Dependencies](#dependencies)
  - [PyPI](#pypi)
  - [GitHub](#github)
- [Usage](#usage)
  - [Console TUI](#console-tui)
  - [CLI Options](#cli-options)
  - [Data Export](#data-export)
- [Endpoint Coverage](#endpoint-coverage)
- [License](#license)
- [Credits](#credits)
- [TODO](#todo)
  - [Data](#data)
  - [Interface](#interface)
  - [Package](#package)
  - [Documentation](#documentation)
  - [Testing](#testing)
  - [Miscellaneous](#miscellaneous)

## Features
- Retrieve data from every* available NWS API endpoint [(see Endpoint Coverage section)](#endpoint-coverage)
- Uses [requests-cache](https://requests-cache.readthedocs.io/en/stable/) for faster data retrieval
- Pretty TUI with [Textual](https://textual.textualize.io) for exploring the data
- Output weather strings that can be piped to other tools (such as [i3status](https://i3wm.org/i3status/))
- Export data to various repositories for analytics or reporting:
  - CSV
  - SQLite
  - Postgres
  - Delta/Spark
  - JSON
## Demos
- [ ] Add GIFs and PNGs here
## Installation
### Dependencies
- [`requests-cache`](https://github.com/requests-cache/requests-cache)
- [`loguru`](https://github.com/Delgan/loguru)
- [`rich`](https://github.com/Textualize/rich)
- [`textual`](https://github.com/Textualize/textual)
### PyPI
- [ ] Add PyPI installation instructions here
### GitHub
- [ ] Add instructions for installing from GitHub
  - See: https://stackoverflow.com/questions/15268953/how-to-install-python-package-from-github
## Usage
### Console TUI
- [ ] List keybindings
### CLI Options
- [ ] Show how to print weather strings for piping
### Data Export
- [ ] Describe how to set up repositories for data export
- [ ] Describe how to enable/use data export features
## Endpoint Coverage
- [ ] /alerts
- [x] /alerts/active
- [x] /alerts/active/count
- [x] /alerts/active/zone/{zoneId}
- [x] /alerts/active/area/{area}
- [x] /alerts/active/region/{region}
- [x] /alerts/types
- [x] /alerts/{id}
- [ ] /aviation/cwsus/{cwsuId}
- [ ] /aviation/cwsus/{cwsuId}/cwas
- [ ] /aviation/cwsus/{cwsuId}/cwas/{date}/{sequence}
- [ ] /aviation/sigmets
- [ ] /aviation/sigmets/{atsu}
- [ ] /aviation/sigmets/{atsu}/{date}
- [ ] /aviation/sigmets/{atsu}/{date}/{time}
- [x] /glossary
- [x] /gridpoints/{wfo}/{x},{y}
- [x] /gridpoints/{wfo}/{x},{y}/forecast
- [x] /gridpoints/{wfo}/{x},{y}/forecast/hourly
- [ ] /gridpoints/{wfo}/{x},{y}/stations
- [ ] ~~/icons/{set}/{timeOfDay}/{first}~~ (**DEPRECATED**)
- [ ] ~~/icons/{set}/{timeOfDay}/{first}/{second}~~ (**DEPRECATED**)
- [ ] ~~/icons~~ (**DEPRECATED**)
- [x] /thumbnails/satellite/{area}
- [ ] /stations/{stationId}/observations
- [x] /stations/{stationId}/observations/latest
- [ ] /stations/{stationId}/observations/{time}
- [ ] /stations/{stationId}/tafs
- [ ] /stations/{stationId}/tafs/{date}/{time}
- [x] /stations
- [x] /stations/{stationId}
- [ ] /offices/{officeId}
- [ ] /offices/{officeId}/headlines/{headlineId}
- [ ] /offices/{officeId}/headlines
- [x] /points/{point}
- [x] /points/{point}/stations
- [x] /radar/servers
- [ ] /radar/servers/{id}
- [x] /radar/stations
- [ ] /radar/stations/{stationId}
- [x] /radar/stations/{stationId}/alarms
- [ ] ~~/radar/queues/{host}~~ (**UNEXPECTED 404**)
- [ ] ~~/radar/profilers/{stationId}~~ (**UNEXPECTED 404**)
- [x] /products
- [x] /products/locations
- [x] /products/types
- [x] /products/{productId}
- [x] /products/types/{typeId}
- [x] /products/types/{typeId}/locations
- [x] /products/locations/{locationId}/types
- [x] /products/types/{typeId}/locations/{locationId}
- [ ] /zones
- [ ] /zones/{type}
- [ ] /zones/{type}/{zoneId}
- [x] /zones/{type}/{zoneId}/forecast
- [x] /zones/forecast/{zoneId}/observations
- [x] /zones/forecast/{zoneId}/stations

## License
The National Weather Service Client (**nwsc**) is made available under the [MIT License](https://opensource.org/license/mit)

## Credits
- Logo by [LogoMVP](https://logomvp.com), which was created by [Eduardo Higareda](https://x.com/lentesdev)
- Icon in logo is from [Phosphor Icons](https://phosphoricons.com/)
- [Bruno](https://www.usebruno.com) was immensely helpful for exploring the NWS API

## TODO
### Data
- [ ] Finish writing API request functions for all endpoints
- [ ] Finish fleshing out dataclasses for all NWS data
- [ ] Update `api.py` to use dataclasess instead of dicts
- [x] Add wind speed/direction string and measurement conversions to `api.py` without using dataframes
- [x] Create a `repository` subpackage for recording historical weather responses
- [ ] Create repositories:
  - [ ] in-memory
  - [ ] sqlite
  - [ ] postgresql
  - [ ] delta
- [x] Revamp or remove `cache.py`: use `requests-cache` instead of rolling your own cache manager
- [ ] Update `api_temp.get_station_observations_data()` to follow the pattern that other `get_*_data()` functions use
### Interface
- [ ] Create an interactive TUI with Textual
- [ ] Update `main.py` to start the TUI by default
- [ ] Update `main.py` argument parser to let the user specify output types:
  - [ ] json
  - [ ] plain-text
  - [ ] emoji-text
  - [ ] rich-table
- [ ] Clean up and improve the quality of `render.py` and rename it to `render_rich.py`
- [x] Create a `render` subpackage and move `render_rich.py` into it
- [ ] Create additional renderers:
  - [ ] json
  - [ ] text
  - [ ] matplotlib
### Package
- [x] Rename `nws` to `nwsc`
- [ ] Remove `pandas` as a dependency
- [ ] Remove `loguru` as a dependency
- [ ] Remove `pytz` as a dependency
- [ ] Finalize dependencies and add them to `pyproject.toml`
- [x] Create resources folder for storing Rich demos and images
- [ ] Review `config.py` to determine if it can be improved
- [ ] Make any needed improvements to `config.py`
- [x] Split `api_temp.py` into separate modules, one for each endpoint
### Documentation
- [ ] Find some examples of great project READMEs
- [ ] Find some examples of great API documentation
- [ ] Fully populate *all* docstrings
  - [ ] Move all "See:" reference links from comments above functions to the module-level docstring
- [ ] Generate API documentation with Sphinx
- [ ] Fully flesh out nwsc READMEs
- [ ] Create "API Coverage" checklist in README and identify all API features that are implemented
### Testing
- [ ] Create unit tests for every function
  - [ ] `api.get_alerts`
  - [ ] `api.get_offices`
  - [ ] `api.get_products`
  - [ ] `api.get_radar`
  - [ ] `api.get_weather`
  - [ ] `config`
  - [ ] `decorators`
  - [ ] `main`
  - [ ] `repository.base`
  - [ ] `repository.in_memory`
  - [ ] `repository.sqlite`
  - [ ] `repository.postgres`
  - [ ] `repository.delta`
### Miscellaneous
- [x] The /radar/queues/{host} is unexpectedly returning 404 - email the NWS NOC
  - [x] If no response from NOC, submit issue to the github repo (https://github.com/weather-gov/api/discussions/756)
