"""
Delegate as much validation as possible out to jsonschema. This module serves
as the single point of entry for validations should we need to further
customize the behavior.
"""

from bravado_core.exception import SwaggerMappingError
from bravado_core.schema import SWAGGER_PRIMITIVES
from bravado_core.swagger20_validator import Swagger20Validator


def validate_schema_object(swagger_spec, schema_object_spec, value):
    """
    :raises ValidationError: when jsonschema validation fails.
    :raises SwaggerMappingError: on invalid Swagger `type`.
    :raises SwaggerValidationError: when user-defined format validation fails.
    """
    obj_type = schema_object_spec['type']

    if obj_type in SWAGGER_PRIMITIVES:
        validate_primitive(swagger_spec, schema_object_spec, value)

    elif obj_type == 'array':
        validate_array(swagger_spec, schema_object_spec, value)

    elif obj_type == 'object':
        validate_object(swagger_spec, schema_object_spec, value)

    elif obj_type == 'file':
        pass

    else:
        raise SwaggerMappingError('Unknown type {0} for value {1}'.format(
            obj_type, value))


def validate_primitive(swagger_spec, primitive_spec, value):
    """
    :type swagger_spec: :class:`bravado_core.spec.Spec`
    :param primitive_spec: spec for a swagger primitive type in dict form
    :type value: int, string, float, long, etc
    """
    Swagger20Validator(
        primitive_spec,
        format_checker=swagger_spec.format_checker).validate(value)


def validate_array(swagger_spec, array_spec, value):
    """
    :type swagger_spec: :class:`bravado_core.spec.Spec`
    :param spec: spec for an 'array' type in dict form
    :type value: list
    """
    Swagger20Validator(
        array_spec,
        format_checker=swagger_spec.format_checker).validate(value)


def validate_object(swagger_spec, object_spec, value):
    """
    :type swagger_spec: :class:`bravado_core.spec.Spec`
    :param object_spec: spec for an 'object' type in dict form
    :type value: dict
    """
    Swagger20Validator(
        object_spec,
        format_checker=swagger_spec.format_checker).validate(value)
