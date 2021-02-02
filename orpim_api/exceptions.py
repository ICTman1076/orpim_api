class InvalidToken(PermissionError):
    pass

class MissingDomainPermission(PermissionError):
    pass

class LinkTaken(IsADirectoryError):
    pass

class InvalidTarget(ValueError):
    pass