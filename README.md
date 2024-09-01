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
- [Getting Started](#getting-started)
  - [How to start the TUI](#how-to-start-the-tui)
  - [How to pretty-print NWS information](#how-to-pretty-print-nws-information)
  - [How to print pipeable weather strings](#how-to-print-pipeable-weather-strings)
- [Purpose and Audience](#purpose-and-audience)
- [Documentation](#documentation)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contributing](#contributing)

## Features
- Retrieve data from every available NWS API endpoint
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

## Getting Started
### How to start the TUI
- [ ] Describe TUI panels/components
- [ ] List keybindings
### How to pretty-print NWS information
- [ ] Show how to pretty-print NWS information to the terminal (STDOUT)
### How to print pipeable weather strings
- [ ] Show how to create weather strings that can be piped to other tools

## Purpose and Audience
I made `nwsc` for myself for these reasons:

- For fun
- I get my weather from [the National Weather Service](http://weather.gov/), but I have some (very minor) gripes about the website's user experience. So I wanted to be able to just type `nwsc` once into a terminal and see all the NWS data I want at a glance, in a way that I find visually pleasing.
- I wanted to start and finish a MVP for a moderately complex software project, and execute it well. Meaning the MVP:
  - Provides all the listed features
  - Is robust (ie, has full test coverage and all tests pass)
  - Is well-documented
  - Is user-friendly

## Documentation
> [!NOTE]
> The content of these markdown files will eventually move into the Sphinx docs
- [Endpoint Coverage](docs/endpoint_coverage.md)
- [System Design](docs/system_design.md)
- [Configuration](docs/configuration.md)

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
