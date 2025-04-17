from app.core.model.custom import VideoPoint
from app.core.model.ffmpeg import FfmpegFilter, FfmpegFilterOne, FfmpegCommand
from app.core.model.video import VideoModel, VideoOutput


class KeyCounter:
    def __init__(self, char):
        self.char = char
        self.counter = 0

    def get(self):
        result = f"{self.char}{self.counter}"
        self.counter += 1
        return result


class FfmpegVideoToModel:
    def __init__(self, model: VideoOutput):
        self.meta = model
        self.model = model.model
        self.key_counter = KeyCounter('z')
        self.duration = VideoPoint("0.5")

        self.output_video_key = None
        self.output_audio_key = None

    def generate(self):
        filter_list = []
        filter_list.extend(self._generate_video())
        filter_list.extend(self._generate_audio())

        return FfmpegCommand(
            inputs=list(self.model.video_input),
            filter_group=filter_list,
            output_video=self.output_video_key,
            output_audio=self.output_audio_key,
            output_file=self.meta.output_file
        )

    def _generate_video(self):
        prev_key = None
        offset_time = VideoPoint()

        for piece in self.model.piece_list:
            current_key = self.key_counter.get()
            yield FfmpegFilter(
                inputs=self._get_piece_input(piece, 'v'),
                filters=[
                    FfmpegFilterOne(
                        name="trim",
                        kwargs={
                            "start": piece.start,
                            "end": piece.end
                        }
                    ),
                    FfmpegFilterOne(name="setpts", argv="PTS-STARTPTS"),
                    FfmpegFilterOne(name="settb", argv="AVTB"),
                    FfmpegFilterOne(name="fps", argv="60")
                ],
                outputs=[current_key]
            )
            if prev_key is not None:
                next_key = self.key_counter.get()
                offset_time -= self.duration

                yield FfmpegFilter(
                    inputs=[prev_key, current_key],
                    filters=[
                        FfmpegFilterOne(
                            name="xfade",
                            kwargs={
                                "transition": "fade",
                                "duration": self.duration,
                                "offset": offset_time
                            }
                        ),
                        FfmpegFilterOne(
                            name="format",
                            argv="yuv420p"
                        )
                    ],
                    outputs=[next_key]
                )
                prev_key = next_key
            else:
                prev_key = current_key

            offset_time += piece.end - piece.start

        self.output_video_key = prev_key

    def _generate_audio(self):
        prev_key = None

        for piece in self.model.piece_list:
            current_key = self.key_counter.get()
            yield FfmpegFilter(
                inputs=self._get_piece_input(piece, 'a'),
                filters=[
                    FfmpegFilterOne(
                        name="atrim",
                        kwargs={
                            "start": piece.start,
                            "end": piece.end
                        }
                    ),
                    FfmpegFilterOne(
                        name="asetpts",
                        argv="PTS-STARTPTS"
                    )
                ],
                outputs=[current_key]
            )
            if prev_key is not None:
                next_key = self.key_counter.get()
                yield FfmpegFilter(
                    inputs=[prev_key, current_key],
                    filters=[
                        FfmpegFilterOne(
                            name="acrossfade",
                            kwargs={
                                "duration": self.duration
                            }
                        )
                    ],
                    outputs=[next_key]
                )
                prev_key = next_key
            else:
                prev_key = current_key

        self.output_audio_key = prev_key

    def _get_piece_input(self, piece, t_):
        return [f"{piece.file_id}:{t_}"]
