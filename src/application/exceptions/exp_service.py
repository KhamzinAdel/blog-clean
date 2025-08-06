class ServiceError(Exception):
    pass


class PostServiceError(ServiceError):
    pass


class AuthorServiceError(ServiceError):
    pass


class InvalidAccessToken(ServiceError):
    pass


class InvalidRefreshToken(ServiceError):
    pass


class InvalidScopeToken(ServiceError):
    pass


class ExpiredAccessToken(ServiceError):
    pass


class ExpiredRefreshToken(ServiceError):
    pass
