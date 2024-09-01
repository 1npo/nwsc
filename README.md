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
  - [Available User Settings](#available-user-settings)
  - [Data Export](#data-export)
- [Endpoint Coverage](#endpoint-coverage)
- [Purpose and Audience](#purpose-and-audience)
- [System Design](#system-design)
  - [Architecture](#architecture)
  - [Data Retrieval](#data-retrieval)
  - [Data Model](#data-model)
    - [Available Information](#available-information)
    - [Dataclasses](#dataclasses)
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
- [ ] Describehow to use the configuration manager
### Available User Settings
> ![WARNING]
> It is strongly advised not to disable caching, for a few reasons:
> 1. The NWS API responses include cache-control headers to tell you when a response will expire. You will always get the same response until that expiration date.
> 2. This API client uses `requests-cache` to cache responses, and will only make network calls when a response has expired.
> 3. Repositories use the response `created_at` date as part of the primary key in almost all tables. So if you disable cache and make many requests, you will add redundant data to your repository.

| Name | Type | Default Value
| --- | --- | --- |
| foo | bar | baz |
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
> **The `/radar/profilers/{stationId}` endpoint is unexpectedly responding with a 404**

> [!NOTE]
> **The `/radar/queues/{host}` endpoint is unexpectedly responding with a 503**
> 
> This is a known issue (https://github.com/weather-gov/api/discussions/756). The endpoint returns too many records. The workaround is to specify the radar station: `/radar/queues/{host}?station={station_id}`.

> [!NOTE]
> **The following endpoints are unexpectedly returning empty data**
> - `/stations/{stationId}/tafs`
> - `/stations/{stationId}/tafs/{date}/{time}`
> 
> This is a known issue (https://github.com/weather-gov/api/discussions/759). The workaround is to get TAFs via `/products/types/TAF` or from the [Aviation Weather Center API](https://aviationweather.gov/data/api/#/Data/dataTaf) via their `/data/api/taf` endpoint.

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
### Architecture
<div align='center'>
<img src='https://github.com/1npo/nwsc/blob/main/resources/img/nwsc_architecture.png' alt='nwsc system architecture diagram'>
</div>

### Data Retrieval
1. Any data that doesn't come directly from the user (eg location data and configuration settings) is retrieved from an API endpoint
2. All API responses are cached by `request-cache` unless caching is disabled by the user
3. 
### Data Model
The NWS API exposes different kinds of weather-related information. This app uses dataclasses to model and describe that information.

#### Available Information
> [!NOTE]
> Location information is part of the data model, but it's the only item that doesn't come from the NWS API. Street addresses come from the user, and coordinates come from the [USCB geocoding service](https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html).

- Locations (street addresses and their coordinates)
- Weather (current observations and forecasts)
- [Alerts](https://alerts.weather.gov)
- [Aviation Weather](https://www.weather.gov/ilm/aviation)
- [Forecast Offices](https://www.weather.gov/srh/nwsoffices)
- [Text Products](https://forecast.weather.gov/product_types.php)
- [Radar Stations, Servers, and Alerts](https://www.weather.gov/nl2/)
- NWS Zones (land, marine, forecast, public, coastal, offshore, fire, and county)

#### Dataclasses
- **`alerts`**
  - `Alert`
  - `PriorAlert`
  - `AlertCounts`
- **`aviation`**
  - `SIGMET`
  - `CenterWeatherAdvisory`
  - `CentralWeatherServiceUnit`
- **`locations`**
  - `Location`
- **`offices`**
  - `Office`
  - `OfficeHeadline`
- **`products`**
  - `Product`
  - `ProductLocation`
  - `ProductType`
- **`radar`**
  - `RadarDataAcquisition`
  - `RadarPerformance`
  - `RadarPathLoss`
  - `RadarAdaptation`
  - `RadarStationAlarm`
  - `RadarQueueItem`
  - `RadarStation`
  - `NetworkInterface`
  - `RadarServer`
- **`stations`**
  - `Station`
- **`weather`**
  - `Observation`
  - `ForecastPeriod`
  - `Forecast`
- **`zones`**
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
- Street address geocoding is done using the US Census Bureau's [geocoding service](https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html)

## Contributing
- See [CONTRIBUTING](CONTRIBUTING.md) for instructions on how to contribute to `nwsc`
- See [TODO](TODO.md) for things that need to be done
