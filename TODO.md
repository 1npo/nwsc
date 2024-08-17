# `nwsc` TODOs
## Data
- [ ] Finish writing API request functions for all endpoints
- [ ] Finish fleshing out dataclasses for all NWS data
- [ ] Update `api.py` to use dataclasess instead of dicts
- [x] Add wind speed/direction string and measurement conversions to `api.py` without using dataframes
- [x] Create a `repository` subpackage for recording historical weather responses
- [ ] Fix `get_zone_stations` - it's returning an empty list
  - [ ] Re-generate `tests/test_data/nws_raw_zone_stations.json`
- [x] Revamp or remove `cache.py`: use `requests-cache` instead of rolling your own cache manager
## Repository
- [ ] Create repository modules:
  - [ ] `in-memory`
  - [ ] `sqlite`
  - [ ] `postgresql`
  - [ ] `delta`
## Interface
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
## Package
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
- [ ] Find some examples of great project READMEs
- [ ] Find some examples of great API documentation
- [ ] Fully populate *all* docstrings
  - [ ] Move all "See:" reference links from comments above functions to the module-level docstring
- [ ] Generate API documentation with Sphinx
- [x] Create "API Coverage" checklist in README and identify all API features that are implemented
## Testing
- [ ] Write unit tests for every (possible) function in:
  - [ ] `main`
  - [ ] `config`
  - [ ] `api.conversions`
  - [ ] `api.geocode`
  - [ ] `api.get_alerts`
  - [ ] `api.get_glossary`
  - [ ] `api.get_offices`
  - [ ] `api.get_products`
  - [ ] `api.get_radar`
  - [ ] `api.get_stations`
  - [ ] `api.get_weather`
  - [ ] `api.get_zones`
  - [ ] `render.decorators`
  - [ ] `repository.base`
  - [ ] `repository.in_memory`
  - [ ] `repository.sqlite`
  - [ ] `repository.postgres`
  - [ ] `repository.delta`
## Miscellaneous
- [x] The `/radar/queues/{host}` endpoint is unexpectedly returning 404 - email the NWS NOC
  - [x] If no response from NOC, submit issue to the github repo (https://github.com/weather-gov/api/discussions/756)