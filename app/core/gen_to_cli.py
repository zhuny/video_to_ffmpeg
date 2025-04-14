from app.core.models import VideoModel, VideoPoint


class KeyCounter:
    def __init__(self, char):
        self.char = char
        self.counter = 0

    def get(self):
        result = f"{self.char}{self.counter}"
        self.counter += 1
        return result


class FfmpegGenerator:
    def __init__(self, model: VideoModel):
        self.model = model
        self.key_counter = KeyCounter('z')
        self.duration = VideoPoint("0.5")

        self.output_video_key = None
        self.output_audio_key = None

    def generate(self):
        yield from self._generate_video()
        yield from self._generate_audio()

    def _generate_video(self):
        prev_key = None
        offset_time = VideoPoint()

        for piece in self.model.piece_list:
            current_key = self.key_counter.get()
            yield {
                "input": self._get_piece_input(piece, 'v'),
                "filters": [
                    {
                        "name": "trim",
                        "kwargs": {
                            "start": piece.start,
                            "end": piece.end
                        }
                    },
                    {
                        "name": "setpts",
                        "args": "PTS-STARTPTS"
                    }
                ],
                "output": [current_key]
            }
            if prev_key is not None:
                next_key = self.key_counter.get()
                offset_time -= self.duration

                yield {
                    "input": [prev_key, current_key],
                    "filters": [
                        {
                            "name": "xfade",
                            "kwargs": {
                                "transition": "fade",
                                "duration": self.duration,
                                "offset": offset_time
                            }
                        }
                    ],
                    "output": [next_key]
                }
                prev_key = next_key
            else:
                prev_key = current_key

            offset_time += piece.end - piece.start

        self.output_video_key = prev_key

    def _generate_audio(self):
        prev_key = None

        for piece in self.model.piece_list:
            current_key = self.key_counter.get()
            yield {
                "input": self._get_piece_input(piece, 'a'),
                "filters": [
                    {
                        "name": "atrim",
                        "kwargs": {
                            "start": piece.start,
                            "end": piece.end
                        }
                    },
                    {
                        "name": "asetpts",
                        "args": "PTS-STARTPTS"
                    }
                ],
                "output": [current_key]
            }
            if prev_key is not None:
                next_key = self.key_counter.get()
                yield {
                    "input": [prev_key, current_key],
                    "filters": [
                        {
                            "name": "acrossfade",
                            "kwargs": {
                                "duration": self.duration
                            }
                        }
                    ],
                    "output": [next_key]
                }
                prev_key = next_key

            else:
                prev_key = current_key

        self.output_audio_key = prev_key

    def _get_piece_input(self, piece, t_):
        return [f"{piece.file_id}:{t_}"]
