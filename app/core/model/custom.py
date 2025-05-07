import re
from decimal import Decimal
from typing import Any

import pydantic
from pydantic_core import core_schema


class VideoPoint(Decimal):
    @classmethod
    def validate(cls, value: Any, handler=None, info: pydantic.ValidationInfo=None):
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

        return cls(value)

    def __str__(self):
        upper, lower = divmod(self, 1)
        string_list = []
        while upper > 0:
            upper, r = divmod(upper, 60)
            if upper > 0:
                r_t = f':{r:02}'
            else:
                r_t = str(r)
            string_list.append(r_t)

        string_list.reverse()

        if lower > 0:
            string_list.append(str(lower).lstrip('0'))

        return ''.join(string_list)

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
        result = self.value = []
        pattern = re.compile(r"(\d+)-(\d+)")

        for v in value.split(","):
            print(value, v)
            if g := pattern.fullmatch(v):
                start, end = g.groups()
                start, end = int(start), int(end)
                result.extend(range(start, end+1))
            else:
                result.append(int(v))

    def shuffle(self):
        import random
        random.shuffle(self.value)

    def __iter__(self):
        yield from self.value

    @classmethod
    def validate(cls, value: Any, handler=None, info: pydantic.ValidationInfo=None):
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
