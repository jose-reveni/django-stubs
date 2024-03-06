from collections.abc import Iterable, Mapping
from io import BytesIO
from re import Pattern
from typing import Any, BinaryIO, Literal, NoReturn, TypeVar, overload, type_check_only

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.base import SessionBase
from django.contrib.sites.models import Site
from django.core.files import uploadedfile, uploadhandler
from django.urls import ResolverMatch
from django.utils.datastructures import CaseInsensitiveMapping, ImmutableList, MultiValueDict
from django.utils.functional import cached_property
from typing_extensions import Self, TypeAlias

RAISE_ERROR: object
host_validation_re: Pattern[str]

class UnreadablePostError(OSError): ...
class RawPostDataException(Exception): ...

UploadHandlerList: TypeAlias = list[uploadhandler.FileUploadHandler] | ImmutableList[uploadhandler.FileUploadHandler]

class HttpHeaders(CaseInsensitiveMapping[str]):
    HTTP_PREFIX: str
    UNPREFIXED_HEADERS: set[str]
    def __init__(self, environ: Mapping[str, Any]) -> None: ...
    @classmethod
    def parse_header_name(cls, header: str) -> str | None: ...
    @classmethod
    def to_wsgi_name(cls, header: str) -> str: ...
    @classmethod
    def to_asgi_name(cls, header: str) -> str: ...
    @classmethod
    def to_wsgi_names(cls, headers: Mapping[str, Any]) -> dict[str, Any]: ...
    @classmethod
    def to_asgi_names(cls, headers: Mapping[str, Any]) -> dict[str, Any]: ...

class HttpRequest(BytesIO):
    GET: _ImmutableQueryDict
    POST: _ImmutableQueryDict
    COOKIES: dict[str, str]
    META: dict[str, Any]
    FILES: MultiValueDict[str, uploadedfile.UploadedFile]
    path: str
    path_info: str
    method: str | None
    resolver_match: ResolverMatch | None
    content_type: str | None
    content_params: dict[str, str] | None
    _body: bytes
    _stream: BinaryIO
    # Attributes added by optional parts of Django
    # django.contrib.admin views:
    current_app: str
    # django.contrib.auth.middleware.AuthenticationMiddleware:
    user: AbstractBaseUser | AnonymousUser
    # django.middleware.locale.LocaleMiddleware:
    LANGUAGE_CODE: str
    # django.contrib.sites.middleware.CurrentSiteMiddleware
    site: Site
    # django.contrib.sessions.middleware.SessionMiddleware
    session: SessionBase
    # The magic. If we instantiate HttpRequest directly somewhere, it has
    # mutable GET and POST. However, both ASGIRequest and WSGIRequest have immutable,
    # so when we use HttpRequest to refer to any of them we want exactly this.
    # Case when some function creates *exactly* HttpRequest (not subclass)
    # remain uncovered, however it's probably the best solution we can afford.
    def __new__(cls) -> _MutableHttpRequest: ...
    # When both __init__ and __new__ are present, mypy will prefer __init__
    # (see comments in mypy.checkmember.type_object_type)
    # def __init__(self) -> None: ...
    def get_host(self) -> str: ...
    def get_port(self) -> str: ...
    def get_full_path(self, force_append_slash: bool = ...) -> str: ...
    def get_full_path_info(self, force_append_slash: bool = ...) -> str: ...
    def get_signed_cookie(
        self, key: str, default: Any = ..., salt: str = ..., max_age: int | None = ...
    ) -> str | None: ...
    def get_raw_uri(self) -> str: ...
    def build_absolute_uri(self, location: str | None = ...) -> str: ...
    @property
    def scheme(self) -> str | None: ...
    def is_secure(self) -> bool: ...
    def is_ajax(self) -> bool: ...
    @property
    def encoding(self) -> str | None: ...
    @encoding.setter
    def encoding(self, val: str) -> None: ...
    @property
    def upload_handlers(self) -> UploadHandlerList: ...
    @upload_handlers.setter
    def upload_handlers(self, upload_handlers: UploadHandlerList) -> None: ...
    @cached_property
    def accepted_types(self) -> list[MediaType]: ...
    def parse_file_upload(
        self, META: Mapping[str, Any], post_data: BinaryIO
    ) -> tuple[QueryDict, MultiValueDict[str, uploadedfile.UploadedFile]]: ...
    @cached_property
    def headers(self) -> HttpHeaders: ...
    @property
    def body(self) -> bytes: ...
    def _load_post_and_files(self) -> None: ...
    def accepts(self, media_type: str) -> bool: ...

@type_check_only
class _MutableHttpRequest(HttpRequest):
    GET: QueryDict  # type: ignore[assignment]
    POST: QueryDict  # type: ignore[assignment]

