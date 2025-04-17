import functools
from typing import Callable, Any

from app.config import setting
from app.core.model.ffmpeg import FfmpegCommand, FfmpegFilter, FfmpegFilterOne


def join(f) -> Callable[[Any], str]:
    @functools.wraps(f)
    def wrapped(self, *args, **kwargs) -> str:
        return ''.join(f(self, *args, **kwargs))
    return wrapped


def to_list(f):
    @functools.wraps(f)
    def wrapped(self, *args, **kwargs):
        return list(f(self, *args, **kwargs))
    return wrapped


class FfmpegModelToCli:
    def __init__(self, model: FfmpegCommand):
        assert isinstance(model, FfmpegCommand)
        self.model = model

    @to_list
    def generate(self):
        yield str(setting.ffmpeg_executable)

        yield from "-hwaccel cuda".split()

        for i in self.model.inputs:
            yield "-i"
            yield str(i)

        yield "-filter_complex"
        yield ";".join(self._build_filter(f) for f in self.model.filter_group)

        yield "-map"
        yield self._index_wrap(self.model.output_video)
        yield "-map"
        yield self._index_wrap(self.model.output_audio)

        yield from "-codec:v libx264 -crf 18 -preset slow".split()

        yield str(self.model.output_file)

    @join
    def _build_filter(self, f: FfmpegFilter):
        for i in f.inputs:
            yield self._index_wrap(i)

        yield ",".join(self._build_filter_kwargs(kw) for kw in f.filters)

        for o in f.outputs:
            yield self._index_wrap(o)

    @join
    def _build_filter_kwargs(self, kw: FfmpegFilterOne):
        yield kw.name
        yield "="

        if kw.argv:
            yield kw.argv

        yield ":".join(
            f'{k}={v}'
            for k, v in kw.kwargs.items()
        )

    def _index_wrap(self, index):
        return f'[{index}]'
