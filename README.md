<div align='center'>
<img src='https://github.com/1npo/nwsc/blob/main/resources/img/nwsc_logo.png' alt='nwsc logo by http://logomvp.com/, https://x.com/lentesdev; using https://phosphoricons.com/'>

---

**National Weather Service Client**

A full-coverage National Weather Service API client for the terminal

---

*Add badges here*

</div>

> [!WARNING]
> Under active development as of July 2024. This warning will be removed when the project reaches a MVP state.

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
  - [Dependencies](#dependencies)
  - [PyPI](#pypi)
  - [GitHub](#github)
- [Usage](#usage)
  - [Console TUI](#console-tui)
  - [CLI Options](#cli-options)
  - [Configuration](#configuration)
  - [Data Export](#data-export)
- [Endpoint Coverage](#endpoint-coverage)
- [Purpose and Audience](#purpose-and-audience)
- [System Design](#system-design)
  - [App Architecture](#app-architecture)
  - [Data Model](#data-model)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contributing](#contributing)

## Features
- Retrieve data from every available NWS API endpoint (see [Endpoint Coverage](#endpoint-coverage))
- Explore the data with a pretty [Textual](https://textual.textualize.io) interface
- Pretty-print data with [Rich](https://rich.readthedocs.io/en/latest/)
- Print weather strings that can be piped to other tools (such as [i3status](https://i3wm.org/i3status/))
- Export data to various repositories for analytics, reporting, or use by other applications:
  - CSV
  - JSON
  - SQLite
  - Postgres
  - Delta/Spark

## Screenshots
- [ ] Add GIFs and PNGs here

## Installation
### Dependencies
- [`requests-cache`](https://github.com/requests-cache/requests-cache)
- [`loguru`](https://github.com/Delgan/loguru) (*being replaced with stdlib logging*)
- [`rich`](https://github.com/Textualize/rich)
- [`textual`](https://github.com/Textualize/textual)
### PyPI
- [ ] Add PyPI installation instructions here
### GitHub
- [ ] Add instructions for installing from GitHub
  - See: https://stackoverflow.com/questions/15268953/how-to-install-python-package-from-github

## Usage
### Console TUI
- [ ] Describe TUI panels/components
- [ ] List keybindings
### CLI Options
- [ ] Show how to print weather strings for piping
### Configuration
- [ ] Show how to use the configuration manager
- [ ] List available config settings
### Data Export
- [ ] Describe how to set up repositories for data export
- [ ] Describe how to enable/use data export features

## Endpoint Coverage
> [!NOTE]
> **The following endpoints are deprecated by NWS**
> - `/icons/{set}/{timeOfDay}/{first}`
> - `/icons/{set}/{timeOfDay}/{first}/{second}`
> - `/icons`
> - `/thumbnails/satellite/{area}`
> - `/points/{point}/stations`

> [!NOTE] 
> **The following endpoints are unexpectedly responding with a 503/404 (https://github.com/weather-gov/api/discussions/756)**
> - `/radar/queues/{host}`
> - `/radar/profilers/{stationId}`
>
> There's a known issue with the `/radar/queues/{host}` endpoint returning a 503 due to too many records. The workaround is to specify the radar station (`/radar/queues/{host}?station={station_id}`)

> [!NOTE]
> **The following endpoints are unexpectedly returning empty data (https://github.com/weather-gov/api/discussions/759)**
> - `/stations/{stationId}/tafs`
> - `/stations/{stationId}/tafs/{date}/{time}`
> 
> This is a known issue. The workaround is to get TAFs via `/products/types/TAF` or from the [Aviation Weather Center API](https://aviationweather.gov/data/api/#/Data/dataTaf) via their `/data/api/taf` endpoint.

- [x] /alerts
- [x] /alerts/active
- [x] /alerts/active/count
- [x] /alerts/active/zone/{zoneId}
- [x] /alerts/active/area/{area}
- [x] /alerts/active/region/{region}
- [x] /alerts/types
- [x] /alerts/{id}
- [x] /aviation/cwsus/{cwsuId}
- [x] /aviation/cwsus/{cwsuId}/cwas
- [x] /aviation/cwsus/{cwsuId}/cwas/{date}/{sequence}
- [x] /aviation/sigmets
- [x] /aviation/sigmets/{atsu}
- [x] /aviation/sigmets/{atsu}/{date}
- [x] /aviation/sigmets/{atsu}/{date}/{time}
- [x] /glossary
- [x] /gridpoints/{wfo}/{x},{y}
- [x] /gridpoints/{wfo}/{x},{y}/forecast
- [x] /gridpoints/{wfo}/{x},{y}/forecast/hourly
- [x] /gridpoints/{wfo}/{x},{y}/stations
- [ ] ~~/icons/{set}/{timeOfDay}/{first}~~ (**DEPRECATED**)
- [ ] ~~/icons/{set}/{timeOfDay}/{first}/{second}~~ (**DEPRECATED**)
- [ ] ~~/icons~~ (**DEPRECATED**)
- [ ] ~~/thumbnails/satellite/{area}~~ (**DEPRECATED**)
- [x] /stations/{stationId}/observations
- [x] /stations/{stationId}/observations/latest
- [x] /stations/{stationId}/observations/{time}
- [ ] ~~/stations/{stationId}/tafs~~ (**EMPTY RESPONSES**)
- [ ] ~~/stations/{stationId}/tafs/{date}/{time}~~ (**EMPTY RESPONSES**)
- [x] /stations
- [x] /stations/{stationId}
- [x] /offices/{officeId}
- [x] /offices/{officeId}/headlines/{headlineId}
- [x] /offices/{officeId}/headlines
- [x] /points/{point}
- [ ] ~~/points/{point}/stations~~ (**DEPRECATED**)
- [x] /radar/servers
- [x] /radar/servers/{id}
- [x] /radar/stations
- [x] /radar/stations/{stationId}
- [x] /radar/stations/{stationId}/alarms
- [x] /radar/queues/{host}
- [ ] ~~/radar/profilers/{stationId}~~ (**UNEXPECTED 404**)
- [x] /products
- [x] /products/locations
- [x] /products/types
- [x] /products/{productId}
- [x] /products/types/{typeId}
- [x] /products/types/{typeId}/locations
- [x] /products/locations/{locationId}/types
- [x] /products/types/{typeId}/locations/{locationId}
- [x] /zones
- [x] /zones/{type}
- [x] /zones/{type}/{zoneId}
- [x] /zones/{type}/{zoneId}/forecast
- [x] /zones/forecast/{zoneId}/observations
- [x] /zones/forecast/{zoneId}/stations

## Purpose and Audience
I made `nwsc` for myself as a labor of love, mainly for the reasons I list below. But I tried to make it robust, user friendly, and maintainable for anyone else who may find it useful.

- I get my weather from [the National Weather Service](http://weather.gov/), but I have some (very minor) gripes about the website's user experience. I wanted to be able to just type `nwsc` once into a terminal and see all the NWS data I want at a glance, in a visually pleasing way.
- I wanted to start a **serious, high-quality** software project, get an MVP released, and execute it well. This project had just the right stuff to keep me interested, challenged, and motivated long enough to produce an MVP.

## System Design
### App Architecture
<div align='center'>
<img src='https://github.com/1npo/nwsc/blob/main/resources/img/nwsc_architecture.png' alt='nwsc system architecture diagram'>
</div>

- `main.py` is the app's entry point. It parses command-line arguments and runs the app as requested by the user.
- `config.py` provides a simple interface for getting and setting the user's settings.
- `api.*` sends API requests to the NWS endpoints, ensures that measurements are available in both metric and imperial, and formats responses as dataclasses.
- `model.*` provides dataclasses that describe the different kinds of information the NWS API offers, using a standardized naming convention:
  - Weather (current observations and forecasts)
  - Locations (street addresses and their coordinates)
  - [Alerts](https://alerts.weather.gov)
  - [Aviation Weather](https://www.weather.gov/ilm/aviation)
  - [Forecast Offices](https://www.weather.gov/srh/nwsoffices)
  - [Text Products](https://forecast.weather.gov/product_types.php)
  - [Radar Stations, Servers, and Alerts](https://www.weather.gov/nl2/)
  - NWS Zones (land, marine, forecast, public, coastal, offshore, fire, and county)
- `repository.*` provides abstractions for creating, reading, updating, and deleting data in CSV/JSON files and relational databases.
- `service.*` provides a second layer of abstraction that uses `repository.*` to manage the different kinds of information offered by the NWS API.
- `render.*` provides an interactive text-based user interface, and functions for pretty-printing NWS information.

### Data Model
- `alerts`
  - `Alert`
  - `PriorAlert`
  - `AlertCounts`
- `aviation`
  - `SIGMET`
  - `CenterWeatherAdvisory`
  - `CentralWeatherServiceUnit`
- `locations`
  - `Location`
- `offices`
  - `Office`
  - `OfficeHeadline`
- `products`
  - `Product`
  - `ProductLocation`
  - `ProductType`
- `radar`
  - `RadarDataAcquisition`
  - `RadarPerformance`
  - `RadarPathLoss`
  - `RadarAdaptation`
  - `RadarStationAlarm`
  - `RadarQueueItem`
  - `RadarStation`
  - `NetworkInterface`
  - `RadarServer`
- `stations`
  - `Station`
- `weather`
  - `Observation`
  - `ForecastPeriod`
  - `Forecast`
- `zones`
  - `Zone`
  - `ZoneForecastPeriod`
  - `ZoneForecast`

## License
The National Weather Service Client (**nwsc**) is made available under the [MIT License](https://opensource.org/license/mit)

## Acknowledgements
- Logo by [LogoMVP](https://logomvp.com), which was created by [Eduardo Higareda](https://x.com/lentesdev)
- Icon in the logo is from [Phosphor Icons](https://phosphoricons.com/)
- [Bruno](https://www.usebruno.com) and [Swagger UI](https://swagger.io/tools/swagger-ui/) were very helpful for exploring the API
- The presentation of hourly forecast data was inspired by DarkSky, specifically [this article](https://nightingaledvs.com/dark-sky-weather-data-viz/)
- The NWS IT/API team have been responsive on their [GitHub page](https://github.com/weather-gov/api) and helpful with troubleshooting endpoint issues
- Parts of the CSV and JSON repositories come from [Red Bird](https://red-bird.readthedocs.io/en/stable/)'s repository pattern examples

## Contributing
- See [CONTRIBUTING](CONTRIBUTING.md) for instructions on how to contribute to `nwsc`
- See [TODO](TODO.md) for things that need to be done
