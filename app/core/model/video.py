import json
import subprocess
from pathlib import Path

import pydantic

from app.config import setting
from app.core.model.custom import VideoPoint


class VideoPieceModel(pydantic.BaseModel):
    file_id: int
    start: VideoPoint
    end: VideoPoint


class VideoModel(pydantic.BaseModel):
    name: str = ""
    video_name: str = ""
    video_description: str = ""
    piece_list: list[VideoPieceModel] = []
    video_input: list[Path] = []

    def is_empty(self):
        return len(self.piece_list) == 0


class VideoOutput:
    def __init__(self, number: int):
        self.number = number
        self.model = VideoModel()

    def is_exists(self):
        return self.info_file.exists()

    @property
    def video_folder(self) -> Path:
        root = Path("~/Videos/ffmpeg").expanduser()
        return root / self._cell(100) / self._cell(10) / self._cell(1)

    @property
    def info_file(self):
        return self.video_folder / 'info.json'

    @property
    def output_file(self):
        return self.video_folder / 'output.ts'

    def update_meta(self, name="", video_name="", video_description=""):
        updated = {
            'name': name,
            'video_name': video_name,
            'video_description': video_description
        }
        updated = {
            k: v
            for k, v in updated.items()
            if v
        }
        self.model = self.model.model_copy(update=updated)

    def is_empty(self):
        return self.model.is_empty()

    def save(self):
        self.video_folder.mkdir(parents=True, exist_ok=True)
        self.info_file.write_text(json.dumps(self.model.model_dump(mode='json')))

    def load(self):
        info = json.loads(self.info_file.read_text())
        self.model = VideoModel.model_validate(info)

    def is_valid_file_id(self, file_id):
        return 0 <= file_id < len(self.model.video_input)

    def add_video_input(self, filename):
        current_index = len(self.model.video_input)
        self.model.video_input.append(filename)
        return current_index

    def add_piece(self, piece: VideoPieceModel):
        assert self.is_valid_file_id(piece.file_id)

        self.model.piece_list.append(piece)

    def generate_output(self):
        from app.core.ffmpeg_model_to_cli import FfmpegModelToCli
        from app.core.ffmpeg_video_to_model import FfmpegVideoToModel

        pipeline_list = [
            FfmpegVideoToModel,
            FfmpegModelToCli
        ]
        data = self

        for pipe in pipeline_list:
            data = pipe(data).generate()

        print(data)
        subprocess.run(data)

    def _cell(self, u: int) -> str:
        ceil_num = self.number // u * u
        return f'{ceil_num:03}'
