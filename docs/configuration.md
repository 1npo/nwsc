# Configuration
- [ ] Describe how to configure `nwsc`

## Available User Settings
> [!WARNING]
> **It is strongly advised not to disable caching, for a few reasons:**
> 1. The NWS API responses include cache-control headers to tell you when a response will expire.
>   - You will always get the same response until that expiration date.
> 2. This API client uses `requests-cache` to cache responses, and will only make network calls when a response has expired.
> 3. Repositories use the response `created_at` date as part of the primary key in almost all tables.
>   - So if you disable cache and make many requests, you will add redundant data to your repository.
>   - For example, if you get a response that expires tomorrow, and then repeat the request 4 times, you will have 5 copies of the same response in your repository. Only the response timestamp will be different.

| Setting Name | Setting Type | Default Value
| --- | --- | --- |
| foo | bar | baz |

## Data Export
- [ ] Describe how to set up repositories for data export
- [ ] Describe how to enable/use data export features
