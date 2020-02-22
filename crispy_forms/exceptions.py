class CrispyError(Exception):
    pass


class FormHelpersException(CrispyError):
    """
    This is raised when building a form via helpers throws an error.
    We want to catch form helper errors as soon as possible because
    debugging templatetags is never fun.
    """

    pass


class DynamicError(CrispyError):
    pass