_Z = TypeVar("_Z")

class QueryDict(MultiValueDict[str, str]):
    _mutable: bool
    # We can make it mutable only by specifying `mutable=True`.
    # It can be done a) with kwarg and b) with pos. arg. `overload` has
    # some problems with args/kwargs + Literal, so two signatures are required.
    # ('querystring', True, [...])
    @overload
    def __init__(
        self: QueryDict,
        query_string: str | bytes | None,
        mutable: Literal[True],
        encoding: str | None = ...,
    ) -> None: ...
    # ([querystring='string',] mutable=True, [...])
    @overload
    def __init__(
        self: QueryDict,
        *,
        mutable: Literal[True],
        query_string: str | bytes | None = ...,
        encoding: str | None = ...,
    ) -> None: ...
    # Otherwise it's immutable
    @overload
    def __init__(  # type: ignore[misc]
        self: _ImmutableQueryDict,
        query_string: str | bytes | None = ...,
        mutable: bool = ...,
        encoding: str | None = ...,
    ) -> None: ...
    @classmethod
    def fromkeys(  # type: ignore[override]
        cls,
        iterable: Iterable[bytes | str],
        value: str | bytes = ...,
        mutable: bool = ...,
        encoding: str | None = ...,
    ) -> Self: ...
    @property
    def encoding(self) -> str: ...
    @encoding.setter
    def encoding(self, value: str) -> None: ...
    def __setitem__(self, key: str | bytes, value: str | bytes) -> None: ...
    def __delitem__(self, key: str | bytes) -> None: ...
    def setlist(self, key: str | bytes, list_: Iterable[str | bytes]) -> None: ...
    def setlistdefault(self, key: str | bytes, default_list: list[str] | None = ...) -> list[str]: ...
    def appendlist(self, key: str | bytes, value: str | bytes) -> None: ...
    # Fake signature (because *args is used in source, but it fails with more that 1 argument)
    @overload
    def pop(self, key: str | bytes, /) -> str: ...
    @overload
    def pop(self, key: str | bytes, default: str | _Z = ..., /) -> str | _Z: ...
    def popitem(self) -> tuple[str, str]: ...
    def clear(self) -> None: ...
    def setdefault(self, key: str | bytes, default: str | bytes | None = ...) -> str: ...
    def copy(self) -> QueryDict: ...
    def urlencode(self, safe: str | None = ...) -> str: ...

@type_check_only
class _ImmutableQueryDict(QueryDict):
    _mutable: Literal[False]
    # def __init__(
    #     self, query_string: Optional[Union[str, bytes]] = ..., mutable: bool = ..., encoding: Optional[str] = ...
    # ) -> None: ...
    def __setitem__(self, key: str | bytes, value: str | bytes) -> NoReturn: ...
    def __delitem__(self, key: str | bytes) -> NoReturn: ...
    def setlist(self, key: str | bytes, list_: Iterable[str | bytes]) -> NoReturn: ...
    def setlistdefault(self, key: str | bytes, default_list: list[str] | None = ...) -> NoReturn: ...
    def appendlist(self, key: str | bytes, value: str | bytes) -> NoReturn: ...
    # Fake signature (because *args is used in source, but it fails with more that 1 argument)
    @overload
    def pop(self, key: str | bytes, /) -> NoReturn: ...
    @overload
    def pop(self, key: str | bytes, default: str | _Z = ..., /) -> NoReturn: ...
    def popitem(self) -> NoReturn: ...
    def clear(self) -> NoReturn: ...
    def setdefault(self, key: str | bytes, default: str | bytes | None = ...) -> NoReturn: ...
    def copy(self) -> QueryDict: ...  # type: ignore[override]
    def urlencode(self, safe: str | None = ...) -> str: ...
    # Fakes for convenience (for `request.GET` and `request.POST`). If dict
    # was created by Django, there is no chance to hit `List[object]` (empty list)
    # edge case.
    def __getitem__(self, key: str) -> str: ...
    def dict(self) -> dict[str, str]: ...  # type: ignore[override]

class MediaType:
    main_type: str
    sub_type: str
    params: dict[str, bytes]
    def __init__(self, media_type_raw_line: str) -> None: ...
    @property
    def is_all_types(self) -> bool: ...
    def match(self, other: str) -> bool: ...

@overload
def bytes_to_text(s: None, encoding: str) -> None: ...
@overload
def bytes_to_text(s: bytes | str, encoding: str) -> str: ...
def split_domain_port(host: str) -> tuple[str, str]: ...
def validate_host(host: str, allowed_hosts: Iterable[str]) -> bool: ...
