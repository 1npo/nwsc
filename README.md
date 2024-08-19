<div align='center'>
<img src='https://github.com/1npo/nwsc/blob/main/resources/img/nwsc-logo.png' alt='nwsc logo by http://logomvp.com/, https://x.com/lentesdev; using https://phosphoricons.com/'>

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
  - [Package Structure](#package-structure)
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

> [!NOTE] 
> **The following endpoints are unexpectedly responding with a 404 (https://github.com/weather-gov/api/discussions/756)**
> - `/radar/queues/{host}`
> - `/radar/profilers/{stationId}`

> [!NOTE]
> **The following endpoints are unexpectedly returning empty data (https://github.com/weather-gov/api/discussions/759)**
> - `/stations/{stationId}/tafs`
> - `/stations/{stationId}/tafs/{date}/{time}`

- [x] /alerts
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
- [ ] /offices/{officeId}
- [ ] /offices/{officeId}/headlines/{headlineId}
- [ ] /offices/{officeId}/headlines
- [x] /points/{point}
- [x] /points/{point}/stations
- [x] /radar/servers
- [x] /radar/servers/{id}
- [x] /radar/stations
- [x] /radar/stations/{stationId}
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
- [x] /zones
- [x] /zones/{type}
- [x] /zones/{type}/{zoneId}
- [x] /zones/{type}/{zoneId}/forecast
- [x] /zones/forecast/{zoneId}/observations
- [x] /zones/forecast/{zoneId}/stations

## Purpose and Audience
I made `nwsc` mainly for myself, for a few reasons I list below. But I tried to design and build it well so that others might enjoy it or find it useful.

- I get my weather from [the National Weather Service](http://weather.gov/), but I have some (very minor) gripes about the website's user experience. I wanted to be able to just type `nwsc` once into a terminal and see all the NWS data I want at a glance, in a visually pleasing way.
- I wanted to start and *actually finish* a "serious" software project, and this one had enough elements to keep me interested and motivated long enough to produce an MVP.
- I think it's so cool that we can see so much detail about the status of the nation's weather radars, even down to how full a generator's fuel tank is. So I thought it would be neat to see all this data presented in a nice way.

## System Design
### App Architecture
- [ ] Create application architecture diagram, export to PNG
- [ ] Add diagram to `resources.img` and embed here
### Data Model
- [ ] Describe dataclasses here
### Package Structure
- [ ] Describe package structure here

## License
The National Weather Service Client (**nwsc**) is made available under the [MIT License](https://opensource.org/license/mit)

## Acknowledgements
- Logo by [LogoMVP](https://logomvp.com), which was created by [Eduardo Higareda](https://x.com/lentesdev)
- Icon in the logo is from [Phosphor Icons](https://phosphoricons.com/)
- [Bruno](https://www.usebruno.com) and [Swagger UI](https://swagger.io/tools/swagger-ui/) were very helpful for exploring the API
- The presentation of hourly forecast data was inspired by DarkSky, specifically [this article](https://nightingaledvs.com/dark-sky-weather-data-viz/)

## Contributing
- See [CONTRIBUTING](CONTRIBUTING.md) for instructions on how to contribute to `nwsc`
- See [TODO](TODO.md) for things that need to be done
