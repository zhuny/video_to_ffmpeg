import datetime
import json
from pathlib import Path


class VideoPoint:
    def __init__(self, value: str):
        self.value = datetime.time.fromisoformat(value)

    def __lt__(self, other):
        return self.value < other.value

    def __str__(self):
        return self.value.isoformat()


class VideoPiece:
    def __init__(self, file_id, start, end):
        self.file_id = file_id
        self.start: VideoPoint = start
        self.end: VideoPoint = end

    @property
    def json(self):
        return {
            'file_id': self.file_id,
            'start': str(self.start),
            'end': str(self.end)
        }

    @classmethod
    def from_json(cls, piece):
        return cls(
            piece['file_id'],
            VideoPoint(piece['start']), VideoPoint(piece['end'])
        )


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
            "video_input": [
                str(vi) for vi in self.video_input
            ],
            "piece_list": [
                piece.json
                for piece in self.piece_list
            ]
        }

    def create(self, name: str):
        self.name = name

    def save(self):
        self.video_folder.mkdir(parents=True, exist_ok=True)
        self.info_file.write_text(json.dumps(self.json))

    def load(self):
        info = json.loads(self.info_file.read_text())
        self.name = info['name']
        self.video_input = [Path(vi) for vi in info['video_input']]
        self.piece_list = [
            VideoPiece.from_json(piece)
            for piece in info['piece_list']
        ]

    def add_video_input(self, filename):
        current_index = len(self.video_input)
        self.video_input.append(filename)
        return current_index

    def add_piece(self, piece: VideoPiece):
        assert 0 <= piece.file_id < len(self.video_input)

        self.piece_list.append(piece)

    def _cell(self, u: int) -> str:
        ceil_num = self.number // u * u
        return f'{ceil_num:03}'
