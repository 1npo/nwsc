# Endpoint Coverage

> [!NOTE]
> The following endpoints are deprecated by NWS
> - `/icons/{set}/{timeOfDay}/{first}`
> - `/icons/{set}/{timeOfDay}/{first}/{second}`
> - `/icons`
> - `/thumbnails/satellite/{area}`
> - `/points/{point}/stations`

> [!NOTE] 
> The `/radar/profilers/{stationId}` endpoint is unexpectedly responding with a 404

> [!NOTE]
> The `/radar/queues/{host}` endpoint is unexpectedly responding with a 503
> 
> This is a known issue (https://github.com/weather-gov/api/discussions/756). The endpoint returns too many records. The workaround is to specify the radar station: `/radar/queues/{host}?station={station_id}`.

> [!NOTE]
> The following endpoints are unexpectedly returning empty data
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
