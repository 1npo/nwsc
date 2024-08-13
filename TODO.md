# TODO

## nws/main.py

- [ ] Add argument: 

## nws/get_data.py

- [ ] Fix wind_speed_str error
- [ ] Create barometric_pressure columns for in_hg and bm
- [ ] Cast columns as int:
    - [ ] observations:
        - [ ] relative_humidity_pc
    - [x] forecast:
        - [x] dew_point_deg_c
        - [x] temperature_deg_c
- [ ] Round columns to 2 decimal places:
    - [ ] observations:
        - [ ] relative_humidity_pc
        - [ ] wind_chill_deg_c
        - [ ] wind_chill_deg_f
        - [ ] wind_speed_m_hr
        - [ ] station_elevation_mi
        - [ ] visibility_mi
        - [ ] cloud_layers_mi

## nws/render.py

- [ ] Create an improved rich_print_overview
- [ ] Create a live/scrollable rich_display_hourly_forecast