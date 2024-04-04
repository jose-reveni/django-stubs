import datetime
from collections.abc import AsyncIterator, Collection, Iterable, Iterator, MutableMapping, Reversible, Sequence, Sized
from typing import Any, Generic, NamedTuple, TypeVar, overload

from django.db.backends.utils import _ExecuteQuery
from django.db.models import Manager
from django.db.models.base import Model
from django.db.models.expressions import Combinable, OrderBy
from django.db.models.sql.query import Query, RawQuery
from django.utils.functional import cached_property
from typing_extensions import Self, TypeAlias

_T = TypeVar("_T", bound=Model, covariant=True)
_Row = TypeVar("_Row", covariant=True)
_QS = TypeVar("_QS", bound=_QuerySet)
_TupleT = TypeVar("_TupleT", bound=tuple[Any, ...], covariant=True)

MAX_GET_RESULTS: int
REPR_OUTPUT_SIZE: int

class BaseIterable(Generic[_Row]):
    queryset: QuerySet[Model]
    chunked_fetch: bool
    chunk_size: int
    def __init__(self, queryset: QuerySet[Model], chunked_fetch: bool = ..., chunk_size: int = ...) -> None: ...
    def __aiter__(self) -> AsyncIterator[_Row]: ...

class ModelIterable(Generic[_T], BaseIterable[_T]):
    def __iter__(self) -> Iterator[_T]: ...

class RawModelIterable(BaseIterable[dict[str, Any]]):
    def __iter__(self) -> Iterator[dict[str, Any]]: ...

class ValuesIterable(BaseIterable[dict[str, Any]]):
    def __iter__(self) -> Iterator[dict[str, Any]]: ...

class ValuesListIterable(BaseIterable[_TupleT]):
    def __iter__(self) -> Iterator[_TupleT]: ...

class NamedValuesListIterable(ValuesListIterable[NamedTuple]):
    def __iter__(self) -> Iterator[NamedTuple]: ...

class FlatValuesListIterable(BaseIterable[_Row]):
    def __iter__(self) -> Iterator[_Row]: ...

