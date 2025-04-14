import re
from decimal import Decimal
from typing import Any

import pydantic
from pydantic_core import core_schema


class VideoPoint(Decimal):
    @classmethod
    def validate(cls, value: Any, handler, info: pydantic.ValidationInfo):
        value = str(value)
        if g := re.fullmatch(r"(?:(\d+):)?(\d+):(\d+)(?:\.(\d+))?", value):
            hours, minutes, seconds, milliseconds = g.groups()
            hours = cls._wrap_num(hours)
            minutes = cls._wrap_num(minutes)
            seconds = cls._wrap_num(seconds)
            milliseconds = cls._wrap_num_milli(milliseconds)
            value = (
                hours * 3600 + minutes * 60 + seconds + milliseconds
            )
        else:
            value = Decimal(value)
        return VideoPoint(value)

    @classmethod
    def _wrap_num(cls, num_text):
        return Decimal(num_text or 0)

    @classmethod
    def _wrap_num_milli(cls, num_text):
        return Decimal(f"0.{num_text}" if num_text else "0")

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
