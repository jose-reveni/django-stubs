from collections.abc import Iterator
from pathlib import Path
from typing import Any

from django.core.exceptions import ImproperlyConfigured
from django.template.backends.base import BaseEngine
from django.utils.functional import cached_property

class InvalidTemplateEngineError(ImproperlyConfigured): ...

class EngineHandler:
    def __init__(self, templates: list[dict[str, Any]] | None = None) -> None: ...
    @cached_property
    def templates(self) -> dict[str, Any]: ...
    def __getitem__(self, alias: str) -> BaseEngine: ...
    def __iter__(self) -> Iterator[Any]: ...
    def all(self) -> list[BaseEngine]: ...

def get_app_template_dirs(dirname: str) -> tuple[Path, ...]: ...
