# orpim_api
A simple python API wrapper for the [orp.im](https://orp.im) URL shortener.

## Requirements
You'll want to [get an orp.im token](https://orp.im/gettoken). We thoroughly encourage you
to consider the premium option - you'll get exclusive domains and more room to get new links
(which could be vital for production environments).

Alternatively, you can ask your users to provide their own tokens, by signing in at
https://orp.im/gettoken.

## Documentation
To use the library, instantiate a class like so:

```
from orpim_api import OrpIM
orp = OrpIM(token[, engine])
```

- `token` is the user's API token.
- `engine` can be [anything that inherits from engines.BaseEngine](https://github.com/ICTman1076/orpim_api/blob/0.1/orpim_api/engines.py).
  A default implementation with urllib is given.

### Creating a url
```
orp.shortenUrl(target[, shortcode[, domain]])
```

- `target` - where you want the URL to lead
- `shortcode` - the bit after the / in the link (if left out or set to `None`, the API will
  generate one automatically)
- `domain` - the domain to use. You may use any domain that is accessible to you when
  generating a link manually. Defaults to dcr.gg

Returns: Incomplete [`ShortenedURL` object](https://github.com/ICTman1076/orpim_api#shortenedurl-object)

Errors:
- `exceptions.MissingDomainPermission` - The user doesn't have access to this domain, either 
  because it's a private domain or the domain is a premium domain and the user is not premium.
- `exceptions.LinkTaken` - The link you are trying to register is already taken.
- `exceptions.InvalidTarget` - The target link is not allowed on this domain.
- `exceptions.InvalidToken` - The token is invalid.

### Listing all your URLs
```
orp.listUrls()
```

Returns: A list of [`ShortenedURL` object](https://github.com/ICTman1076/orpim_api#shortenedurl-object)s

Errors:
- `exceptions.InvalidToken` - The token is invalid.

### `ShortenedURL` object
You'll never need to instantiate one. It has the following properties:

- `ShortenedURL.id`* - Internal link ID.
- `ShortenedURL.sub` - Subdomain (usually `www`) of link
- `ShortenedURL.domain` - Domain of link
- `ShortenedURL.link` - Shortcode (after `/`) of link
- `ShortenedURL.target` - URL to which link redirects
- `ShortenedURL.user`* - User to whom the link belongs
- `ShortenedURL.disabled`* - Disabled status of link. Anything but 0 = disabled.
- `ShortenedURL.counter`* - Number of times link has been visited
- `ShortenedURL.cost`* - Amount of credits this link is using (and thus deletion would
  return to the user)
- `ShortenedURL.premium_needed_at_creation`* - the level of premium needed to create the
  link when it was created.

If a property is marked with a *, it means it may not appear in incomplete versions
of this object (and will be set to `None`)

https://api.orp.im/ has details on the API, and as the library closely mirrors the API
it works as fallback documentation.