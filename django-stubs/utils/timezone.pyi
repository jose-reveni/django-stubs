from contextlib import ContextDecorator
from datetime import date, datetime, time, timedelta, timezone, tzinfo
from types import TracebackType
from typing import Literal, overload

import zoneinfo  # type: ignore[import-not-found,unused-ignore]

def get_fixed_timezone(offset: timedelta | int) -> timezone: ...
def get_default_timezone() -> zoneinfo.ZoneInfo: ...
def get_default_timezone_name() -> str: ...
def get_current_timezone() -> zoneinfo.ZoneInfo: ...
def get_current_timezone_name() -> str: ...
def activate(timezone: tzinfo | str) -> None: ...
def deactivate() -> None: ...

class override(ContextDecorator):
    timezone: str | tzinfo | None
    old_timezone: tzinfo | None
    def __init__(self, timezone: str | tzinfo | None) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...

def localtime(value: datetime | None = ..., timezone: tzinfo | None = ...) -> datetime: ...
def localdate(value: datetime | None = ..., timezone: tzinfo | None = ...) -> date: ...
def now() -> datetime: ...
@overload
def is_aware(value: time) -> Literal[False]: ...
@overload
def is_aware(value: datetime) -> bool: ...
@overload
def is_naive(value: time) -> Literal[True]: ...
@overload
def is_naive(value: datetime) -> bool: ...
def make_aware(value: datetime, timezone: tzinfo | None = ...) -> datetime: ...
def make_naive(value: datetime, timezone: tzinfo | None = ...) -> datetime: ...
