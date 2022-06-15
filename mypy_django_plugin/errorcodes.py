from mypy.errorcodes import ErrorCode

MANAGER_UNTYPED = ErrorCode("django-manager", "Untyped manager disallowed", "Django")
MANAGER_MISSING = ErrorCode("django-manager-missing", "Couldn't resolve related manager for model", "Django")
