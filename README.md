<div align='center'>
<img src='https://github.com/1npo/nwsc/blob/main/resources/img/nwsc-logo.png' alt='nwsc logo by http://logomvp.com/, https://x.com/lentesdev; using https://phosphoricons.com/'>

---

**National Weather Service Client**

A full-coverage National Weather Service API client for the terminal. Made for weather nerds.

---

*Add badges here*

*Add screenshot here*

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
  - [Configuration](#configuration)
  - [Data Export](#data-export)
- [Endpoint Coverage](#endpoint-coverage)
- [Architecture](#architecture)
- [License](#license)
- [Credits](#credits)
- [Contributing](#contributing)

## Features
- Retrieve data from every* available NWS API endpoint [(see Endpoint Coverage section)](#endpoint-coverage)
- Explore the data with a pretty [Textual](https://textual.textualize.io) interface
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
- [x] /zones
- [x] /zones/{type}
- [x] /zones/{type}/{zoneId}
- [x] /zones/{type}/{zoneId}/forecast
- [x] /zones/forecast/{zoneId}/observations
- [x] /zones/forecast/{zoneId}/stations

## Architecture
- [ ] Create application architecture diagram, export to PNG
- [ ] Add diagram to `resources.img` and embed here

## License
The National Weather Service Client (**nwsc**) is made available under the [MIT License](https://opensource.org/license/mit)

## Credits
- Logo by [LogoMVP](https://logomvp.com), which was created by [Eduardo Higareda](https://x.com/lentesdev)
- Icon in the logo is from [Phosphor Icons](https://phosphoricons.com/)
- [Bruno](https://www.usebruno.com) and [Swagger UI](https://swagger.io/tools/swagger-ui/) were very helpful for exploring the API

## Contributing
- See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on how to contribute to `nwsc`.
- See [TODO.md](TODO.md) for things that need to be done.