class _QuerySet(Generic[_T, _Row], Reversible[_Row], Iterable[_Row], Sized):
    model: type[_T]
    query: Query
    _iterable_class: type[BaseIterable]
    _result_cache: list[_Row] | None
    def __init__(
        self,
        model: type[Model] | None = ...,
        query: Query | None = ...,
        using: str | None = ...,
        hints: dict[str, Model] | None = ...,
    ) -> None: ...
    @classmethod
    def as_manager(cls) -> Manager[_T]: ...
    def __len__(self) -> int: ...
    def __bool__(self) -> bool: ...
    def __class_getitem__(cls: type[_QS], item: type[_T]) -> type[_QS]: ...
    def __getstate__(self) -> dict[str, Any]: ...
    # Technically, the other QuerySet must be of the same type _T, but _T is covariant
    def __and__(self, other: _QuerySet[_T, _Row]) -> Self: ...
    def __or__(self, other: _QuerySet[_T, _Row]) -> Self: ...
    # IMPORTANT: When updating any of the following methods' signatures, please ALSO modify
    # the corresponding method in BaseManager.
    def iterator(self, chunk_size: int | None = ...) -> Iterator[_Row]: ...
    def aiterator(self, chunk_size: int = ...) -> AsyncIterator[_Row]: ...
    def aggregate(self, *args: Any, **kwargs: Any) -> dict[str, Any]: ...
    async def aaggregate(self, *args: Any, **kwargs: Any) -> dict[str, Any]: ...
    def get(self, *args: Any, **kwargs: Any) -> _Row: ...
    async def aget(self, *args: Any, **kwargs: Any) -> _Row: ...
    def create(self, **kwargs: Any) -> _T: ...
    async def acreate(self, **kwargs: Any) -> _T: ...
    def bulk_create(
        self,
        objs: Iterable[_T],
        batch_size: int | None = ...,
        ignore_conflicts: bool = ...,
        update_conflicts: bool = ...,
        update_fields: Collection[str] | None = ...,
        unique_fields: Collection[str] | None = ...,
    ) -> list[_T]: ...
    async def abulk_create(
        self,
        objs: Iterable[_T],
        batch_size: int | None = ...,
        ignore_conflicts: bool = ...,
        update_conflicts: bool = ...,
        update_fields: Collection[str] | None = ...,
        unique_fields: Collection[str] | None = ...,
    ) -> list[_T]: ...
    def bulk_update(self, objs: Iterable[_T], fields: Iterable[str], batch_size: int | None = ...) -> int: ...
    async def abulk_update(self, objs: Iterable[_T], fields: Iterable[str], batch_size: int | None = ...) -> int: ...
    def get_or_create(self, defaults: MutableMapping[str, Any] | None = ..., **kwargs: Any) -> tuple[_T, bool]: ...
    async def aget_or_create(
        self, defaults: MutableMapping[str, Any] | None = ..., **kwargs: Any
    ) -> tuple[_T, bool]: ...
    def update_or_create(
        self,
        defaults: MutableMapping[str, Any] | None = ...,
        create_defaults: MutableMapping[str, Any] | None = ...,
        **kwargs: Any,
    ) -> tuple[_T, bool]: ...
    async def aupdate_or_create(
        self,
        defaults: MutableMapping[str, Any] | None = ...,
        create_defaults: MutableMapping[str, Any] | None = ...,
        **kwargs: Any,
    ) -> tuple[_T, bool]: ...
    def earliest(self, *fields: str | OrderBy) -> _Row: ...
    async def aearliest(self, *fields: str | OrderBy) -> _Row: ...
    def latest(self, *fields: str | OrderBy) -> _Row: ...
    async def alatest(self, *fields: str | OrderBy) -> _Row: ...
    def first(self) -> _Row | None: ...
    async def afirst(self) -> _Row | None: ...
    def last(self) -> _Row | None: ...
    async def alast(self) -> _Row | None: ...
    def in_bulk(self, id_list: Iterable[Any] | None = ..., *, field_name: str = ...) -> dict[Any, _T]: ...
    async def ain_bulk(self, id_list: Iterable[Any] | None = ..., *, field_name: str = ...) -> dict[Any, _T]: ...
    def delete(self) -> tuple[int, dict[str, int]]: ...
    async def adelete(self) -> tuple[int, dict[str, int]]: ...
    def update(self, **kwargs: Any) -> int: ...
    async def aupdate(self, **kwargs: Any) -> int: ...
    def exists(self) -> bool: ...
    async def aexists(self) -> bool: ...
    def explain(self, *, format: Any | None = ..., **options: Any) -> str: ...
    async def aexplain(self, *, format: Any | None = ..., **options: Any) -> str: ...
    def contains(self, obj: Model) -> bool: ...
    async def acontains(self, obj: Model) -> bool: ...
    def raw(
        self,
        raw_query: _ExecuteQuery,
        params: Any = ...,
        translations: dict[str, str] | None = ...,
        using: str | None = ...,
    ) -> RawQuerySet: ...
    # The type of values may be overridden to be more specific in the mypy plugin, depending on the fields param
    def values(self, *fields: str | Combinable, **expressions: Any) -> _QuerySet[_T, dict[str, Any]]: ...
    # The type of values_list may be overridden to be more specific in the mypy plugin, depending on the fields param
    def values_list(self, *fields: str | Combinable, flat: bool = ..., named: bool = ...) -> _QuerySet[_T, Any]: ...
    def dates(self, field_name: str, kind: str, order: str = ...) -> _QuerySet[_T, datetime.date]: ...
    def datetimes(
        self, field_name: str, kind: str, order: str = ..., tzinfo: datetime.tzinfo | None = ...
    ) -> _QuerySet[_T, datetime.datetime]: ...
    def none(self) -> Self: ...
    def all(self) -> Self: ...
    def filter(self, *args: Any, **kwargs: Any) -> Self: ...
    def exclude(self, *args: Any, **kwargs: Any) -> Self: ...
    def complex_filter(self, filter_obj: Any) -> Self: ...
    def count(self) -> int: ...
    async def acount(self) -> int: ...
    def union(self, *other_qs: Any, all: bool = ...) -> Self: ...
    def intersection(self, *other_qs: Any) -> Self: ...
    def difference(self, *other_qs: Any) -> Self: ...
    def select_for_update(
        self, nowait: bool = ..., skip_locked: bool = ..., of: Sequence[str] = ..., no_key: bool = ...
    ) -> Self: ...
    def select_related(self, *fields: Any) -> Self: ...
    def prefetch_related(self, *lookups: Any) -> Self: ...
    def annotate(self, *args: Any, **kwargs: Any) -> Self: ...
    def alias(self, *args: Any, **kwargs: Any) -> Self: ...
    def order_by(self, *field_names: Any) -> Self: ...
    def distinct(self, *field_names: Any) -> Self: ...
    # extra() return type won't be supported any time soon
    def extra(
        self,
        select: dict[str, Any] | None = ...,
        where: Sequence[str] | None = ...,
        params: Sequence[Any] | None = ...,
        tables: Sequence[str] | None = ...,
        order_by: Sequence[str] | None = ...,
        select_params: Sequence[Any] | None = ...,
    ) -> _QuerySet[Any, Any]: ...
    def reverse(self) -> Self: ...
    def defer(self, *fields: Any) -> Self: ...
    def only(self, *fields: Any) -> Self: ...
    def using(self, alias: str | None) -> Self: ...
    @property
    def ordered(self) -> bool: ...
    @property
    def db(self) -> str: ...
    def _fetch_all(self) -> None: ...
    def resolve_expression(self, *args: Any, **kwargs: Any) -> Any: ...
    def __iter__(self) -> Iterator[_Row]: ...
    def __aiter__(self) -> AsyncIterator[_Row]: ...
    @overload
    def __getitem__(self, i: int) -> _Row: ...
    @overload
    def __getitem__(self, s: slice) -> Self: ...
    def __reversed__(self) -> Iterator[_Row]: ...

