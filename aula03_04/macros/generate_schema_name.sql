{% macro generate_schema_name(custom_schema_name, node) %}

    {% set default_schema = target.schema %}

    {% if custom_schema_name is none %}

        {{ default_schema }}

    {% else %}

        {% if target.name == 'prod' %}

            {{ custom_schema_name | trim }}_prod

        {% elif target.name == 'dev' %}

            {{ custom_schema_name | trim }}_dev

        {% else %}

            {{ custom_schema_name | trim }}

        {% endif %}

    {% endif %}

{% endmacro %}
