from collections.abc import Iterable, Iterator, Sequence, Sized
from typing import ClassVar, Generic, Protocol, TypeVar, overload

from django.utils.functional import _StrPromise

class UnorderedObjectListWarning(RuntimeWarning): ...
class InvalidPage(Exception): ...
class PageNotAnInteger(InvalidPage): ...
class EmptyPage(InvalidPage): ...

_T = TypeVar("_T")

class _SupportsPagination(Protocol[_T], Sized, Iterable):
    @overload
    def __getitem__(self, __index: int) -> _T: ...
    @overload
    def __getitem__(self, __index: slice) -> _SupportsPagination[_T]: ...

class Paginator(Generic[_T]):
    ELLIPSIS: ClassVar[_StrPromise]
    object_list: _SupportsPagination[_T]
    per_page: int
    orphans: int
    allow_empty_first_page: bool
    def __init__(
        self,
        object_list: _SupportsPagination[_T],
        per_page: int | str,
        orphans: int = ...,
        allow_empty_first_page: bool = ...,
    ) -> None: ...
    def __iter__(self) -> Iterator[Page[_T]]: ...
    def validate_number(self, number: int | float | str) -> int: ...
    def get_page(self, number: int | float | str | None) -> Page[_T]: ...
    def page(self, number: int | str) -> Page[_T]: ...
    @property
    def count(self) -> int: ...
    @property
    def num_pages(self) -> int: ...
    @property
    def page_range(self) -> range: ...
    def get_elided_page_range(
        self, number: int | float | str = ..., *, on_each_side: int = ..., on_ends: int = ...
    ) -> Iterator[str | int]: ...

class Page(Sequence[_T]):
    object_list: _SupportsPagination[_T]
    number: int
    paginator: Paginator
    def __init__(
        self,
        object_list: _SupportsPagination[_T],
        number: int,
        paginator: Paginator,
    ) -> None: ...
    @overload
    def __getitem__(self, index: int) -> _T: ...
    @overload
    def __getitem__(self, index: slice) -> Sequence[_T]: ...  # Avoid override error
    def __len__(self) -> int: ...
    def has_next(self) -> bool: ...
    def has_previous(self) -> bool: ...
    def has_other_pages(self) -> bool: ...
    def next_page_number(self) -> int: ...
    def previous_page_number(self) -> int: ...
    def start_index(self) -> int: ...
    def end_index(self) -> int: ...