class RawQuerySet(Iterable[_T], Sized):
    query: RawQuery
    def __init__(
        self,
        raw_query: RawQuery | str,
        model: type[Model] | None = ...,
        query: Query | None = ...,
        params: tuple[Any] = ...,
        translations: dict[str, str] | None = ...,
        using: str = ...,
        hints: dict[str, Model] | None = ...,
    ) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_T]: ...
    def __bool__(self) -> bool: ...
    @overload
    def __getitem__(self, k: int) -> _T: ...
    @overload
    def __getitem__(self, k: str) -> Any: ...
    @overload
    def __getitem__(self, k: slice) -> RawQuerySet[_T]: ...
    @cached_property
    def columns(self) -> list[str]: ...
    @property
    def db(self) -> str: ...
    def iterator(self) -> Iterator[_T]: ...
    @cached_property
    def model_fields(self) -> dict[str, str]: ...
    def prefetch_related(self, *lookups: Any) -> RawQuerySet[_T]: ...
    def resolve_model_init_order(self) -> tuple[list[str], list[int], list[tuple[str, int]]]: ...
    def using(self, alias: str | None) -> RawQuerySet[_T]: ...

_QuerySetAny: TypeAlias = _QuerySet  # noqa: PYI047

QuerySet: TypeAlias = _QuerySet[_T, _T]

class Prefetch:
    prefetch_through: str
    prefetch_to: str
    queryset: QuerySet | None
    to_attr: str | None
    def __init__(self, lookup: str, queryset: QuerySet | None = ..., to_attr: str | None = ...) -> None: ...
    def __getstate__(self) -> dict[str, Any]: ...
    def add_prefix(self, prefix: str) -> None: ...
    def get_current_prefetch_to(self, level: int) -> str: ...
    def get_current_to_attr(self, level: int) -> tuple[str, str]: ...
    def get_current_queryset(self, level: int) -> QuerySet | None: ...

def prefetch_related_objects(model_instances: Iterable[_T], *related_lookups: str | Prefetch) -> None: ...
async def aprefetch_related_objects(model_instances: Iterable[_T], *related_lookups: str | Prefetch) -> None: ...
def get_prefetcher(instance: Model, through_attr: str, to_attr: str) -> tuple[Any, Any, bool, bool]: ...

class InstanceCheckMeta(type): ...
class EmptyQuerySet(metaclass=InstanceCheckMeta): ...
