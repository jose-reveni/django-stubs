from typing import Any

from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.backends.mysql.base import DatabaseWrapper

class DatabaseOperations(BaseDatabaseOperations):
    connection: DatabaseWrapper
    compiler_module: str
    integer_field_ranges: dict[str, tuple[int, int]]
    cast_data_types: dict[str, str]
    cast_char_field_without_max_length: str
    explain_prefix: str
    def date_extract_sql(self, lookup_type: str, field_name: str) -> Any: ...
    def date_trunc_sql(self, lookup_type: str, field_name: str, tzname: str | None = ...) -> Any: ...
    def datetime_cast_date_sql(self, field_name: str, tzname: str | None) -> Any: ...
    def datetime_cast_time_sql(self, field_name: str, tzname: str | None) -> Any: ...
    def datetime_extract_sql(self, lookup_type: str, field_name: str, tzname: str | None) -> Any: ...
    def datetime_trunc_sql(self, lookup_type: str, field_name: str, tzname: str | None) -> Any: ...
    def time_trunc_sql(self, lookup_type: str, field_name: str, tzname: str | None = ...) -> Any: ...
    def fetch_returned_insert_rows(self, cursor: Any) -> Any: ...
    def format_for_duration_arithmetic(self, sql: Any) -> Any: ...
    def force_no_ordering(self) -> Any: ...
    def last_executed_query(self, cursor: Any, sql: Any, params: Any) -> Any: ...
    def no_limit_value(self) -> Any: ...
    def quote_name(self, name: str) -> Any: ...
    def return_insert_columns(self, fields: Any) -> Any: ...
    def sequence_reset_by_name_sql(self, style: Any, sequences: Any) -> Any: ...
    def validate_autopk_value(self, value: Any) -> Any: ...
    def adapt_datetimefield_value(self, value: Any) -> Any: ...
    def adapt_timefield_value(self, value: Any) -> Any: ...
    def max_name_length(self) -> Any: ...
    def bulk_insert_sql(self, fields: Any, placeholder_rows: Any) -> Any: ...
    def combine_expression(self, connector: Any, sub_expressions: Any) -> Any: ...
    def get_db_converters(self, expression: Any) -> Any: ...
    def convert_booleanfield_value(self, value: Any, expression: Any, connection: Any) -> Any: ...
    def convert_datetimefield_value(self, value: Any, expression: Any, connection: Any) -> Any: ...
    def convert_uuidfield_value(self, value: Any, expression: Any, connection: Any) -> Any: ...
    def binary_placeholder_sql(self, value: Any) -> Any: ...
    def subtract_temporals(self, internal_type: Any, lhs: Any, rhs: Any) -> Any: ...
    def explain_query_prefix(self, format: Any | None = ..., **options: Any) -> Any: ...
    def regex_lookup(self, lookup_type: str) -> Any: ...
    def insert_statement(self, ignore_conflicts: bool = ...) -> Any: ...
    def lookup_cast(self, lookup_type: str, internal_type: Any | None = ...) -> Any: ...
