class ServiceError(Exception):
    pass


class PostServiceError(ServiceError):
    pass


class AuthorServiceError(ServiceError):
    pass
