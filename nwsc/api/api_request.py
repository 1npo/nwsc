import pytz
from datetime import datetime
from requests_cache import CachedSession


def api_request(session: CachedSession, url: str) -> dict:
	return session.get(url).json()


def parse_timestamp(timestamp: str) -> datetime | None:
	if timestamp:
		return datetime.fromisoformat(timestamp).astimezone(pytz.timezone('US/Eastern')).replace(tzinfo=None)
