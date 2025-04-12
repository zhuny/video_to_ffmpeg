from pathlib import Path
from typing import Any

from pydantic import BaseModel


class FfmpegFilterOne(BaseModel):
    name: str
    kwargs: dict[str, Any]


class FfmpegFilter(BaseModel):
    inputs: list[str]
    filters: list[FfmpegFilterOne]
    outputs: list[str]


class FfmpegCommand(BaseModel):
    inputs: list[Path]
    filter_group: list[FfmpegFilter]
    output_video: str
    output_audio: str
    output_file: Path
