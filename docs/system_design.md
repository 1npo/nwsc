# System Design
## Architecture
<div align='center'>
<img src='https://github.com/1npo/nwsc/blob/main/resources/img/nwsc_architecture.png' alt='nwsc system architecture diagram'>
</div>

## Data Retrieval
1. Any data that doesn't come directly from the user (eg location data and configuration settings) is retrieved from an API endpoint
2. Whenever the user initiates an API request, cached responses are always used until they expire
3. The user can choose to retrieve data from a repository instead of from the API
4. Response data is transformed and loaded into dataclasses "at the seams", meaning:
  - Immediately after receiving an API response (either from the network or the cache)
  - Immediately after retrieving records from a repository

## Data Model
The NWS API exposes different kinds of weather-related information. This app uses dataclasses to model and describe that information.

### Available Information
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
- Miscellaneous
  - Glossary
  - Types
  - Enums

### Dataclasses
- **`alerts`**
  - `Alert`
  - `PriorAlert`
  - `AlertCounts`
- **`aviation`**
  - `SIGMET`
  - `CenterWeatherAdvisory`
  - `CentralWeatherServiceUnit`
- **`glossary`**
  - **`Glossary`**
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

### Entity-Relationship Diagrams
#### Alerts
<div align='center'>
<img src='https://github.com/1npo/nwsc/blob/main/resources/img/erd/erd_alerts.png' alt='erd for alerts'>
</div>

#### Aviation
<div align='center'>
<img src='https://github.com/1npo/nwsc/blob/main/resources/img/erd/erd_aviation.png' alt='erd for aviation'>
</div>

#### Locations
<div align='center'>
<img src='https://github.com/1npo/nwsc/blob/main/resources/img/erd/erd_locations.png' alt='erd for alerts'>
</div>

#### Offices
<div align='center'>
<img src='https://github.com/1npo/nwsc/blob/main/resources/img/erd/erd_offices.png' alt='erd for alerts'>
</div>

#### Products
<div align='center'>
<img src='https://github.com/1npo/nwsc/blob/main/resources/img/erd/erd_products.png' alt='erd for alerts'>
</div>

#### Radars
<div align='center'>
<img src='https://github.com/1npo/nwsc/blob/main/resources/img/erd/erd_radars.png' alt='erd for alerts'>
</div>

#### Stations
<div align='center'>
<img src='https://github.com/1npo/nwsc/blob/main/resources/img/erd/erd_stations.png' alt='erd for alerts'>
</div>

#### Weather
<div align='center'>
<img src='https://github.com/1npo/nwsc/blob/main/resources/img/erd/erd_weather.png' alt='erd for alerts'>
</div>

#### Zones
<div align='center'>
<img src='https://github.com/1npo/nwsc/blob/main/resources/img/erd/erd_zones.png' alt='erd for alerts'>
</div>
