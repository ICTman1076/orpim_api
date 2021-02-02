from .engines import DefaultEngine
from .exceptions import *

class ShortenedURL:
    def __init__(self, data, target=None):
        self.rawData = data
        if target != None:
            self.id = None
            self.sub = data["final_domain"].split(".")[0]
            self.domain = ".".join(data["final_domain"].split(".")[1:])
            self.link = data["final_link"]
            self.target = target
            self.user = None
            self.disabled = None
            self.counter = None
            self.cost = None
            self.premium_needed_at_creation = None
        else:
            self.id = data["id"]
            self.sub = data["sub"]
            self.domain = data["domain"]
            self.link = data["link"]
            self.target = data["target"]
            self.user = data["user"]
            self.disabled = data["disabled"]
            self.counter = data["counter"]
            self.cost = data["cost"]
            self.premium_needed_at_creation = data["premium_needed_at_creation"]
        self.fullLink = self.sub+"."+self.domain+"/"+self.link


class OrpIM:
    def __init__(self, token, engine=DefaultEngine):
        self._token = token
        self._engine = engine()
    
    def shortenUrl(self, target, shortcode=None, domain="dcr.gg"):
        data = {
            "target": target,
            "domain": domain,
            "token": self._token
        }
        if shortcode:
            data["link"] = shortcode
        result = self._engine.sendReq("/create", data)
        if result["success"]:
            return ShortenedURL(result, target)
        else:
            if "already registered" in result["message"]:
                raise LinkTaken(data["message"])
            elif "not a valid target" in result["message"]:
                validTargets = result["message"].split("<br>")
                raise InvalidTarget(domain+" links must only use the following targets: "+validTargets)
            elif "domain requires a premium tier" in data["message"]:
                raise MissingDomainPermission("A non-premium token cannot be used for premium domains.")
            elif "private" in data["message"]:
                raise MissingDomainPermission("This token does not have access to "+domain)
            else:
                # an un-accounted for error should just generically exception
                raise Exception(data["message"])

    def listUrls(self):
        data = {"token": self._token}
        result = self._engine.sendReq("/list", data)
        results = []
        for item in result:
            results.append(ShortenedURL(item))
        return results
        
