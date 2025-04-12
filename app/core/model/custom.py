import datetime
from typing import Any

import pydantic
from pydantic_core import core_schema


class VideoPoint:
    def __init__(self, value: str):
        self.value = datetime.time.fromisoformat(value)

    def __lt__(self, other):
        return self.value < other.value

    def __str__(self):
        return self.value.isoformat()

    @classmethod
    def validate(cls, value: Any, handler, info: pydantic.ValidationInfo):
        return cls(str(value))

    @classmethod
    def __get_pydantic_core_schema__(cls,
                                     source_type: Any,
                                     handler: pydantic.GetCoreSchemaHandler):
        return core_schema.with_info_wrap_validator_function(
            cls.validate,
            handler(str),
            field_name=handler.field_name,
            serialization=core_schema.PlainSerializerFunctionSerSchema(
                function=str,
                type='function-plain'
            )
        )


class IntList:
    def __init__(self, value: str):
        self.value = [int(_) for _ in value.split(",")]

    @classmethod
    def validate(cls, value: Any, handler, info: pydantic.ValidationInfo):
        return cls(str(value))

    @classmethod
    def __get_pydantic_core_schema__(cls,
                                     source_type: Any,
                                     handler: pydantic.GetCoreSchemaHandler):
        return core_schema.with_info_wrap_validator_function(
            cls.validate,
            handler(str),
            field_name=handler.field_name,
            serialization=core_schema.PlainSerializerFunctionSerSchema(
                function=str,
                type='function-plain'
            )
        )
