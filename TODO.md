# TODO
Roadmap and individual tasks that need to be completed to reach MVP status.

## Roadmap
> [!NOTE]
> The roadmap lists high-level milestones. The remaining sections list specific tasks that need to be done to reach these milestones.
- [x] Get all data from all endpoints
- [x] Create a model of all API data
- [ ] Create repositories for loading modeled API data into databases
- [ ] Create services to interface with repositories
- [ ] Create schemas for relational repositories
- [ ] Design and build a user interface
- [ ] Design and build a suite of unit tests
- [ ] Complete and finalize MVP documentation
  
## Data
### Retrieval & Processing
- [x] Finish writing API request functions for all endpoints
- [x] Add wind speed/direction string and measurement conversions to `nwsc.api.conversions` without using dataframes
- [x] Fix `get_zone_stations` - it's returning an empty list
  - [x] Re-generate `tests/test_data/nws_raw_zone_stations.json`
- [x] Revamp or remove `cache.py`: use `requests-cache` instead of rolling your own cache manager
- [x] Write `nwsc.api.get_enums` to extract `VALID_NWS_ZONES` and `VALID_NWS_FORECAST_OFFICES` enums programmatically from API error responses
- [x] Clean up and standardize all `nwsc.api.*` modules, to get them ready to use dataclasses
### Modeling
- [x] Finish fleshing out dataclasses for all NWS data
  - [x] alerts
  - [x] aviation
  - [x] glossary
  - [x] locations
  - [x] offices
  - [x] products
  - [x] radar
  - [x] stations
  - [x] weather
  - [x] zones
- [x] Update `nwsc.api.*` to use dataclasess instead of dicts
  - [x] alerts
  - [x] aviation
  - [x] locations
  - [x] offices
  - [x] products
  - [x] radar
  - [x] stations
  - [x] weather
  - [x] zones
- [ ] Do some research on NWS' radars and data processing systems (eg NEXRAD) to understand what all the API response fields mean
  - See: https://www.weather.gov/nl2/ServerView
- [ ] Revise `model.radar` to better model NWS radars and servers

## Repository & Service
- [x] Create a `repository` subpackage for recording historical weather responses
- [ ] Create repository modules:
  - [x] in-memory
  - [x] sqlite
  - [ ] json
  - [ ] csv
  - [ ] postgresql
  - [ ] delta
- [ ] Define table schema for:
  - [ ] locations
  - [ ] stations
  - [ ] observations
  - [ ] forecasts
  - [ ] alerts
  - [ ] radar servers
  - [ ] radar stations
  - [ ] radar station alarms
  - [ ] text products
  - [ ] zones
  - [ ] offices
  - [ ] sigmets
  - [ ] center weather service units
  - [ ] center weather advisories
  - [ ] glossary
- [ ] Create repository services:
  - [ ] locations
  - [ ] weather
  - [ ] alerts
  - [ ] aviation weather
  - [ ] forecast offices
  - [ ] text products
  - [ ] radars
  - [ ] zones

## Interface
- [ ] Create an interactive TUI with Textual
- [ ] Update `main.py` to start the TUI by default
- [ ] Update `main.py` argument parser to let the user specify print output types:
  - [ ] json
  - [ ] plain-text
  - [ ] emoji-text
  - [ ] rich
- [x] Create a `render` subpackage and move `render_rich.py` into it
- [ ] Create additional renderers:
  - [ ] json
  - [ ] plain-text
  - [ ] emoji-text
  - [ ] rich
- [ ] Take some cues from DarkSky, especially when visualizing hourly forecasts:
  - See: https://nightingaledvs.com/dark-sky-weather-data-viz/
- [ ] Explore other TUI projects for inspiration:
  - See: https://github.com/rothgar/awesome-tuis

## Package
- [ ] Move package from `venv` to `(micro)mamba`
- [ ] Set up badges:
  - [ ] GitHub Release
  - [ ] GitHub License
  - [ ] GitHub Actions Workflow Status
    - [ ] Tests
    - [ ] Release to PyPI
  - [ ] GitHub code size
  - [ ] Conda Version
  - [ ] PyPI Version
- [x] Rename `nws` to `nwsc`
- [ ] Remove `pandas` as a dependency
- [ ] Remove `loguru` as a dependency
- [ ] Remove `pytz` as a dependency
- [ ] Finalize dependencies and add them to `pyproject.toml`
- [x] Create resources folder for storing Rich demos and images
- [ ] Review `config.py` to determine if it can be improved
- [ ] Make any needed improvements to `config.py`
- [x] Split `api_temp.py` into separate modules, one for each endpoint
- [ ] Set up GitHub Actions CI/CD to publish new versions of `nwsc` to PyPI

## Documentation
- [x] Find some examples of great project READMEs (See links below for inspo)
  - App images/screenshots in table cells, package structure: https://github.com/supunlakmal/thismypc
  - Markdown alerts: https://github.com/lobehub/lobe-chat#readme
- [x] Determine the structure and contents of the `nwsc` README
- [ ] Find some examples of great API documentation
- [ ] Fully populate *all* docstrings
  - [ ] Move all "See:" reference links from comments above functions to the module-level docstring
- [ ] Generate API documentation with Sphinx
- [ ] Create `docs` folder and put Sphinx docs into it
- [x] Create "API Coverage" checklist in README and identify all API features that are implemented
- [ ] Take static screenshots of some printed outputs
- [ ] Record GIFs showing how to navigate the app to do some basic things

## Testing
- [ ] Write unit tests for every (possible) function in:
  - [ ] `main`
  - [ ] `config`
  - [ ] `api.conversions`
  - [ ] `api.geocode`
  - [ ] `api.get_alerts`
  - [ ] `api.get_aviation`
  - [ ] `api.get_enums`
  - [ ] `api.get_glossary`
  - [ ] `api.get_offices`
  - [ ] `api.get_products`
  - [ ] `api.get_radar`
  - [ ] `api.get_stations`
  - [ ] `api.get_weather`
  - [ ] `api.get_zones`
  - [ ] `render.decorators`
  - [ ] `repository.base_repository`
  - [ ] `repository.in_memory_repository`
  - [ ] `repository.sqlite_repository`
  - [ ] `repository.postgres_repository`
  - [ ] `repository.delta_repository`
  - [ ] `repository.json_repository`
- [ ] Set up GitHub Action(s) to run unit tests

## Miscellaneous
- [x] The `/radar/queues/{host}` endpoint is unexpectedly returning 404 - email the NWS NOC
  - [x] If no response from NOC, submit issue to the github repo (https://github.com/weather-gov/api/discussions/756)