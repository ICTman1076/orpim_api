from .exceptions import InvalidToken
import urllib.request as urllib
import urllib.parse as urlparse
import json
class BaseEngine:
    def __init__(self, base="https://api.orp.im/v0"):
        self._base = base

    def sendReq(self, endpoint, values):
        url = self._base + endpoint
        data = self._webRequest(url, values)
        try:
            if not data["success"]:
                if data["message"] == "Invalid API Token":
                    raise InvalidToken(data["message"])
                else:
                    return data # let the caller deal with it
            else:
                return data
        except TypeError:
            return data

    def _webRequest(self, url, value):
        raise NotImplementedError("Whoever wrote this library forgot to implement this engine properly. Try using another engine.")

class DefaultEngine(BaseEngine):
    def _webRequest(self, url, values):
        getstring = urlparse.urlencode(values)
        url = url + "?" + getstring

        res = urllib.urlopen(url)

        dataStr = res.read()
        data = json.loads(dataStr)
        return data