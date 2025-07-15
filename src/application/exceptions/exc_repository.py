class RepositoryError(Exception):
    pass


class NotFoundInfoException(RepositoryError):
    pass


class NotPerformedActionException(RepositoryError):
    pass
