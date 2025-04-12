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

        video.generate_output()
