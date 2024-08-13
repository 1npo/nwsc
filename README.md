# nwsc
A text-based full-coverage National Weather Service API client.
Logo by logomvp.com
# Endpoint Coverage
- [ ] /alerts **N/A**
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
- [ ] /icons/{set}/{timeOfDay}/{first} **DEPRECATED**
- [ ] /icons/{set}/{timeOfDay}/{first}/{second} **DEPRECATED**
- [ ] /icons **DEPRECATED**
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
- [ ] /radar/servers/{id} **N/A**
- [x] /radar/stations
- [ ] /radar/stations/{stationId}
- [ ] /radar/stations/{stationId}/alarms
- [ ] /radar/queues/{host} **UNEXPECTED 404**
- [ ] /radar/profilers/{stationId} **UNEXPECTED 404**
- [ ] /products
- [ ] /products/locations
- [ ] /products/types
- [ ] /products/{productId}
- [ ] /products/types/{typeId}
- [ ] /products/types/{typeId}/locations
- [ ] /products/locations/{locationId}/types
- [ ] /products/types/{typeId}/locations/{locationId}
- [ ] /zones
- [ ] /zones/{type}
- [ ] /zones/{type}/{zoneId}
- [ ] /zones/{type}/{zoneId}/forecast
- [ ] /zones/forecast/{zoneId}/observations
- [ ] /zones/forecast/{zoneId}/stations
# TODO
## Data
- [ ] Finish writing API request functions for all endpoints
- [x] Finish fleshing out dataclasses for all NWS data
- [ ] Update `api.py` to use dataclasess instead of dicts
- [x] Add wind speed/direction string and measurement conversions to `api.py` without using dataframes
- [x] Create a `repository` subpackage for recording historical weather responses
- [ ] Create repositories:
  - [ ] in-memory
  - [ ] sqlite
  - [ ] postgresql
  - [ ] delta
- [ ] Revamp or remove `cache.py`: use `requests-cache` instead of rolling your own cache manager
## Interface
- [ ] Create an interactive TUI with Textual
- [ ] Update `main.py` to start the TUI by default
- [ ] Update `main.py` argument parser to let the user specify output types:
  - [ ] json
  - [ ] plain-text
  - [ ] emoji-text
  - [ ] rich-table
- [ ] Clean up and improve the quality of `render.py` and rename it to `render_rich.py`
- [ ] Create a `render` subpackage and move `render_rich.py` into it
- [ ] Create additional renderers:
  - [ ] json
  - [ ] text
  - [ ] matplotlib
## Package
- [x] Rename `nws` to `nwsc`
- [ ] Remove `pandas` as a dependency
- [ ] Review `config.py` to determine if it can be improved
- [ ] Make any needed improvements to `config.py`
- [ ] Split `api.py` into separate modules, one for each endpoint
## Documentation
- [ ] Find some examples of great project READMEs
- [ ] Find some examples of great API documentation
- [ ] Fully populate *all* docstrings
- [ ] Generate API documentation with Sphinx
- [ ] Fully flesh out nwsc READMEs
- [ ] Create "API Coverage" checklist in README and identify all API features that are implemented
## Testing
- [ ] Create unit tests for every function
## Contribution
- [ ] The /radar/queues/{host} is unexpectedly returning 404 - submit an issue
# Resources
- https://docs.scalar.com/swagger-editor
# Notes
- RE: /product* endpoints: Get only the list of product types when starting nwsc. Make additional requests only when prompted by the user.