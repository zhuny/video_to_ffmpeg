import json
from pathlib import Path


class VideoOutput:
    def __init__(self, number: int):
        self.number = number

        self.name = ""
        self.video_input = []
        self.piece_list = []

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
    def json(self):
        return {
            "name": self.name,
            "video_input": self.video_input,
            "piece_list": self.piece_list
        }

    def create(self, name: str):
        self.name = name
        self._save()

    def _cell(self, u: int) -> str:
        ceil_num = self.number // u * u
        return f'{ceil_num:03}'

    def _save(self):
        self.video_folder.mkdir(parents=True, exist_ok=True)
        self.info_file.write_text(json.dumps(self.json))
