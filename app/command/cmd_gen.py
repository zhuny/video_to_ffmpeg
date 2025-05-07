from pathlib import Path

from app.core.model.custom import IntList
from app.core.model.video import VideoOutput


def run(video_id_list: IntList):
    """
    ffmpeg 코멘드로 변환하여 비디오를 생성합니다.

    :param video_id_list: 생성할 비디오 ID리스트 (comma seperated)
    """

    for video_id in video_id_list:
        video = VideoOutput(video_id)
        if not video.is_exists():
            print(f"Video Id ({video_id}) Not Exists")
            return

        video.load()

        if video.is_empty():
            print(f"Add Piece First!")
            return

        video.generate_output()
        video.generate_thumbnail()

        for png in video.video_folder.glob('*.png'):
            png: Path
            png_new = png.with_stem(
                stem=png.stem.replace(
                    'thumb',
                    f'thumb_{video_id:03}'
                )
            )
            print(png, png_new)
            png.replace(png_new)
