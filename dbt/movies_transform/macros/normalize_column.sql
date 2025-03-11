{% macro normalize(column) %}
    LOWER ( TRIM ( {{ column }} ) )
{% endmacro %}
