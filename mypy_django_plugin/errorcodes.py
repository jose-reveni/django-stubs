from mypy.errorcodes import ErrorCode

MANAGER_UNTYPED = ErrorCode("django-manager", "Untyped manager disallowed", "Django")
MANAGER_MISSING = ErrorCode("", "Couldn't resolve manager for model", "Django")
