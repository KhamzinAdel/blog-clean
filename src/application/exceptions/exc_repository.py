
class RepositoryError(Exception):
    pass


class NotFoundInfoException(RepositoryError):
    pass


class NotDependencyRelationshipException(RepositoryError):
    pass


class UniqueForeignException(RepositoryError):
    pass


class DataEmptyException(RepositoryError):
    pass


class NonCorrectFormatException(RepositoryError):
    pass


class NotPerformedActionException(RepositoryError):
    pass
