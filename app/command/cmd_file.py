from pathlib import Path

from app.core.model.video import VideoOutput


def run(video_id: int, filename: Path):
    """
    Video에 사용할 동영상을 추가합니다.

    :param video_id: Video ID
    :param filename: 사용할 파일 이름
    """
    video = VideoOutput(video_id)
    if not video.is_exists():
        print("Video Not Exists!")
        return

    video.load()
    index = video.add_video_input(filename)
    video.save()
    print(f"New File : {filename}")
    print(f"File Index : {index}")
