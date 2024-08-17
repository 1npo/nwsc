# See:
# - https://github.com/weather-gov/api/discussions/478
# - https://weather-gov.github.io/api/general-faqs, especially these sections:
#   - "How do I get a forecast for a location from the API?"
#   - "How do I know I'm getting the latest data? Do I need to use “cache busting” methods?"
API_URL_USCB_GEOCODE = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?benchmark=Public_AR_Current&format=json&address='
API_URL_NWS_POINTS = 'https://api.weather.gov/points/'
API_URL_NWS_GRIDPOINTS = 'https://api.weather.gov/gridpoints/'
API_URL_NWS_STATIONS = 'https://api.weather.gov/stations/'
API_URL_NWS_ALERTS = 'http://api.weather.gov/alerts/'
API_URL_NWS_ALERTS_AREA = 'http://api.weather.gov/alerts/active/area/'
API_URL_NWS_ALERTS_REGION = 'http://api.weather.gov/alerts/active/region/'
API_URL_NWS_ALERTS_ZONE = 'http://api.weather.gov/alerts/active/zone/'
API_URL_NWS_ALERT_TYPES = 'http://api.weather.gov/alerts/types'
API_URL_NWS_ALERT_COUNTS = 'http://api.weather.gov/alerts/active/count'
API_URL_NWS_GLOSSARY = 'https://api.weather.gov/glossary'
API_URL_NWS_SERVERS = 'http://api.weather.gov/radar/servers'
API_URL_NWS_RADAR_STATIONS = 'http://api.weather.gov/radar/stations/'
API_URL_NWS_PRODUCTS = 'http://api.weather.gov/products/'
API_URL_NWS_PRODUCT_TYPES = 'http://api.weather.gov/products/types'
API_URL_NWS_PRODUCT_LOCATIONS = 'http://api.weather.gov/products/locations'
API_URL_NWS_ZONES = 'http://api.weather.gov/zones'
API_URL_NWS_ZONE_FORECASTS = 'http://api.weather.gov/zones/forecast'
API_URL_NWS_OFFICES = 'http://api.weather.gov/offices/'

# See: https://codes.wmo.int/common/unit
WMI_UNIT_MAP = {                            
	'wmoUnit:Pa':               'pa',       # pressure in pascals
	'wmoUnit:km_h-1':           'kmph',     # kilometers per hour
	'wmoUnit:m':                'm',        # meters
	'wmoUnit:percent':          'pc',       # percent
	'wmoUnit:mm':               'mm',       # milimeters
	'wmoUnit:degree_(angle)':   'deg_ang',  # degrees (angle)
	'wmoUnit:degC':             'c',        # degrees celsius
	'wmoUnit:W':				'w',		# watts
	'wmoUnit:dB':				'db',		# decibels
	'F':                        'f',        # degrees fahrenheit
	'nwsUnit:s':				's',		# seconds
}

# See:
# - https://www.atmos.albany.edu/facstaff/ralazear/ATM209/Home_files/METAR_Code.pdf
# - https://en.wikipedia.org/wiki/Okta
METAR_CLOUD_COVER_MAP = {
	'SKC':  'Clear Sky',
	'CLR':  'Clear Sky',
	'FEW':  'Few Clouds',           # 1-2 oktas (1/8 - 2/8 of sky covered)
	'SCT':  'Scattered Clouds',     # 3-4 oktas (3/8 - 4/8 of sky covered)
	'BKN':  'Broken Sky',           # 4-7 oktas (5/8 - 7/8 of sky covered)
	'OVC':  'Overcast',             # 8 oktas (sky completely covered)
}

INVALID_ENUM_MESSAGE_DELIMITER = 'Does not have a value in the enumeration'
FAILED_TO_GET_ENUM_MESSAGE = (
    'Unable to extract list of valid NWS $enum_type from the API. Falling back on hardcoded '
    'values that may be out of date. This is unexpected and a bug, please report the issue '
    'on GitHub at https://github.com/1npo/nwsc/issues.'
)

# As of 2024-8-17:
#
# There isn't an API endpoint for getting a list of valid NWS zones or forecast offices.
# The only way to get these values programmatically is by extracting them from the error
# response string when making a request to:
#
# - /zones/{zoneId} with an invalid zoneId
# - /offices/{officeId} with an invalid officeId
#
# These values are hardcoded to prevent crashing/exceptions in the event that extracting
# these enums fails for some reason (eg due to changes in the structure or format of
# error responses).


VALID_NWS_ZONES = [
    'land',
    'marine',
    'forecast',
    'public',
    'coastal',
    'offshore',
    'fire',
    'county',
]


VALID_NWS_FORECAST_OFFICES = [
	'AKQ', 	'CRP', 	'TSA', 	'LOT', 	'PSR', 
	'ALY', 	'EPZ', 	'ABR', 	'LSX', 	'REV', 
	'BGM', 	'EWX', 	'APX', 	'MKX', 	'SEW', 
	'BOX', 	'FFC', 	'ARX', 	'MPX', 	'SGX', 
	'BTV', 	'FWD', 	'BIS', 	'MQT', 	'SLC', 
	'BUF', 	'HGX', 	'BOU', 	'OAX', 	'STO', 
	'CAE', 	'HUN', 	'CYS', 	'PAH', 	'TFX', 
	'CAR', 	'JAN', 	'DDC', 	'PUB', 	'TWC', 
	'CHS', 	'JAX', 	'DLH', 	'RIW', 	'VEF', 
	'CLE', 	'KEY', 	'DMX', 	'SGF', 	'AER', 
	'CTP', 	'LCH', 	'DTX', 	'TOP', 	'AFC', 
	'GSP', 	'LIX', 	'DVN', 	'UNR', 	'AFG', 
	'GYX', 	'LUB', 	'EAX', 	'BOI', 	'AJK', 
	'ILM', 	'LZK', 	'FGF', 	'BYZ', 	'ALU', 
	'ILN', 	'MAF', 	'FSD', 	'EKA', 	'GUM', 
	'LWX', 	'MEG', 	'GID', 	'FGZ', 	'HPA', 
	'MHX', 	'MFL', 	'GJT', 	'GGW', 	'HFO', 
	'OKX', 	'MLB', 	'GLD', 	'HNX', 	'PPG', 
	'PBZ', 	'MOB', 	'GRB', 	'LKN', 	'STU', 
	'PHI', 	'MRX', 	'GRR', 	'LOX', 	'NH1', 
	'RAH', 	'OHX', 	'ICT', 	'MFR', 	'NH2', 
	'RLX', 	'OUN', 	'ILX', 	'MSO', 	'ONA', 
	'RNK', 	'SHV', 	'IND', 	'MTR', 	'ONP', 
	'ABQ', 	'SJT', 	'IWX', 	'OTX', 	
	'AMA', 	'SJU', 	'JKL', 	'PDT', 	
	'BMX', 	'TAE', 	'LBF', 	'PIH', 	
	'BRO', 	'TBW', 	'LMK', 	'PQR', 	
]
