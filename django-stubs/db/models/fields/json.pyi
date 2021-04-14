from . import Field
from .mixins import CheckFieldDefaultMixin
from django.db.models import lookups
from django.db.models.lookups import PostgresOperatorLookup, Transform
from typing import Any, Optional, Callable

class JSONField(CheckFieldDefaultMixin, Field):
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        encoder: Optional[Callable] = ...,
        decoder: Optional[Callable] = ...,
        **kwargs: Any
    ) -> None: ...

class DataContains(PostgresOperatorLookup): ...
class ContainedBy(PostgresOperatorLookup): ...
class HasKeyLookup(PostgresOperatorLookup): ...
class HasKey(HasKeyLookup): ...
class HasKeys(HasKeyLookup): ...
class HasAnyKeys(HasKeys): ...
class JSONExact(lookups.Exact): ...

class KeyTransform(Transform):
    key_name: Any = ...
    def __init__(self, key_name: Any, *args: Any, **kwargs: Any) -> None: ...
    def preprocess_lhs(self, compiler: Any, connection: Any, lhs_only: bool = ...): ...

class KeyTextTransform(KeyTransform): ...

class KeyTransformTextLookupMixin:
    def __init__(self, key_transform: Any, *args: Any, **kwargs: Any) -> None: ...

class CaseInsensitiveMixin: ...
class KeyTransformIsNull(lookups.IsNull): ...
class KeyTransformIn(lookups.In): ...
class KeyTransformExact(JSONExact): ...
class KeyTransformIExact(CaseInsensitiveMixin, KeyTransformTextLookupMixin, lookups.IExact): ...
class KeyTransformIContains(CaseInsensitiveMixin, KeyTransformTextLookupMixin, lookups.IContains): ...
class KeyTransformStartsWith(KeyTransformTextLookupMixin, lookups.StartsWith): ...
class KeyTransformIStartsWith(CaseInsensitiveMixin, KeyTransformTextLookupMixin, lookups.IStartsWith): ...
class KeyTransformEndsWith(KeyTransformTextLookupMixin, lookups.EndsWith): ...
class KeyTransformIEndsWith(CaseInsensitiveMixin, KeyTransformTextLookupMixin, lookups.IEndsWith): ...
class KeyTransformRegex(KeyTransformTextLookupMixin, lookups.Regex): ...
class KeyTransformIRegex(CaseInsensitiveMixin, KeyTransformTextLookupMixin, lookups.IRegex): ...
class KeyTransformNumericLookupMixin: ...
class KeyTransformLt(KeyTransformNumericLookupMixin, lookups.LessThan): ...
class KeyTransformLte(KeyTransformNumericLookupMixin, lookups.LessThanOrEqual): ...
class KeyTransformGt(KeyTransformNumericLookupMixin, lookups.GreaterThan): ...
class KeyTransformGte(KeyTransformNumericLookupMixin, lookups.GreaterThanOrEqual): ...

class KeyTransformFactory:
    key_name: Any = ...
    def __init__(self, key_name: Any) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any): ...
